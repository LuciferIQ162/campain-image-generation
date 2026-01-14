"""
Copilot Image AI - Template-based AI Image Generation and Enhancement
"""

__version__ = "1.0.0"
__author__ = "LuciferIQ162"
__description__ = "Template copilot-based AI model for image generation and enhancement"

# Lazy imports to avoid loading heavy dependencies
def __getattr__(name):
    if name == "ImageGenerator":
        from .generators.image_generator import ImageGenerator
        return ImageGenerator
    elif name == "ImageEnhancer":
        from .enhancers.image_enhancer import ImageEnhancer
        return ImageEnhancer
    elif name == "TemplateManager":
        from .templates.template_manager import TemplateManager
        return TemplateManager
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "ImageGenerator",
    "ImageEnhancer",
    "TemplateManager",
]
