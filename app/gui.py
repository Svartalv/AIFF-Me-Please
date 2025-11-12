"""Simple Tkinter GUI for AIFF Me Please converter."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import subprocess
import os
import re
import sys

# Try to import mutagen
try:
    import mutagen
    from mutagen.flac import FLAC
    from mutagen.mp3 import MP3
except ImportError:
    print("Error: mutagen is not installed. Please run: pip3 install --user mutagen")
    sys.exit(1)

# Pillow/PIL is NOT used - it causes macOS version compatibility issues
# The app works perfectly without it (just no icon display)
HAS_PIL = False


class FLAC2AIFFApp:
    """Main application GUI."""
    
    def __init__(self, root: tk.Tk):
        """Initialize GUI."""
        self.root = root
        self.root.title("AIFF Me Please")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Configure dark theme colors - Cursor-style
        self.bg_color = "#1e1e1e"  # Cursor background
        self.fg_color = "#cccccc"  # Light gray text (readable)
        self.accent_color = "#0d0d0d"  # Very dark grey buttons (almost black)
        self.secondary_bg = "#252526"  # Input fields (darker)
        self.border_color = "#3e3e42"  # Subtle borders
        self.hover_color = "#1a1a1a"  # Slightly lighter hover
        self.button_text = "#ffffff"  # White text on buttons for readability
        self.icon_image = None  # Store icon for messageboxes
        
        # Configure root background
        self.root.configure(bg=self.bg_color)
        
        # Set app icon if available
        self._set_app_icon()
        
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
    
    def _set_app_icon(self) -> None:
        """Set the application icon."""
        try:
            # Try to load icon - check multiple locations and formats
            base_path = Path(__file__).parent.parent
            app_path = Path(__file__).parent
            current_dir = Path.cwd()
            
            icon_paths = [
                app_path / "aiffmeplease.png",  # Primary icon location
                current_dir / "app" / "aiffmeplease.png",  # From project root
                base_path / "app" / "aiffmeplease.png",  # Alternative
                base_path / "resources" / "aiffmeplease.png",
                base_path / "resources" / "icon.png",
            ]
            
            for icon_path in icon_paths:
                abs_path = icon_path.resolve() if icon_path.exists() else None
                if icon_path.exists() or (abs_path and abs_path.exists()):
                    try:
                        actual_path = abs_path if abs_path else icon_path
                        if actual_path.suffix in [".png", ".jpg", ".jpeg"] and HAS_PIL:
                            # For image files, use PhotoImage
                            img = Image.open(actual_path)
                            # Convert to RGBA if needed
                            if img.mode != 'RGBA':
                                img = img.convert('RGBA')
                            # Resize to appropriate size for icon
                            img = img.resize((256, 256), Image.Resampling.LANCZOS)
                            photo = ImageTk.PhotoImage(img)
                            self.root.iconphoto(True, photo)
                            # Keep reference to prevent garbage collection
                            self.root.icon_image = photo
                            self.icon_image = photo  # Store for messageboxes
                            print(f"✓ Loaded app icon from {actual_path}")
                            return
                        elif actual_path.suffix == ".icns":
                            # For macOS .icns files, use iconbitmap
                            self.root.iconbitmap(str(actual_path))
                            print(f"✓ Loaded app icon from {actual_path}")
                            return
                    except Exception as e:
                        print(f"Error loading icon from {icon_path}: {e}")
                        import traceback
                        traceback.print_exc()
                        continue
            
            # If no icon found, print helpful message
            print(f"No icon file found. Checked: {[str(p) for p in icon_paths]}")
        except Exception as e:
            # If icon loading fails, continue without icon
            print(f"Could not load app icon: {e}")
            import traceback
            traceback.print_exc()
    
    def _build_ui(self) -> None:
        """Build the user interface."""
        # Main container with dark background
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=30, pady=30)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Title with modern styling - Cursor style
        title_label = tk.Label(
            main_frame,
            text="Convert your audio files to AIFF",
            font=("SF Pro Display", 22, "normal"),
            bg=self.bg_color,
            fg="#ffffff"  # Bright white for title
        )
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 50))
        row += 1
        
        # Input folder - Cursor style
        input_label = tk.Label(
            main_frame,
            text="Input folder:",
            font=("SF Pro Text", 11, "normal"),
            bg=self.bg_color,
            fg=self.fg_color  # Readable gray
        )
        input_label.grid(row=row, column=0, sticky=tk.W, pady=12)
        
        input_entry = tk.Entry(
            main_frame,
            textvariable=self.input_dir,
            font=("SF Pro Text", 10, "normal"),
            bg=self.secondary_bg,
            fg="#ffffff",  # White text for readability
            insertbackground="#ffffff",
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.border_color,
            highlightcolor="#007acc"  # Blue focus (Cursor style)
        )
        input_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=15, pady=12, ipady=8)
        
        # Use ttk.Button with dark style for macOS compatibility
        input_button = ttk.Button(
            main_frame,
            text="Choose",
            command=self._select_input_folder,
            style="Dark.TButton"
        )
        input_button.grid(row=row, column=2, padx=5, pady=12)
        row += 1
        
        # Output folder - Cursor style
        output_label = tk.Label(
            main_frame,
            text="Output folder:",
            font=("SF Pro Text", 11, "normal"),
            bg=self.bg_color,
            fg=self.fg_color  # Readable gray
        )
        output_label.grid(row=row, column=0, sticky=tk.W, pady=12)
        
        output_entry = tk.Entry(
            main_frame,
            textvariable=self.output_dir,
            font=("SF Pro Text", 10, "normal"),
            bg=self.secondary_bg,
            fg="#ffffff",  # White text for readability
            insertbackground="#ffffff",
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.border_color,
            highlightcolor="#007acc"  # Blue focus (Cursor style)
        )
        output_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=15, pady=12, ipady=8)
        
        # Use ttk.Button with dark style for macOS compatibility
        output_button = ttk.Button(
            main_frame,
            text="Choose",
            command=self._select_output_folder,
            style="Dark.TButton"
        )
        output_button.grid(row=row, column=2, padx=5, pady=12)
        row += 1
        
        # File list with scrollbar
        list_frame = tk.Frame(main_frame, bg=self.bg_color)
        list_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=20)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(row, weight=1)
        
        # Create treeview for file list with dark theme
        columns = ("input", "output", "status")
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure dark button style for macOS compatibility
        style.configure("Dark.TButton",
            background="#0d0d0d",
            foreground="#ffffff",
            borderwidth=0,
            focuscolor="none",
            padding=10
        )
        style.map("Dark.TButton",
            background=[("active", "#1a1a1a"), ("!disabled", "#0d0d0d")],
            foreground=[("active", "#ffffff"), ("!disabled", "#ffffff")]
        )
        
        # Configure treeview style - Cursor style
        style.configure("Treeview",
            background=self.secondary_bg,
            foreground="#cccccc",  # Readable text
            fieldbackground=self.secondary_bg,
            borderwidth=1,
            bordercolor=self.border_color,
            font=("SF Pro Text", 10, "normal")
        )
        style.configure("Treeview.Heading",
            background=self.bg_color,
            foreground="#cccccc",  # Readable headers
            borderwidth=1,
            bordercolor=self.border_color,
            relief=tk.FLAT,
            font=("SF Pro Text", 10, "normal")
        )
        style.map("Treeview",
            background=[("selected", "#094771")],  # Blue selection (Cursor style)
            foreground=[("selected", "#ffffff")]
        )
        
        # Configure scrollbar - Hide it completely (minimal design)
        style.configure("Vertical.TScrollbar",
            background=self.bg_color,
            troughcolor=self.bg_color,
            borderwidth=0,
            arrowcolor=self.bg_color,
            darkcolor=self.bg_color,
            lightcolor=self.bg_color,
            width=0  # Make it invisible
        )
        
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        self.file_tree.heading("input", text="Input File")
        self.file_tree.heading("output", text="Output Name")
        self.file_tree.heading("status", text="Status")
        self.file_tree.column("input", width=300)
        self.file_tree.column("output", width=300)
        self.file_tree.column("status", width=120)
        
        # Scrollbar for file list - hidden (minimal design)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_tree.yview, style="Vertical.TScrollbar")
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        self.file_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Don't show scrollbar - hide it completely
        # scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        row += 1
        
        # Status area - Cursor style
        self.status_label = tk.Label(
            main_frame,
            text="Ready - Select files to convert",
            font=("SF Pro Text", 10, "normal"),
            bg=self.bg_color,
            fg="#858585"  # Readable gray (Cursor status style)
        )
        self.status_label.grid(row=row, column=0, columnspan=3, pady=20)
        row += 1
        
        # Start button - Use ttk.Button with dark style for macOS compatibility
        self.start_button = ttk.Button(
            main_frame,
            text="Start Conversion",
            command=self._start_conversion,
            style="Dark.TButton"
        )
        self.start_button.grid(row=row, column=0, columnspan=3, pady=25)
    
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
                    fg="#89d185"  # Cursor green
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
                            fg="#89d185"  # Cursor green
                        )
                        # Build file list preview
                        self._update_file_list(audio_files)
                    else:
                        self.status_label.config(
                            text="No audio files found in selected folder",
                            fg="#dcdcaa"  # Cursor yellow/warning
                        )
                        self.selected_files = []
                        self._clear_file_list()
                except Exception:
                    self.status_label.config(
                        text="Folder selected",
                        fg="#aaaaaa"  # Gray
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
            
            # Sanitize display text to avoid TclError with Unicode characters
            # Only allow ASCII for display in Treeview
            def safe_display(text: str, max_len: int = 45) -> str:
                """Convert to safe ASCII for Treeview display."""
                safe = ""
                for char in text:
                    # Only allow ASCII printable characters
                    if 32 <= ord(char) <= 126:  # Printable ASCII
                        safe += char
                    elif char == '\n' or char == '\t':
                        safe += ' '
                    # Skip all other characters (Unicode, emojis, etc.)
                safe = safe.strip()
                if len(safe) > max_len:
                    safe = safe[:max_len-3] + "..."
                return safe or "Unknown"
            
            # Add to treeview - sanitize for display
            input_display = safe_display(file_path.name)
            output_display = safe_display(output_name)
            
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
                    # Sanitize status text for display
                    safe_status = ""
                    for char in status:
                        if 32 <= ord(char) <= 126:  # Printable ASCII
                            safe_status += char
                    safe_status = safe_status or status[:10]  # Fallback
                    current_values[2] = safe_status
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
        
        # Disable start button - Cursor style disabled state
        self.start_button.config(state=tk.DISABLED)
        style.configure("Dark.TButton",
            background="#0d0d0d",
            foreground="#666666"  # Darker gray when disabled
        )
        self.is_converting = True
        self.status_label.config(text=f"Converting {len(audio_files)} file(s)...", fg=self.fg_color)
        
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
                        fg=self.fg_color
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
                error_msg = str(e)[:200] if str(e) else "Unknown error"
                print(f"Exception converting {audio_path.name}: {error_msg}")
                # Update status to failed
                self.root.after(0, lambda idx=i-1: self._update_file_status(idx, "Failed"))
        
        # Update UI
        self.root.after(0, lambda: self._conversion_complete(converted, failed, len(audio_files)))
    
    def _show_custom_message(self, title: str, message: str, msg_type: str = "info") -> None:
        """Show custom messagebox with cat icon."""
        # Create custom dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set icon if available
        if self.icon_image:
            dialog.iconphoto(True, self.icon_image)
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg=self.bg_color, padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon and message frame
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cat icon
        if self.icon_image:
            icon_label = tk.Label(
                content_frame,
                image=self.icon_image,
                bg=self.bg_color
            )
            icon_label.pack(pady=(0, 15))
        
        # Message text
        msg_label = tk.Label(
            content_frame,
            text=message,
            font=("SF Pro Text", 11, "normal"),
            bg=self.bg_color,
            fg=self.fg_color,
            justify=tk.LEFT
        )
        msg_label.pack(pady=10)
        
        # OK button
        ok_button = tk.Button(
            main_frame,
            text="OK",
            command=dialog.destroy,
            font=("SF Pro Text", 11, "normal"),
            bg=self.accent_color,  # Dark grey button
            fg="#ffffff",
            activebackground=self.hover_color,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            padx=40,
            pady=10,
            cursor="hand2"
        )
        ok_button.pack(pady=(20, 0))
        
        # Make dialog modal
        dialog.wait_window()
    
    def _conversion_complete(self, converted: int, failed: int, total: int) -> None:
        """Handle conversion completion."""
        self.is_converting = False
        self.start_button.config(state=tk.NORMAL)
        style.configure("Dark.TButton",
            background="#0d0d0d",
            foreground="#ffffff"  # White text when enabled
        )
        
        if converted > 0:
            self.status_label.config(
                text=f"Complete! Converted {converted} of {total} file(s)",
                fg="#89d185"  # Cursor green for success
            )
            # Custom messagebox with cat icon
            self._show_custom_message(
                "Conversion Complete",
                f"Converted: {converted}\n"
                f"Failed: {failed}\n"
                f"Total: {total}",
                "info"
            )
        else:
            self.status_label.config(
                text="Conversion failed",
                fg="#f48771"  # Cursor red/orange for error
            )
            # Custom messagebox with cat icon
            self._show_custom_message(
                "Error",
                f"Failed to convert files. Check that ffmpeg is installed.",
                "error"
            )


def main():
    """Main entry point for GUI."""
    root = tk.Tk()
    app = FLAC2AIFFApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
