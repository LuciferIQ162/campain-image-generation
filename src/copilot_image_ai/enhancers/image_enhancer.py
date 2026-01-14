"""
AI-powered image enhancement utilities
"""

import os
from typing import Optional, Tuple, Union
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2

from ..config import Config


# Enhancement constants
DEFAULT_DENOISE_H_PARAM = 30  # H parameter for Non-Local Means denoising
UNSHARP_MASK_RADIUS = 2  # Radius for unsharp mask filter
UNSHARP_MASK_PERCENT_BASE = 150  # Base percent for unsharp mask
UNSHARP_MASK_THRESHOLD = 3  # Threshold for unsharp mask


class ImageEnhancer:
    """
    AI-powered image enhancer with various enhancement capabilities
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize image enhancer
        
        Args:
            config: Configuration object
        """
        from ..config import get_config
        
        self.config = config or get_config()
    
    def enhance(
        self,
        image: Union[str, Image.Image, np.ndarray],
        upscale_factor: Optional[int] = None,
        denoise: bool = True,
        denoise_strength: Optional[float] = None,
        sharpen: bool = True,
        sharpen_amount: Optional[float] = None,
        color_enhance: Optional[bool] = None,
        contrast_enhance: bool = True,
        brightness_adjust: Optional[float] = None,
        output_path: Optional[str] = None
    ) -> Image.Image:
        """
        Enhance image with multiple techniques
        
        Args:
            image: Input image (path, PIL Image, or numpy array)
            upscale_factor: Factor to upscale image (2, 4, etc.)
            denoise: Apply denoising
            denoise_strength: Denoising strength (0.0-1.0)
            sharpen: Apply sharpening
            sharpen_amount: Sharpening amount (0.0-1.0)
            color_enhance: Enhance color saturation
            contrast_enhance: Enhance contrast
            brightness_adjust: Brightness adjustment (-1.0 to 1.0)
            output_path: Path to save enhanced image
        
        Returns:
            Enhanced PIL Image
        """
        # Load image
        img = self._load_image(image)
        
        # Get parameters from config if not provided
        upscale_factor = upscale_factor or self.config.get("enhancement.upscale_factor")
        denoise_strength = denoise_strength or self.config.get("enhancement.denoise_strength")
        sharpen_amount = sharpen_amount or self.config.get("enhancement.sharpen_amount")
        color_enhance = color_enhance if color_enhance is not None else self.config.get("enhancement.color_enhance")
        
        print(f"Enhancing image: {img.size}")
        
        # Upscale
        if upscale_factor and upscale_factor > 1:
            img = self._upscale(img, upscale_factor)
            print(f"Upscaled to: {img.size}")
        
        # Denoise
        if denoise:
            img = self._denoise(img, denoise_strength)
            print("Denoising applied")
        
        # Enhance color
        if color_enhance:
            img = self._enhance_color(img)
            print("Color enhancement applied")
        
        # Enhance contrast
        if contrast_enhance:
            img = self._enhance_contrast(img)
            print("Contrast enhancement applied")
        
        # Adjust brightness
        if brightness_adjust:
            img = self._adjust_brightness(img, brightness_adjust)
            print(f"Brightness adjusted by {brightness_adjust}")
        
        # Sharpen
        if sharpen:
            img = self._sharpen(img, sharpen_amount)
            print("Sharpening applied")
        
        # Save if output path provided
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            quality = self.config.get("output.quality")
            img.save(output_path, quality=quality)
            print(f"Enhanced image saved to: {output_path}")
        
        return img
    
    def _load_image(self, image: Union[str, Image.Image, np.ndarray]) -> Image.Image:
        """Load image from various sources"""
        if isinstance(image, str):
            return Image.open(image).convert('RGB')
        elif isinstance(image, Image.Image):
            return image.convert('RGB')
        elif isinstance(image, np.ndarray):
            return Image.fromarray(image).convert('RGB')
        else:
            raise ValueError("Unsupported image type")
    
    def _upscale(self, image: Image.Image, factor: int) -> Image.Image:
        """Upscale image using high-quality interpolation"""
        new_size = (image.width * factor, image.height * factor)
        return image.resize(new_size, Image.Resampling.LANCZOS)
    
    def _denoise(self, image: Image.Image, strength: float) -> Image.Image:
        """Apply denoising using Non-Local Means"""
        img_array = np.array(image)
        
        # Convert strength (0-1) to h parameter
        h = int(strength * DEFAULT_DENOISE_H_PARAM)
        
        # Apply Non-Local Means denoising
        denoised = cv2.fastNlMeansDenoisingColored(img_array, None, h, h, 7, 21)
        
        return Image.fromarray(denoised)
    
    def _sharpen(self, image: Image.Image, amount: float) -> Image.Image:
        """Apply sharpening filter"""
        if amount <= 0:
            return image
        
        # Apply unsharp mask
        sharpened = image.filter(
            ImageFilter.UnsharpMask(
                radius=UNSHARP_MASK_RADIUS,
                percent=int(amount * UNSHARP_MASK_PERCENT_BASE),
                threshold=UNSHARP_MASK_THRESHOLD
            )
        )
        
        return sharpened
    
    def _enhance_color(self, image: Image.Image, factor: float = 1.3) -> Image.Image:
        """Enhance color saturation"""
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
    
    def _enhance_contrast(self, image: Image.Image, factor: float = 1.2) -> Image.Image:
        """Enhance contrast"""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    def _adjust_brightness(self, image: Image.Image, adjustment: float) -> Image.Image:
        """Adjust brightness"""
        factor = 1.0 + adjustment
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    def auto_enhance(
        self,
        image: Union[str, Image.Image, np.ndarray],
        output_path: Optional[str] = None
    ) -> Image.Image:
        """
        Automatically enhance image with optimal settings
        
        Args:
            image: Input image
            output_path: Path to save enhanced image
        
        Returns:
            Enhanced PIL Image
        """
        return self.enhance(
            image=image,
            denoise=True,
            sharpen=True,
            color_enhance=True,
            contrast_enhance=True,
            output_path=output_path
        )
    
    def super_resolution(
        self,
        image: Union[str, Image.Image, np.ndarray],
        scale: int = 2,
        output_path: Optional[str] = None
    ) -> Image.Image:
        """
        Perform super-resolution upscaling
        
        Args:
            image: Input image
            scale: Upscaling factor
            output_path: Path to save result
        
        Returns:
            Upscaled image
        """
        img = self._load_image(image)
        
        print(f"Performing super-resolution upscaling (x{scale})")
        
        # For now, use high-quality interpolation
        # In production, this could use a deep learning model
        result = self._upscale(img, scale)
        
        # Apply slight sharpening after upscale
        result = self._sharpen(result, 0.3)
        
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            quality = self.config.get("output.quality")
            result.save(output_path, quality=quality)
            print(f"Super-resolution result saved to: {output_path}")
        
        return result
    
    def remove_noise(
        self,
        image: Union[str, Image.Image, np.ndarray],
        strength: float = 0.5,
        output_path: Optional[str] = None
    ) -> Image.Image:
        """
        Remove noise from image
        
        Args:
            image: Input image
            strength: Denoising strength (0.0-1.0)
            output_path: Path to save result
        
        Returns:
            Denoised image
        """
        img = self._load_image(image)
        result = self._denoise(img, strength)
        
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            quality = self.config.get("output.quality")
            result.save(output_path, quality=quality)
            print(f"Denoised image saved to: {output_path}")
        
        return result
    
    def adjust_lighting(
        self,
        image: Union[str, Image.Image, np.ndarray],
        brightness: float = 0.0,
        contrast: float = 1.2,
        output_path: Optional[str] = None
    ) -> Image.Image:
        """
        Adjust image lighting (brightness and contrast)
        
        Args:
            image: Input image
            brightness: Brightness adjustment (-1.0 to 1.0)
            contrast: Contrast factor (0.5 to 2.0)
            output_path: Path to save result
        
        Returns:
            Adjusted image
        """
        img = self._load_image(image)
        
        # Adjust brightness
        if brightness != 0.0:
            img = self._adjust_brightness(img, brightness)
        
        # Adjust contrast
        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)
        
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            quality = self.config.get("output.quality")
            img.save(output_path, quality=quality)
            print(f"Lighting-adjusted image saved to: {output_path}")
        
        return img
