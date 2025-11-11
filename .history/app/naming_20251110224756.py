"""Filename generation and sanitization utilities."""
import re
from pathlib import Path
from typing import Dict, Optional


class FilenameGenerator:
    """Generates safe filenames from tags and templates."""
    
    def __init__(self, template: str, unsafe_chars: str = "/\\?*:\"<>|"):
        """Initialize with template and unsafe character list."""
        self.template = template
        self.unsafe_chars = unsafe_chars
        self._sanitize_pattern = re.compile(f"[{re.escape(unsafe_chars)}]")
    
    def sanitize(self, text: str) -> str:
        """Remove or replace unsafe characters."""
        if not text:
            return ""
        # Replace unsafe chars with underscore
        sanitized = self._sanitize_pattern.sub("_", text)
        # Remove leading/trailing dots and spaces
        sanitized = sanitized.strip(" .")
        # Collapse multiple underscores
        sanitized = re.sub(r"_+", "_", sanitized)
        return sanitized
    
    def generate(self, tags: Dict[str, str], original_path: Path, 
                 output_dir: Path, overwrite: bool = False) -> Path:
        """Generate output filename from tags and template."""
        # If template is {original}, just use original filename with .aiff extension
        if self.template == "{original}":
            # Keep original filename, just change extension to .aiff
            filename = original_path.stem + ".aiff"
            output_path = output_dir / filename
            
            # Handle collisions if not overwriting
            if not overwrite and output_path.exists():
                output_path = self._handle_collision(output_path)
            
            return output_path
        
        # Otherwise, use template-based naming (legacy support)
        # Extract values from tags, with fallbacks
        artist = tags.get("artist", "").strip()
        title = tags.get("title", "").strip()
        album = tags.get("album", "").strip()
        
        # Fallback to original filename if artist/title missing
        if not artist or not title:
            original_stem = original_path.stem
            if not artist:
                artist = original_stem
            if not title:
                title = original_stem
        
        # Sanitize values
        artist = self.sanitize(artist) if artist else "Unknown Artist"
        title = self.sanitize(title) if title else "Unknown Title"
        album = self.sanitize(album) if album else ""
        
        # Build filename from template
        filename = self.template.format(
            artist=artist,
            title=title,
            album=album,
            original=original_path.stem,  # Add original placeholder
            **{k: self.sanitize(str(v)) if v else "" for k, v in tags.items()}
        )
        
        # Ensure .aiff extension
        if not filename.endswith(".aiff"):
            filename += ".aiff"
        
        output_path = output_dir / filename
        
        # Handle collisions if not overwriting
        if not overwrite and output_path.exists():
            output_path = self._handle_collision(output_path)
        
        return output_path
    
    def _handle_collision(self, path: Path) -> Path:
        """Handle filename collisions by appending (2), (3), etc."""
        if not path.exists():
            return path
        
        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        counter = 2
        
        while True:
            new_name = f"{stem} ({counter}){suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
            
            # Safety limit
            if counter > 1000:
                # Fallback: add timestamp
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{stem}_{timestamp}{suffix}"
                return parent / new_name

