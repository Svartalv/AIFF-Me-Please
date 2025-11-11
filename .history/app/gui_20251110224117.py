"""Tkinter GUI for FLAC2AIFF converter."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Optional
import threading
import os

from .config import Config
from .logging_utils import ConversionLogger
from .engine import ConversionEngine


class FLAC2AIFFApp:
    """Main application GUI."""
    
    def __init__(self, root: tk.Tk):
        """Initialize GUI."""
        self.root = root
        self.root.title("FLAC2AIFF for CDJ")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Configuration
        self.config = Config()
        
        # State
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.bit_depth_var = tk.IntVar(value=self.config.bit_depth)
        self.sample_rate_var = tk.IntVar(value=self.config.sample_rate)
        self.embed_artwork_var = tk.BooleanVar(value=self.config.embed_artwork)
        self.overwrite_var = tk.BooleanVar(value=self.config.overwrite)
        self.concurrency_var = tk.IntVar(value=self.config.concurrency)
        self.filename_template_var = tk.StringVar(value=self.config.filename_template)
        
        self.engine: Optional[ConversionEngine] = None
        self.logger: Optional[ConversionLogger] = None
        self.is_converting = False
        
        self._build_ui()
    
    def _build_ui(self) -> None:
        """Build the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="FLAC2AIFF for CDJ",
            font=("", 16, "bold")
        )
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 20))
        row += 1
        
        # Input folder
        ttk.Label(main_frame, text="Input folder:").grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.input_dir, width=50).grid(
            row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=5
        )
        ttk.Button(
            main_frame,
            text="Choose...",
            command=self._select_input_folder
        ).grid(row=row, column=2, padx=5, pady=5)
        row += 1
        
        # Output folder
        ttk.Label(main_frame, text="Output folder:").grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.output_dir, width=50).grid(
            row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=5
        )
        ttk.Button(
            main_frame,
            text="Choose...",
            command=self._select_output_folder
        ).grid(row=row, column=2, padx=5, pady=5)
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10
        )
        row += 1
        
        # Audio settings
        settings_label = ttk.Label(
            main_frame,
            text="Audio Settings",
            font=("", 12, "bold")
        )
        settings_label.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        row += 1
        
        # Bit depth
        bit_frame = ttk.Frame(main_frame)
        bit_frame.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        ttk.Label(bit_frame, text="Bit depth:").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            bit_frame,
            text="16-bit",
            variable=self.bit_depth_var,
            value=16
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            bit_frame,
            text="24-bit",
            variable=self.bit_depth_var,
            value=24
        ).pack(side=tk.LEFT, padx=5)
        row += 1
        
        # Sample rate
        ttk.Label(main_frame, text="Sample rate:").grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        sample_frame = ttk.Frame(main_frame)
        sample_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Label(sample_frame, text="44.1 kHz (recommended)").pack(side=tk.LEFT)
        row += 1
        
        # Options
        ttk.Checkbutton(
            main_frame,
            text="Embed artwork",
            variable=self.embed_artwork_var
        ).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Checkbutton(
            main_frame,
            text="Overwrite existing files",
            variable=self.overwrite_var
        ).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1
        
        # Concurrency
        ttk.Label(main_frame, text="Max concurrent jobs:").grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        concurrency_spin = ttk.Spinbox(
            main_frame,
            from_=1,
            to=8,
            textvariable=self.concurrency_var,
            width=10
        )
        concurrency_spin.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Filename template
        ttk.Label(main_frame, text="Filename pattern:").grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        template_entry = ttk.Entry(
            main_frame,
            textvariable=self.filename_template_var,
            width=50
        )
        template_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(
            main_frame,
            text="(use {artist}, {title}, {album})",
            font=("", 8)
        ).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10
        )
        row += 1
        
        # Status area
        status_label = ttk.Label(
            main_frame,
            text="Status",
            font=("", 12, "bold")
        )
        status_label.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        row += 1
        
        # Current file
        self.current_file_label = ttk.Label(
            main_frame,
            text="Ready",
            foreground="gray"
        )
        self.current_file_label.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Progress text
        self.progress_text = ttk.Label(
            main_frame,
            text="0 / 0 files",
            foreground="gray"
        )
        self.progress_text.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        
        self.start_button = ttk.Button(
            button_frame,
            text="Start",
            command=self._start_conversion,
            width=15
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._cancel_conversion,
            state=tk.DISABLED,
            width=15
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        self.open_output_button = ttk.Button(
            button_frame,
            text="Open Output",
            command=self._open_output_folder,
            width=15
        )
        self.open_output_button.pack(side=tk.LEFT, padx=5)
        
        self.open_log_button = ttk.Button(
            button_frame,
            text="Open Log",
            command=self._open_log,
            width=15
        )
        self.open_log_button.pack(side=tk.LEFT, padx=5)
    
    def _select_input_folder(self) -> None:
        """Select input folder or files."""
        # First try to let user select files (they can also navigate to a folder)
        selection = filedialog.askopenfilenames(
            title="Select FLAC files (or cancel to select folder)",
            filetypes=[("FLAC files", "*.flac"), ("All files", "*.*")]
        )
        
        if selection:
            # Files selected - use their parent directory
            paths = [Path(f) for f in selection]
            if paths:
                # Get the common parent directory
                common_parent = paths[0].parent
                # Verify all files are in the same directory (or at least use first file's parent)
                if all(p.parent == common_parent for p in paths):
                    folder = str(common_parent)
                else:
                    # Files in different directories - use first file's parent
                    folder = str(paths[0].parent)
                    messagebox.showinfo(
                        "Note",
                        f"Selected files are in different directories. "
                        f"Using folder: {folder}\n\n"
                        f"All FLAC files in this folder will be converted."
                    )
                
                self.input_dir.set(folder)
                # Auto-set output folder if empty
                if not self.output_dir.get():
                    output_path = Path(folder).parent / f"{Path(folder).name}_AIFF"
                    self.output_dir.set(str(output_path))
        else:
            # No files selected - fallback to folder selection
            folder = filedialog.askdirectory(title="Select input folder")
            if folder:
                self.input_dir.set(folder)
                # Auto-set output folder if empty
                if not self.output_dir.get():
                    output_path = Path(folder).parent / f"{Path(folder).name}_AIFF"
                    self.output_dir.set(str(output_path))
    
    def _select_output_folder(self) -> None:
        """Select output folder."""
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_dir.set(folder)
    
    def _update_progress(self, filename: str, current: int, total: int) -> None:
        """Update progress display."""
        self.root.after(0, lambda: self._update_progress_ui(filename, current, total))
    
    def _update_progress_ui(self, filename: str, current: int, total: int) -> None:
        """Update progress UI (called on main thread)."""
        self.current_file_label.config(text=f"Processing: {filename}")
        if total > 0:
            progress = (current / total) * 100
            self.progress_var.set(progress)
            self.progress_text.config(text=f"{current} / {total} files")
    
    def _start_conversion(self) -> None:
        """Start conversion process."""
        # Validate inputs
        input_path_str = self.input_dir.get().strip()
        if not input_path_str:
            messagebox.showerror("Error", "Please select an input folder")
            return
        
        input_path = Path(input_path_str)
        if not input_path.exists():
            messagebox.showerror("Error", f"Input folder does not exist:\n{input_path}")
            return
        
        if not input_path.is_dir():
            messagebox.showerror("Error", f"Input path is not a folder:\n{input_path}")
            return
        
        output_path_str = self.output_dir.get().strip()
        if not output_path_str:
            messagebox.showerror("Error", "Please select an output folder")
            return
        
        output_path = Path(output_path_str)
        # Create parent directory if it doesn't exist
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot create output directory:\n{str(e)}")
            return
        
        # Update config from UI
        self.config.set("bit_depth", self.bit_depth_var.get())
        self.config.set("sample_rate", self.sample_rate_var.get())
        self.config.set("embed_artwork", self.embed_artwork_var.get())
        self.config.set("overwrite", self.overwrite_var.get())
        self.config.set("concurrency", self.concurrency_var.get())
        self.config.set("filename_template", self.filename_template_var.get())
        self.config.save()
        
        # Initialize logger
        self.logger = ConversionLogger(
            str(output_path),
            log_level=self.config.log_level
        )
        
        # Initialize engine
        self.engine = ConversionEngine(
            self.config,
            self.logger,
            progress_callback=self._update_progress
        )
        
        # Disable start button, enable cancel
        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.is_converting = True
        
        # Reset progress
        self.progress_var.set(0)
        self.progress_text.config(text="0 / 0 files")
        self.current_file_label.config(text="Starting conversion...", foreground="black")
        
        # Run conversion in separate thread
        thread = threading.Thread(
            target=self._run_conversion,
            args=(input_path, output_path),
            daemon=True
        )
        thread.start()
    
    def _run_conversion(self, input_path: Path, output_path: Path) -> None:
        """Run conversion (in background thread)."""
        try:
            # Check if ffmpeg is available before starting
            import subprocess
            ffmpeg_path = self.engine.transcoder.ffmpeg_path
            test_cmd = [ffmpeg_path, "-version"]
            try:
                result = subprocess.run(
                    test_cmd,
                    capture_output=True,
                    timeout=5,
                    check=False
                )
                if result.returncode != 0:
                    # ffmpeg not working
                    error_msg = (
                        f"FFmpeg is not working properly.\n\n"
                        f"Path: {ffmpeg_path}\n\n"
                        "Please install ffmpeg:\n"
                        "  brew install ffmpeg\n\n"
                        "Or run: ./setup_ffmpeg.sh"
                    )
                    self.root.after(0, lambda: messagebox.showerror("FFmpeg Not Found", error_msg))
                    self.root.after(0, self._conversion_complete)
                    return
            except FileNotFoundError:
                error_msg = (
                    f"FFmpeg not found at: {ffmpeg_path}\n\n"
                    "Please install ffmpeg:\n"
                    "  brew install ffmpeg\n\n"
                    "Or run: ./setup_ffmpeg.sh"
                )
                self.root.after(0, lambda: messagebox.showerror("FFmpeg Not Found", error_msg))
                self.root.after(0, self._conversion_complete)
                return
            except subprocess.TimeoutExpired:
                error_msg = (
                    f"FFmpeg timed out when checking version.\n\n"
                    f"Path: {ffmpeg_path}\n\n"
                    "Please check your ffmpeg installation."
                )
                self.root.after(0, lambda: messagebox.showerror("FFmpeg Error", error_msg))
                self.root.after(0, self._conversion_complete)
                return
            except Exception as e:
                error_msg = (
                    f"Error checking ffmpeg:\n\n"
                    f"{str(e)}\n\n"
                    f"Path: {ffmpeg_path}\n\n"
                    "Please install ffmpeg:\n"
                    "  brew install ffmpeg"
                )
                self.root.after(0, lambda: messagebox.showerror("FFmpeg Error", error_msg))
                self.root.after(0, self._conversion_complete)
                return
            
            # Run conversion
            self.engine.convert_batch(input_path, output_path)
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            self.root.after(0, lambda: messagebox.showerror(
                "Conversion Error",
                f"An error occurred during conversion:\n\n{str(e)}\n\n"
                f"Details:\n{error_details[:500]}"
            ))
        finally:
            self.root.after(0, self._conversion_complete)
    
    def _conversion_complete(self) -> None:
        """Handle conversion completion."""
        self.is_converting = False
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        
        if self.logger:
            stats = self.logger.stats
            total_processed = stats['converted'] + stats['skipped'] + stats['failed']
            
            if total_processed == 0:
                # No files were processed
                self.current_file_label.config(
                    text="No FLAC files found",
                    foreground="orange"
                )
                messagebox.showwarning(
                    "No Files Found",
                    f"No FLAC files were found in the input folder.\n\n"
                    f"Please check that:\n"
                    f"• The folder contains .flac files\n"
                    f"• You selected the correct folder\n"
                    f"• Files have the .flac extension"
                )
            else:
                summary = f"Conversion complete!\n\n"
                summary += f"Converted: {stats['converted']}\n"
                summary += f"Skipped: {stats['skipped']}\n"
                summary += f"Failed: {stats['failed']}\n"
                
                self.current_file_label.config(
                    text="Conversion complete",
                    foreground="green"
                )
                
                messagebox.showinfo("Conversion Complete", summary)
    
    def _cancel_conversion(self) -> None:
        """Cancel ongoing conversion."""
        if self.engine:
            self.engine.cancel()
        self.current_file_label.config(
            text="Cancelling...",
            foreground="orange"
        )
    
    def _open_output_folder(self) -> None:
        """Open output folder in Finder."""
        output_path = self.output_dir.get()
        if output_path and Path(output_path).exists():
            os.system(f'open "{output_path}"')
        else:
            messagebox.showwarning("Warning", "Output folder does not exist yet")
    
    def _open_log(self) -> None:
        """Open log file."""
        if self.logger:
            log_path = self.logger.get_log_path()
            if Path(log_path).exists():
                os.system(f'open "{log_path}"')
            else:
                messagebox.showwarning("Warning", "No log file available yet")
        else:
            messagebox.showwarning("Warning", "No conversion has been run yet")


def main():
    """Main entry point for GUI."""
    root = tk.Tk()
    app = FLAC2AIFFApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

