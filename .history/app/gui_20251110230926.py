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
        self.root.geometry("700x300")
        self.root.resizable(True, False)
        
        # Configuration
        self.config = Config()
        
        # State
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        
        self.engine: Optional[ConversionEngine] = None
        self.logger: Optional[ConversionLogger] = None
        self.is_converting = False
        
        self._build_ui()
    
    def _build_ui(self) -> None:
        """Build the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
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
        ttk.Label(main_frame, text="Input folder:", font=("", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )
        ttk.Entry(main_frame, textvariable=self.input_dir, width=60).grid(
            row=row, column=1, sticky=(tk.W, tk.E), padx=10, pady=10
        )
        ttk.Button(
            main_frame,
            text="Choose...",
            command=self._select_input_folder
        ).grid(row=row, column=2, padx=5, pady=10)
        row += 1
        
        # Output folder
        ttk.Label(main_frame, text="Output folder:", font=("", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )
        ttk.Entry(main_frame, textvariable=self.output_dir, width=60).grid(
            row=row, column=1, sticky=(tk.W, tk.E), padx=10, pady=10
        )
        ttk.Button(
            main_frame,
            text="Choose...",
            command=self._select_output_folder
        ).grid(row=row, column=2, padx=5, pady=10)
        row += 1
        
        # Status area
        self.status_label = ttk.Label(
            main_frame,
            text="Ready",
            foreground="gray",
            font=("", 10)
        )
        self.status_label.grid(row=row, column=0, columnspan=3, pady=20)
        row += 1
        
        # Start button
        self.start_button = ttk.Button(
            main_frame,
            text="Start Conversion",
            command=self._start_conversion,
            width=20
        )
        self.start_button.grid(row=row, column=0, columnspan=3, pady=10)
    
    def _select_input_folder(self) -> None:
        """Select input folder."""
        folder = filedialog.askdirectory(title="Select input folder containing FLAC files")
        if folder:
            folder_path = Path(folder)
            if not folder_path.exists():
                messagebox.showerror("Error", f"Selected folder does not exist:\n{folder}")
                return
            
            if not folder_path.is_dir():
                messagebox.showerror("Error", f"Selected path is not a folder:\n{folder}")
                return
            
            self.input_dir.set(str(folder_path))
            
            # Check if folder contains FLAC files and show count
            flac_count = len(list(folder_path.glob("*.flac"))) + len(list(folder_path.glob("**/*.flac")))
            if flac_count > 0:
                self.status_label.config(
                    text=f"Found {flac_count} FLAC file(s) in folder",
                    foreground="green"
                )
            else:
                self.status_label.config(
                    text="No FLAC files found in selected folder",
                    foreground="orange"
                )
            
            # Auto-set output folder if empty
            if not self.output_dir.get():
                output_path = folder_path.parent / f"{folder_path.name}_AIFF"
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
        if total > 0:
            self.status_label.config(
                text=f"Processing: {filename} ({current}/{total})",
                foreground="black"
            )
    
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
        
        # Set fixed high-quality settings
        self.config.set("bit_depth", 24)  # Top quality
        self.config.set("sample_rate", 44100)
        self.config.set("embed_artwork", False)
        self.config.set("overwrite", False)
        self.config.set("concurrency", 2)
        self.config.set("filename_template", "{original}")  # Keep original filename
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
        
        # Disable start button
        self.start_button.config(state=tk.DISABLED)
        self.is_converting = True
        
        # Update status
        self.status_label.config(text="Starting conversion...", foreground="black")
        
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
        
        if self.logger:
            stats = self.logger.stats
            total_processed = stats['converted'] + stats['skipped'] + stats['failed']
            
            if total_processed == 0:
                # No files were processed
                self.status_label.config(
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
                if stats['skipped'] > 0:
                    summary += f"Skipped: {stats['skipped']}\n"
                if stats['failed'] > 0:
                    summary += f"Failed: {stats['failed']}\n"
                
                self.status_label.config(
                    text=f"Complete! Converted {stats['converted']} file(s)",
                    foreground="green"
                )
                
                messagebox.showinfo("Conversion Complete", summary)
    


def main():
    """Main entry point for GUI."""
    root = tk.Tk()
    app = FLAC2AIFFApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

