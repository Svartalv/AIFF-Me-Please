"""Simple Tkinter GUI for FLAC2AIFF converter."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import subprocess
import os
import re
import mutagen
from mutagen.flac import FLAC
from mutagen.mp3 import MP3


class FLAC2AIFFApp:
    """Main application GUI."""
    
    def __init__(self, root: tk.Tk):
        """Initialize GUI."""
        self.root = root
        self.root.title("FLAC2AIFF for CDJ")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Configure dark theme colors
        self.bg_color = "#1a1a1a"  # Dark gray/black
        self.fg_color = "#ffffff"  # White text
        self.accent_color = "#4a9eff"  # Blue accent
        self.secondary_bg = "#2d2d2d"  # Slightly lighter for inputs
        self.border_color = "#404040"  # Border color
        
        # Configure root background
        self.root.configure(bg=self.bg_color)
        
        # State
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.selected_files = []  # Track selected files
        self.file_list_data = []  # List of (input_file, output_name, status)
        self.is_converting = False
        
        self._build_ui()
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename - remove ALL non-ASCII and special characters.
        
        CDJ-safe whitelist (ONLY these allowed):
        - Basic ASCII letters: A-Z, a-z
        - Numbers: 0-9
        - Space
        - Minimal safe punctuation: - _ ( )
        
        Everything else is REMOVED:
        - Emojis (🕊️, etc.)
        - Accented characters (é, ä, ø, etc.)
        - Fancy Unicode (𝓶, etc.)
        - All special symbols: [ ] { } , . ' + & / \ : * ? " < > | % #
        - Control characters
        """
        if not filename:
            return "Unknown"
        
        # Strict whitelist: ONLY ASCII letters, numbers, space, and: - _ ( )
        sanitized = ""
        for char in filename:
            # Check if character is basic ASCII letter (A-Z, a-z)
            if ('A' <= char <= 'Z') or ('a' <= char <= 'z'):
                sanitized += char
            # Check if character is number (0-9)
            elif '0' <= char <= '9':
                sanitized += char
            # Allow space
            elif char == ' ':
                sanitized += ' '
            # Allow only these safe punctuation marks
            elif char in "-_()":
                sanitized += char
            # EVERYTHING ELSE IS REMOVED (emojis, Unicode, special chars, etc.)
        
        # Collapse multiple spaces into single space
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        # Trim spaces at start and end
        sanitized = sanitized.strip()
        
        # Remove trailing dots, spaces, dashes, underscores
        sanitized = sanitized.rstrip('. -_')
        
        # Ensure it doesn't start with a dot, dash, or underscore
        sanitized = sanitized.lstrip('.-_')
        
        # Remove any remaining problematic patterns
        # Remove multiple dashes/underscores
        sanitized = re.sub(r'[-_]{2,}', '-', sanitized)
        
        # If empty after sanitization, use fallback
        if not sanitized:
            sanitized = "Unknown"
        
        # Final check: ensure no forbidden characters remain
        # This is a safety check - should already be clean
        final = ""
        for char in sanitized:
            if (('A' <= char <= 'Z') or ('a' <= char <= 'z') or 
                ('0' <= char <= '9') or char == ' ' or char in "-_()"):
                final += char
        sanitized = final.strip() or "Unknown"
        
        return sanitized
    
    def _get_tags_from_file(self, file_path: Path) -> dict:
        """Extract tags from audio file."""
        tags = {}
        try:
            if file_path.suffix.lower() == '.flac':
                audio = FLAC(str(file_path))
            elif file_path.suffix.lower() == '.mp3':
                audio = MP3(str(file_path))
            else:
                return tags
            
            # Common tag fields
            tag_fields = {
                'artist': ['artist', 'ARTIST', 'TPE1'],
                'title': ['title', 'TITLE', 'TIT2'],
                'album': ['album', 'ALBUM', 'TALB'],
                'label': ['label', 'LABEL', 'TPUB', 'organization', 'ORGANIZATION'],
                'year': ['year', 'YEAR', 'date', 'DATE', 'TDRC'],
                'tracknumber': ['tracknumber', 'TRACKNUMBER', 'TRACK', 'TRCK'],
            }
            
            for key, possible_fields in tag_fields.items():
                for field in possible_fields:
                    if field in audio:
                        value = audio[field]
                        if isinstance(value, list) and value:
                            tags[key] = str(value[0]).strip()
                            break
                    # Try lowercase
                    field_lower = field.lower()
                    for tag_key in audio.keys():
                        if tag_key.lower() == field_lower:
                            value = audio[tag_key]
                            if isinstance(value, list) and value:
                                tags[key] = str(value[0]).strip()
                                break
                    if key in tags:
                        break
        except Exception:
            pass
        
        return tags
    
    def _build_filename_from_tags(self, file_path: Path, tags: dict) -> str:
        """Build filename from tags using template: Artist - Title."""
        artist = tags.get('artist', '').strip()
        title = tags.get('title', '').strip()
        
        # Fallback to original filename if tags missing
        if not artist and not title:
            return file_path.stem
        
        # Build filename: "Artist - Title"
        if artist and title:
            filename = f"{artist} - {title}"
        elif artist:
            filename = artist
        elif title:
            filename = title
        else:
            filename = file_path.stem
        
        # Sanitize the filename
        filename = self._sanitize_filename(filename)
        
        return filename
    
    def _build_ui(self) -> None:
        """Build the user interface."""
        main_frame = ttk.Frame(self.root, padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="FLAC2AIFF for CDJ",
            font=("", 18, "bold")
        )
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 30))
        row += 1
        
        # Input folder
        ttk.Label(main_frame, text="Input folder:", font=("", 12)).grid(
            row=row, column=0, sticky=tk.W, pady=12
        )
        input_entry = ttk.Entry(main_frame, textvariable=self.input_dir, width=55, font=("", 10))
        input_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=12, pady=12)
        ttk.Button(
            main_frame,
            text="Choose...",
            command=self._select_input_folder,
            width=12
        ).grid(row=row, column=2, padx=5, pady=12)
        row += 1
        
        # Output folder
        ttk.Label(main_frame, text="Output folder:", font=("", 12)).grid(
            row=row, column=0, sticky=tk.W, pady=12
        )
        output_entry = ttk.Entry(main_frame, textvariable=self.output_dir, width=55, font=("", 10))
        output_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=12, pady=12)
        ttk.Button(
            main_frame,
            text="Choose...",
            command=self._select_output_folder,
            width=12
        ).grid(row=row, column=2, padx=5, pady=12)
        row += 1
        
        # File list with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create treeview for file list
        columns = ("input", "output", "status")
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        self.file_tree.heading("input", text="Input File")
        self.file_tree.heading("output", text="Output Name")
        self.file_tree.heading("status", text="Status")
        self.file_tree.column("input", width=250)
        self.file_tree.column("output", width=250)
        self.file_tree.column("status", width=100)
        
        # Scrollbar for file list
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        self.file_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        row += 1
        
        # Status area
        self.status_label = ttk.Label(
            main_frame,
            text="Ready - Select files to convert",
            foreground="gray",
            font=("", 10)
        )
        self.status_label.grid(row=row, column=0, columnspan=3, pady=10)
        row += 1
        
        # Start button
        self.start_button = ttk.Button(
            main_frame,
            text="Start Conversion",
            command=self._start_conversion,
            width=25
        )
        self.start_button.grid(row=row, column=0, columnspan=3, pady=15)
    
    def _select_input_folder(self) -> None:
        """Select input files or folder."""
        # Allow selecting files (FLAC or MP3)
        files = filedialog.askopenfilenames(
            title="Select FLAC or MP3 files (or cancel to select folder)",
            filetypes=[
                ("Audio files", "*.flac *.mp3"),
                ("FLAC files", "*.flac"),
                ("MP3 files", "*.mp3"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            # Files selected - store them and use their parent directory
            file_paths = [Path(f) for f in files]
            self.selected_files = file_paths  # Store selected files
            
            if file_paths:
                # Get common parent directory
                common_parent = file_paths[0].parent
                # Check if all files are in same directory
                if all(p.parent == common_parent for p in file_paths):
                    folder_path = common_parent
                else:
                    folder_path = file_paths[0].parent
                
                self.input_dir.set(str(folder_path))
                
                # Show count of selected files and build file list
                count = len(file_paths)
                self.status_label.config(
                    text=f"Selected {count} file(s) to convert",
                    foreground="green"
                )
                
                # Build file list preview
                self._update_file_list(file_paths)
                
                # Auto-set output folder if empty
                if not self.output_dir.get():
                    output_path = folder_path.parent / f"{folder_path.name}_AIFF"
                    self.output_dir.set(str(output_path))
        else:
            # No files selected - fallback to folder selection
            folder = filedialog.askdirectory(title="Select input folder containing audio files")
            if folder:
                folder_path = Path(folder)
                if not folder_path.exists() or not folder_path.is_dir():
                    messagebox.showerror("Error", f"Invalid folder:\n{folder}")
                    return
                
                self.input_dir.set(str(folder_path))
                # When folder is selected, find all audio files in it
                try:
                    audio_files = list(folder_path.rglob("*.flac")) + list(folder_path.rglob("*.mp3"))
                    self.selected_files = audio_files  # Store all found files
                    count = len(audio_files)
                    if count > 0:
                        self.status_label.config(
                            text=f"Found {count} audio file(s) in folder",
                            foreground="green"
                        )
                        # Build file list preview
                        self._update_file_list(audio_files)
                    else:
                        self.status_label.config(
                            text="No audio files found in selected folder",
                            foreground="orange"
                        )
                        self.selected_files = []
                        self._clear_file_list()
                except Exception:
                    self.status_label.config(
                        text="Folder selected",
                        foreground="gray"
                    )
                    self.selected_files = []
                    self._clear_file_list()
                
                # Auto-set output folder if empty
                if not self.output_dir.get():
                    output_path = folder_path.parent / f"{folder_path.name}_AIFF"
                    self.output_dir.set(str(output_path))
    
    def _clear_file_list(self) -> None:
        """Clear the file list display."""
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        self.file_list_data = []
    
    def _update_file_list(self, files: list) -> None:
        """Update the file list display with selected files and their output names."""
        # Clear existing items
        self._clear_file_list()
        
        # Build list data
        self.file_list_data = []
        for file_path in files:
            # Get tags and build output name (already sanitized)
            tags = self._get_tags_from_file(file_path)
            output_name = self._build_filename_from_tags(file_path, tags) + ".aiff"
            
            # Store data
            self.file_list_data.append({
                'input': file_path,
                'output': output_name,
                'status': 'Pending'
            })
            
            # Add to treeview - show full names but truncate for display
            input_display = file_path.name
            if len(input_display) > 45:
                input_display = input_display[:42] + "..."
            
            output_display = output_name
            if len(output_display) > 45:
                output_display = output_display[:42] + "..."
            
            self.file_tree.insert("", tk.END, values=(input_display, output_display, "Pending"))
    
    def _update_file_status(self, index: int, status: str) -> None:
        """Update status of a file in the list."""
        if 0 <= index < len(self.file_list_data):
            self.file_list_data[index]['status'] = status
            # Update treeview
            items = list(self.file_tree.get_children())
            if 0 <= index < len(items):
                item = items[index]
                current_values = list(self.file_tree.item(item, 'values'))
                if len(current_values) >= 3:
                    current_values[2] = status
                    self.file_tree.item(item, values=tuple(current_values))
    
    def _select_output_folder(self) -> None:
        """Select output folder."""
        folder = filedialog.askdirectory(title="Select output folder for converted AIFF files")
        if folder:
            folder_path = Path(folder)
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
                self.output_dir.set(str(folder_path))
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create output folder:\n{str(e)}")
    
    def _find_ffmpeg(self) -> str:
        """Find ffmpeg binary."""
        # Try common locations first
        common_paths = [
            "/opt/homebrew/bin/ffmpeg",  # Apple Silicon Homebrew
            "/usr/local/bin/ffmpeg",     # Intel Homebrew
            "/usr/bin/ffmpeg",           # System
        ]
        
        for path in common_paths:
            if Path(path).exists():
                return path
        
        # Try system PATH
        try:
            result = subprocess.run(["which", "ffmpeg"], capture_output=True, check=True, timeout=2)
            path = result.stdout.decode().strip()
            if path:
                return path
        except:
            pass
        
        # Try bundled location
        script_dir = Path(__file__).parent.parent
        bundled = script_dir / "resources" / "ffmpeg" / "ffmpeg"
        if bundled.exists():
            return str(bundled)
        
        return "ffmpeg"  # Fallback
    
    def _start_conversion(self) -> None:
        """Start conversion process."""
        # Validate inputs
        input_path_str = self.input_dir.get().strip()
        if not input_path_str:
            messagebox.showerror("Error", "Please select an input folder")
            return
        
        input_path = Path(input_path_str)
        if not input_path.exists() or not input_path.is_dir():
            messagebox.showerror("Error", f"Input folder does not exist:\n{input_path}")
            return
        
        output_path_str = self.output_dir.get().strip()
        if not output_path_str:
            messagebox.showerror("Error", "Please select an output folder")
            return
        
        output_path = Path(output_path_str)
        try:
            output_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot create output directory:\n{str(e)}")
            return
        
        # Use selected files if available, otherwise find all in folder
        if self.selected_files:
            audio_files = self.selected_files
        else:
            audio_files = list(input_path.rglob("*.flac")) + list(input_path.rglob("*.mp3"))
        
        if not audio_files:
            messagebox.showwarning("No Files", "No files selected or found in the input folder")
            return
        
        # Check ffmpeg
        ffmpeg_path = self._find_ffmpeg()
        try:
            result = subprocess.run(
                [ffmpeg_path, "-version"],
                capture_output=True,
                check=True,
                timeout=5
            )
            if result.returncode != 0:
                raise Exception("ffmpeg returned non-zero exit code")
        except FileNotFoundError:
            messagebox.showerror(
                "FFmpeg Not Found",
                f"FFmpeg is required but not found.\n\n"
                f"Please install ffmpeg:\n"
                f"  brew install ffmpeg\n\n"
                f"Or download from: https://evermeet.cx/ffmpeg/\n\n"
                f"Then restart the app."
            )
            return
        except Exception as e:
            messagebox.showerror(
                "FFmpeg Error",
                f"FFmpeg found but not working.\n\n"
                f"Path: {ffmpeg_path}\n"
                f"Error: {str(e)}\n\n"
                f"Please check your ffmpeg installation."
            )
            return
        
        # Disable start button
        self.start_button.config(state=tk.DISABLED)
        self.is_converting = True
        self.status_label.config(text=f"Converting {len(audio_files)} file(s)...", foreground="black")
        
        # Run conversion in thread
        thread = threading.Thread(
            target=self._convert_files,
            args=(audio_files, output_path, ffmpeg_path),
            daemon=True
        )
        thread.start()
    
    def _convert_files(self, audio_files: list, output_dir: Path, ffmpeg_path: str) -> None:
        """Convert audio files (FLAC/MP3) to AIFF."""
        converted = 0
        failed = 0
        
        for i, audio_path in enumerate(audio_files, 1):
            try:
                # Get tags from file
                tags = self._get_tags_from_file(audio_path)
                
                # Build filename from tags
                clean_name = self._build_filename_from_tags(audio_path, tags)
                output_filename = clean_name + ".aiff"
                output_path = output_dir / output_filename
                
                # Handle collisions - sanitize the collision number too
                counter = 1
                original_output = output_path
                while output_path.exists():
                    collision_name = self._sanitize_filename(f"{clean_name} ({counter})")
                    output_path = output_dir / f"{collision_name}.aiff"
                    counter += 1
                
                # Update file status in list
                self.root.after(0, lambda idx=i-1: self._update_file_status(idx, "Converting"))
                
                # Update main status
                self.root.after(0, lambda c=i, t=len(audio_files): 
                    self.status_label.config(
                        text=f"Converting {c} of {t} files...",
                        foreground="black"
                    ))
                
                # Convert with ffmpeg (16-bit, 44.1kHz, stereo)
                # Use 16-bit for maximum compatibility (CDJ standard)
                # Preserve all metadata
                cmd = [
                    ffmpeg_path,
                    "-i", str(audio_path),
                    "-ar", "44100",              # 44.1kHz sample rate
                    "-ac", "2",                  # Stereo
                    "-c:a", "pcm_s16be",         # 16-bit PCM big-endian (AIFF format, CDJ compatible)
                    "-map_metadata", "0",         # Copy all metadata from input
                    "-map", "0:a",               # Map all audio streams
                    "-f", "aiff",                # AIFF format
                    "-y",                        # Overwrite if exists
                    str(output_path)
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0:
                    converted += 1
                    # Update status to success
                    self.root.after(0, lambda idx=i-1: self._update_file_status(idx, "Done"))
                else:
                    failed += 1
                    error_msg = result.stderr[-200:] if result.stderr else "Unknown error"
                    print(f"Failed to convert {audio_path.name}: {error_msg}")
                    # Update status to failed
                    self.root.after(0, lambda idx=i-1: self._update_file_status(idx, "Failed"))
                    
            except Exception as e:
                failed += 1
        
        # Update UI
        self.root.after(0, lambda: self._conversion_complete(converted, failed, len(audio_files)))
    
    def _conversion_complete(self, converted: int, failed: int, total: int) -> None:
        """Handle conversion completion."""
        self.is_converting = False
        self.start_button.config(state=tk.NORMAL)
        
        if converted > 0:
            self.status_label.config(
                text=f"Complete! Converted {converted} of {total} file(s)",
                foreground="green"
            )
            messagebox.showinfo(
                "Conversion Complete",
                f"Converted: {converted}\n"
                f"Failed: {failed}\n"
                f"Total: {total}"
            )
        else:
            self.status_label.config(
                text="Conversion failed",
                foreground="red"
            )
            messagebox.showerror("Error", f"Failed to convert files. Check that ffmpeg is installed.")


def main():
    """Main entry point for GUI."""
    root = tk.Tk()
    app = FLAC2AIFFApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
