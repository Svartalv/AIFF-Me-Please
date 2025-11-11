"""Conversion engine orchestrating the conversion process."""
import os
from pathlib import Path
from typing import List, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from .config import Config
from .transcode import Transcoder
from .tags import TagHandler
from .naming import FilenameGenerator
from .logging_utils import ConversionLogger


class ConversionEngine:
    """Orchestrates FLAC to AIFF conversion."""
    
    def __init__(self, config: Config, logger: ConversionLogger,
                 progress_callback: Optional[Callable[[str, int, int], None]] = None):
        """Initialize conversion engine."""
        self.config = config
        self.logger = logger
        self.progress_callback = progress_callback
        self.transcoder = Transcoder()
        self.tag_handler = TagHandler()
        self.filename_gen = FilenameGenerator(
            template=config.filename_template,
            unsafe_chars=config.unsafe_chars
        )
        self._cancelled = False
        self._lock = threading.Lock()
    
    def cancel(self) -> None:
        """Cancel ongoing conversion."""
        with self._lock:
            self._cancelled = True
    
    def _is_cancelled(self) -> bool:
        """Check if conversion was cancelled."""
        with self._lock:
            return self._cancelled
    
    def scan_flac_files(self, input_dir: Path) -> List[Path]:
        """Scan directory for FLAC files."""
        flac_files = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith('.flac'):
                    flac_files.append(Path(root) / file)
        return sorted(flac_files)
    
    def convert_file(self, flac_path: Path, output_dir: Path) -> bool:
        """Convert a single FLAC file to AIFF."""
        if self._is_cancelled():
            return False
        
        try:
            # Read tags
            tags = self.tag_handler.read_flac_tags(flac_path)
            tags = self.tag_handler.normalize_tags(tags)
            
            # Get artwork if enabled
            artwork = None
            if self.config.embed_artwork:
                artwork = self.tag_handler.get_artwork(flac_path)
            
            # Generate output filename
            output_path = self.filename_gen.generate(
                tags=tags,
                original_path=flac_path,
                output_dir=output_dir,
                overwrite=self.config.overwrite
            )
            
            # Check if output exists and overwrite is disabled
            if not self.config.overwrite and output_path.exists():
                self.logger.log_file_skip(
                    flac_path.name,
                    f"Output already exists: {output_path.name}"
                )
                return False
            
            # Log start
            self.logger.log_file_start(flac_path.name)
            
            # Convert audio
            success, error_msg = self.transcoder.convert(
                input_path=flac_path,
                output_path=output_path,
                sample_rate=self.config.sample_rate,
                bit_depth=self.config.bit_depth
            )
            
            if not success:
                self.logger.log_file_fail(flac_path.name, error_msg)
                return False
            
            # Write tags
            tag_success = self.tag_handler.write_aiff_tags(
                output_path,
                tags,
                artwork
            )
            
            if not tag_success:
                self.logger.warning(
                    f"Tag writing failed for {flac_path.name}, but file was converted"
                )
            
            # Log success
            self.logger.log_file_success(flac_path.name, output_path.name)
            return True
            
        except Exception as e:
            self.logger.log_file_fail(flac_path.name, str(e))
            return False
    
    def convert_batch(self, input_dir: Path, output_dir: Path) -> None:
        """Convert all FLAC files in input directory."""
        # Reset cancellation flag
        with self._lock:
            self._cancelled = False
        
        # Ensure output directory exists
        output_dir = Path(output_dir)
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.logger.error(f"Cannot create output directory {output_dir}: {e}")
            raise
        
        # Scan for FLAC files
        flac_files = self.scan_flac_files(input_dir)
        
        if not flac_files:
            error_msg = f"No FLAC files found in {input_dir}"
            self.logger.warning(error_msg)
            # Also log what files were found
            all_files = []
            try:
                for root, dirs, files in os.walk(input_dir):
                    for file in files:
                        all_files.append(file)
                if all_files:
                    self.logger.info(f"Found {len(all_files)} files in directory (none are FLAC)")
                else:
                    self.logger.info("Directory is empty")
            except Exception as e:
                self.logger.error(f"Error scanning directory: {e}")
            return
        
        total = len(flac_files)
        self.logger.info(f"Found {total} FLAC file(s) to convert")
        
        # Convert files
        concurrency = max(1, self.config.concurrency)
        
        if concurrency == 1:
            # Sequential processing
            for i, flac_path in enumerate(flac_files, 1):
                if self._is_cancelled():
                    self.logger.info("Conversion cancelled by user")
                    break
                
                if self.progress_callback:
                    self.progress_callback(flac_path.name, i, total)
                
                self.convert_file(flac_path, output_dir)
        else:
            # Parallel processing
            with ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures = {
                    executor.submit(self.convert_file, flac_path, output_dir): flac_path
                    for flac_path in flac_files
                }
                
                completed = 0
                for future in as_completed(futures):
                    if self._is_cancelled():
                        self.logger.info("Conversion cancelled by user")
                        # Cancel remaining tasks
                        for f in futures:
                            f.cancel()
                        break
                    
                    flac_path = futures[future]
                    completed += 1
                    
                    if self.progress_callback:
                        self.progress_callback(flac_path.name, completed, total)
                    
                    try:
                        future.result()
                    except Exception as e:
                        self.logger.log_file_fail(flac_path.name, str(e))
        
        # Log summary
        self.logger.log_summary()

