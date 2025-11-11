"""Configuration management for FLAC2AIFF."""
import json
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Manages application configuration with defaults and user overrides."""
    
    DEFAULT_CONFIG = {
        "bit_depth": 16,
        "sample_rate": 44100,
        "embed_artwork": False,
        "overwrite": False,
        "concurrency": 2,
        "filename_template": "{artist} - {title}",
        "unsafe_chars": "/\\?*:\"<>|",
        "log_level": "info"
    }
    
    def __init__(self, config_path: str = None):
        """Initialize config, loading from file if it exists."""
        if config_path is None:
            # Store config in user's Application Support directory
            app_name = "FLAC2AIFF"
            home = Path.home()
            config_dir = home / "Library" / "Application Support" / app_name
            config_dir.mkdir(parents=True, exist_ok=True)
            config_path = str(config_dir / "config.json")
        
        self.config_path = config_path
        self._config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self) -> None:
        """Load configuration from file, merging with defaults."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self._config.update(user_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config from {self.config_path}: {e}")
    
    def save(self) -> None:
        """Save current configuration to file."""
        config_dir = Path(self.config_path).parent
        config_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save config to {self.config_path}: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config[key] = value
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple configuration values."""
        self._config.update(updates)
    
    @property
    def bit_depth(self) -> int:
        return self.get("bit_depth", 16)
    
    @property
    def sample_rate(self) -> int:
        return self.get("sample_rate", 44100)
    
    @property
    def embed_artwork(self) -> bool:
        return self.get("embed_artwork", False)
    
    @property
    def overwrite(self) -> bool:
        return self.get("overwrite", False)
    
    @property
    def concurrency(self) -> int:
        return self.get("concurrency", 2)
    
    @property
    def filename_template(self) -> str:
        return self.get("filename_template", "{artist} - {title}")
    
    @property
    def unsafe_chars(self) -> str:
        return self.get("unsafe_chars", "/\\?*:\"<>|")
    
    @property
    def log_level(self) -> str:
        return self.get("log_level", "info")

