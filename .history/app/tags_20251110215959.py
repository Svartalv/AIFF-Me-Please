"""Tag reading and writing for FLAC and AIFF files."""
from pathlib import Path
from typing import Dict, Optional, Any
import mutagen
from mutagen.flac import FLAC
from mutagen.aiff import AIFF
from mutagen.id3 import ID3, TPE1, TPE2, TIT2, TALB, TDRC, TCON, TRCK, TPOS, COMM, TPUB, APIC


class TagHandler:
    """Handles reading FLAC tags and writing AIFF/ID3 tags."""
    
    # Tag mapping: FLAC field -> ID3 frame
    TAG_MAP = {
        "artist": ("TPE1", lambda v: TPE1(encoding=3, text=[str(v)])),
        "albumartist": ("TPE2", lambda v: TPE2(encoding=3, text=[str(v)])),
        "title": ("TIT2", lambda v: TIT2(encoding=3, text=[str(v)])),
        "album": ("TALB", lambda v: TALB(encoding=3, text=[str(v)])),
        "date": ("TDRC", lambda v: TDRC(text=[str(v)])),
        "year": ("TDRC", lambda v: TDRC(text=[str(v)])),
        "genre": ("TCON", lambda v: TCON(encoding=3, text=[str(v)])),
        "tracknumber": ("TRCK", lambda v: TRCK(encoding=3, text=[str(v)])),
        "discnumber": ("TPOS", lambda v: TPOS(encoding=3, text=[str(v)])),
        "comment": ("COMM", lambda v: COMM(encoding=3, lang="eng", desc="", text=[str(v)])),
        "label": ("TPUB", lambda v: TPUB(encoding=3, text=[str(v)])),
        "organization": ("TPUB", lambda v: TPUB(encoding=3, text=[str(v)])),
    }
    
    def read_flac_tags(self, flac_path: Path) -> Dict[str, str]:
        """Read tags from FLAC file."""
        tags = {}
        try:
            audio = FLAC(str(flac_path))
            for key, value_list in audio.items():
                # FLAC tags are typically uppercase, but mutagen normalizes
                key_lower = key.lower()
                if value_list:
                    # Take first value if multiple
                    tags[key_lower] = str(value_list[0])
        except Exception as e:
            # Return empty dict on error, caller will handle
            pass
        return tags
    
    def get_artwork(self, flac_path: Path) -> Optional[bytes]:
        """Extract artwork from FLAC file."""
        try:
            audio = FLAC(str(flac_path))
            pictures = audio.pictures
            if pictures:
                # Return first picture (usually front cover)
                return pictures[0].data
        except Exception:
            pass
        return None
    
    def write_aiff_tags(self, aiff_path: Path, tags: Dict[str, str], 
                        artwork: Optional[bytes] = None) -> bool:
        """Write tags to AIFF file using ID3."""
        try:
            audio = AIFF(str(aiff_path))
            
            # Add ID3 tag if it doesn't exist
            if audio.tags is None:
                audio.add_tags()
            
            # Map and write tags
            for flac_key, value in tags.items():
                if not value:
                    continue
                
                flac_key_lower = flac_key.lower()
                if flac_key_lower in self.TAG_MAP:
                    frame_id, frame_factory = self.TAG_MAP[flac_key_lower]
                    try:
                        frame = frame_factory(value)
                        audio.tags[frame_id] = frame
                    except Exception as e:
                        # Log warning but continue
                        pass
            
            # Handle artwork if provided
            if artwork:
                try:
                    # Determine MIME type from image data
                    mime_type = "image/jpeg"
                    if artwork.startswith(b'\x89PNG'):
                        mime_type = "image/png"
                    elif artwork.startswith(b'GIF'):
                        mime_type = "image/gif"
                    
                    apic = APIC(
                        encoding=3,
                        mime=mime_type,
                        type=3,  # Front cover
                        desc="",
                        data=artwork
                    )
                    audio.tags["APIC"] = apic
                except Exception:
                    # Artwork embedding failed, but continue
                    pass
            
            audio.save()
            return True
        except Exception as e:
            return False
    
    def normalize_tags(self, tags: Dict[str, str]) -> Dict[str, str]:
        """Normalize tag keys and values."""
        normalized = {}
        for key, value in tags.items():
            key_lower = key.lower()
            # Handle common variations
            if key_lower == "date" or key_lower == "year":
                # Prefer "date" for ID3 TDRC
                if "date" not in normalized:
                    normalized["date"] = str(value).strip()
            elif key_lower in self.TAG_MAP:
                normalized[key_lower] = str(value).strip()
            else:
                # Keep other tags as-is
                normalized[key_lower] = str(value).strip()
        return normalized

