"""
Configuration management for Copilot Image AI
"""

import os
from typing import Dict, Any, Optional
import yaml
from pathlib import Path


class Config:
    """Configuration manager for the image generation and enhancement system"""
    
    DEFAULT_CONFIG = {
        "generation": {
            "model": "stabilityai/stable-diffusion-2-1",
            "num_inference_steps": 50,
            "guidance_scale": 7.5,
            "default_size": [512, 512],
            "negative_prompt": "blurry, low quality, distorted",
        },
        "enhancement": {
            "upscale_factor": 2,
            "denoise_strength": 0.3,
            "sharpen_amount": 0.5,
            "color_enhance": True,
        },
        "output": {
            "directory": "output",
            "format": "png",
            "quality": 95,
        },
        "templates": {
            "directory": "templates",
            "auto_load": True,
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to custom configuration file (YAML)
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
    
    def load_config(self, config_path: str) -> None:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            custom_config = yaml.safe_load(f)
            self._merge_config(self.config, custom_config)
    
    def _merge_config(self, base: Dict, custom: Dict) -> None:
        """Recursively merge custom config into base config"""
        for key, value in custom.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., 'generation.model')
            default: Default value if key not found
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., 'generation.model')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, config_path: str) -> None:
        """Save current configuration to YAML file"""
        Path(config_path).parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary"""
        return self.config.copy()


# Global configuration instance
_global_config = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get global configuration instance"""
    global _global_config
    if _global_config is None:
        _global_config = Config(config_path)
    return _global_config


def reset_config() -> None:
    """Reset global configuration to default"""
    global _global_config
    _global_config = None
