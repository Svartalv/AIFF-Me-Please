"""Logging utilities for conversion operations."""
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class ConversionLogger:
    """Structured logger for conversion operations."""
    
    def __init__(self, output_dir: str, log_level: str = "info"):
        """Initialize logger with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.output_dir / f"convert-log-{timestamp}.txt"
        
        # Set up logging
        level_map = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR
        }
        level = level_map.get(log_level.lower(), logging.INFO)
        
        # Configure file handler
        self.logger = logging.getLogger("FLAC2AIFF")
        self.logger.setLevel(level)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler (for debugging)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        self.stats = {
            "converted": 0,
            "skipped": 0,
            "failed": 0,
            "warnings": []
        }
    
    def info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        self.logger.warning(message)
        self.stats["warnings"].append(message)
    
    def error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)
    
    def debug(self, message: str) -> None:
        """Log debug message."""
        self.logger.debug(message)
    
    def log_file_start(self, filename: str) -> None:
        """Log start of file conversion."""
        self.info(f"Processing: {filename}")
    
    def log_file_success(self, filename: str, output_path: str) -> None:
        """Log successful file conversion."""
        self.info(f"✓ Converted: {filename} → {output_path}")
        self.stats["converted"] += 1
    
    def log_file_skip(self, filename: str, reason: str) -> None:
        """Log skipped file."""
        self.info(f"⊘ Skipped: {filename} ({reason})")
        self.stats["skipped"] += 1
    
    def log_file_fail(self, filename: str, reason: str) -> None:
        """Log failed file conversion."""
        self.error(f"✗ Failed: {filename} ({reason})")
        self.stats["failed"] += 1
    
    def log_summary(self) -> str:
        """Log and return conversion summary."""
        summary = f"""
Conversion Summary
==================
Converted: {self.stats['converted']}
Skipped: {self.stats['skipped']}
Failed: {self.stats['failed']}
Warnings: {len(self.stats['warnings'])}
"""
        self.info(summary)
        return summary
    
    def get_log_path(self) -> str:
        """Get path to log file."""
        return str(self.log_file)

