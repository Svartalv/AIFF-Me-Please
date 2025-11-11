"""Simple Tkinter GUI for FLAC2AIFF converter."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import subprocess
import os


class FLAC2AIFFApp:
    """Main application GUI."""
    
    def __init__(self, root: tk.Tk):
        """Initialize GUI."""
        self.root = root
        self.root.title("FLAC2AIFF for CDJ")
        self.root.geometry("700x300")
        self.root.resizable(True, False)
        
        # State
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.is_converting = False
        
        self._build_ui()
    
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
        
        # Status area
        self.status_label = ttk.Label(
            main_frame,
            text="Ready - Select input folder to begin",
            foreground="gray",
            font=("", 10)
        )
        self.status_label.grid(row=row, column=0, columnspan=3, pady=15)
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
            # Files selected - use their parent directory
            file_paths = [Path(f) for f in files]
            if file_paths:
                # Get common parent directory
                common_parent = file_paths[0].parent
                # Check if all files are in same directory
                if all(p.parent == common_parent for p in file_paths):
                    folder_path = common_parent
                else:
                    folder_path = file_paths[0].parent
                    messagebox.showinfo(
                        "Note",
                        f"Selected files are in different folders. Using: {folder_path}\n\n"
                        f"All audio files in this folder will be converted."
                    )
                
                self.input_dir.set(str(folder_path))
                
                # Count audio files in the folder
                try:
                    audio_files = list(folder_path.glob("*.flac")) + list(folder_path.glob("*.mp3"))
                    count = len(audio_files)
                    if count > 0:
                        self.status_label.config(
                            text=f"Found {count} audio file(s) in folder",
                            foreground="green"
                        )
                    else:
                        self.status_label.config(
                            text="Folder selected",
                            foreground="gray"
                        )
                except Exception:
                    self.status_label.config(
                        text="Folder selected",
                        foreground="gray"
                    )
                
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
                
                # Count audio files
                try:
                    audio_files = list(folder_path.rglob("*.flac")) + list(folder_path.rglob("*.mp3"))
                    count = len(audio_files)
                    if count > 0:
                        self.status_label.config(
                            text=f"Found {count} audio file(s) in folder",
                            foreground="green"
                        )
                    else:
                        self.status_label.config(
                            text="No audio files found in selected folder",
                            foreground="orange"
                        )
                except Exception:
                    self.status_label.config(
                        text="Folder selected",
                        foreground="gray"
                    )
                
                # Auto-set output folder if empty
                if not self.output_dir.get():
                    output_path = folder_path.parent / f"{folder_path.name}_AIFF"
                    self.output_dir.set(str(output_path))
    
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
        
        # Find audio files (FLAC and MP3)
        audio_files = list(input_path.rglob("*.flac")) + list(input_path.rglob("*.mp3"))
        if not audio_files:
            messagebox.showwarning("No Files", "No FLAC or MP3 files found in the input folder")
            return
        
        # Check ffmpeg
        ffmpeg_path = self._find_ffmpeg()
        try:
            subprocess.run([ffmpeg_path, "-version"], capture_output=True, check=True, timeout=5)
        except Exception as e:
            messagebox.showerror(
                "FFmpeg Not Found",
                f"FFmpeg is required but not found.\n\n"
                f"Please install: brew install ffmpeg\n\n"
                f"Error: {str(e)}"
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
                # Generate output filename (same name, .aiff extension)
                output_filename = audio_path.stem + ".aiff"
                output_path = output_dir / output_filename
                
                # Handle collisions
                counter = 1
                while output_path.exists():
                    output_path = output_dir / f"{audio_path.stem} ({counter}).aiff"
                    counter += 1
                
                # Update status
                self.root.after(0, lambda f=audio_path.name, c=i, t=len(audio_files): 
                    self.status_label.config(
                        text=f"Converting: {f} ({c}/{t})",
                        foreground="black"
                    ))
                
                # Convert with ffmpeg (24-bit, 44.1kHz, stereo)
                cmd = [
                    ffmpeg_path,
                    "-i", str(audio_path),
                    "-ar", "44100",
                    "-ac", "2",
                    "-sample_fmt", "s24",
                    "-f", "aiff",
                    "-y",
                    str(output_path)
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0 and output_path.exists():
                    converted += 1
                else:
                    failed += 1
                    
            except Exception as e:
                failed += 1
        
        # Update UI
        self.root.after(0, lambda: self._conversion_complete(converted, failed, len(flac_files)))
    
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
