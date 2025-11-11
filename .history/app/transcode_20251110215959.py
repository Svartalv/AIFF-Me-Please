"""FFmpeg wrapper for FLAC to AIFF conversion."""
import subprocess
import os
from pathlib import Path
from typing import Optional, Tuple


class Transcoder:
    """Handles audio transcoding using ffmpeg."""
    
    def __init__(self, ffmpeg_path: Optional[str] = None):
        """Initialize transcoder with ffmpeg path."""
        self.ffmpeg_path = ffmpeg_path or self._find_ffmpeg()
    
    def _find_ffmpeg(self) -> str:
        """Find ffmpeg binary in app bundle or system."""
        import sys
        
        # Try bundled ffmpeg first (when running as .app)
        if getattr(sys, 'frozen', False):
            # Running as bundled app
            # PyInstaller puts binaries in the same directory as the executable
            bundle_path = Path(sys.executable).parent
            bundled_ffmpeg = bundle_path / "ffmpeg"
            if bundled_ffmpeg.exists() and bundled_ffmpeg.is_file():
                return str(bundled_ffmpeg)
            # Also try Contents/Resources (alternative bundle structure)
            bundle_path = Path(sys.executable).parent.parent
            bundled_ffmpeg = bundle_path / "Contents" / "Resources" / "ffmpeg"
            if bundled_ffmpeg.exists():
                return str(bundled_ffmpeg)
        
        # Try relative to script location (development)
        script_dir = Path(__file__).parent.parent
        bundled_ffmpeg = script_dir / "resources" / "ffmpeg" / "ffmpeg"
        if bundled_ffmpeg.exists():
            return str(bundled_ffmpeg)
        
        # Fallback to system ffmpeg
        return "ffmpeg"
    
    def convert(self, input_path: Path, output_path: Path, 
                sample_rate: int = 44100, bit_depth: int = 16) -> Tuple[bool, str]:
        """
        Convert FLAC to AIFF.
        
        Returns:
            (success: bool, error_message: str)
        """
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build ffmpeg command
        # -i: input file
        # -ar: sample rate
        # -ac: channels (2 = stereo)
        # -sample_fmt: sample format based on bit depth
        # -f: output format (aiff)
        # -y: overwrite (we handle this in engine, but ffmpeg needs it)
        
        if bit_depth == 16:
            sample_fmt = "s16"
        elif bit_depth == 24:
            sample_fmt = "s24"
        elif bit_depth == 32:
            sample_fmt = "s32"
        else:
            sample_fmt = "s16"  # Default to 16-bit
        
        cmd = [
            self.ffmpeg_path,
            "-i", str(input_path),
            "-ar", str(sample_rate),
            "-ac", "2",  # Stereo
            "-sample_fmt", sample_fmt,
            "-f", "aiff",
            "-y",  # Overwrite (we check before calling)
            str(output_path)
        ]
        
        try:
            # Run ffmpeg, capturing stderr for error messages
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.split('\n')[-5:]  # Last 5 lines
                return False, "\n".join(error_msg)
            
            # Verify output file exists
            if not output_path.exists():
                return False, "Output file was not created"
            
            # Basic validation: check file size
            if output_path.stat().st_size == 0:
                return False, "Output file is empty"
            
            return True, ""
            
        except FileNotFoundError:
            return False, f"ffmpeg not found at {self.ffmpeg_path}"
        except Exception as e:
            return False, str(e)
    
    def get_duration(self, file_path: Path) -> Optional[float]:
        """Get audio file duration in seconds using ffprobe."""
        try:
            # Try ffprobe (usually bundled with ffmpeg)
            ffprobe_path = self.ffmpeg_path.replace("ffmpeg", "ffprobe")
            if not os.path.exists(ffprobe_path):
                ffprobe_path = "ffprobe"
            
            cmd = [
                ffprobe_path,
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(file_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return float(result.stdout.strip())
        except Exception:
            return None

