"""
Example: Image enhancement using various techniques
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from copilot_image_ai import ImageEnhancer
from PIL import Image, ImageDraw


def create_sample_image(path: str):
    """Create a sample image for demonstration"""
    img = Image.new('RGB', (400, 300), color=(100, 150, 200))
    draw = ImageDraw.Draw(img)
    
    # Draw some shapes
    draw.rectangle([50, 50, 150, 150], fill=(255, 200, 100), outline=(0, 0, 0), width=2)
    draw.ellipse([200, 100, 350, 250], fill=(150, 255, 150), outline=(0, 0, 0), width=2)
    
    # Add some text
    draw.text((150, 20), "Sample Image", fill=(255, 255, 255))
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return img


def main():
    """Demonstrate image enhancement capabilities"""
    
    print("=" * 60)
    print("Copilot Image AI - Image Enhancement Example")
    print("=" * 60)
    print()
    
    # Create sample image
    sample_path = "output/sample_image.png"
    print("Creating sample image...")
    sample_image = create_sample_image(sample_path)
    print(f"✓ Sample image created: {sample_path}")
    
    # Initialize enhancer
    enhancer = ImageEnhancer()
    
    # Example 1: Auto enhancement
    print("\n" + "=" * 60)
    print("Example 1: Auto Enhancement")
    print("=" * 60)
    
    enhanced = enhancer.auto_enhance(
        sample_path,
        output_path="output/enhanced_auto.png"
    )
    print("✓ Auto enhancement complete!")
    
    # Example 2: Super resolution upscaling
    print("\n" + "=" * 60)
    print("Example 2: Super Resolution (2x upscale)")
    print("=" * 60)
    
    upscaled = enhancer.super_resolution(
        sample_path,
        scale=2,
        output_path="output/upscaled_2x.png"
    )
    print(f"✓ Image upscaled from {sample_image.size} to {upscaled.size}")
    
    # Example 3: Custom enhancement
    print("\n" + "=" * 60)
    print("Example 3: Custom Enhancement Settings")
    print("=" * 60)
    
    custom_enhanced = enhancer.enhance(
        sample_path,
        upscale_factor=2,
        denoise=True,
        denoise_strength=0.3,
        sharpen=True,
        sharpen_amount=0.7,
        color_enhance=True,
        contrast_enhance=True,
        brightness_adjust=0.1,
        output_path="output/enhanced_custom.png"
    )
    print("✓ Custom enhancement complete!")
    
    # Example 4: Lighting adjustment
    print("\n" + "=" * 60)
    print("Example 4: Lighting Adjustment")
    print("=" * 60)
    
    lighting_adjusted = enhancer.adjust_lighting(
        sample_path,
        brightness=0.2,
        contrast=1.3,
        output_path="output/lighting_adjusted.png"
    )
    print("✓ Lighting adjustment complete!")
    
    # Example 5: Denoise only
    print("\n" + "=" * 60)
    print("Example 5: Noise Removal")
    print("=" * 60)
    
    denoised = enhancer.remove_noise(
        sample_path,
        strength=0.5,
        output_path="output/denoised.png"
    )
    print("✓ Noise removal complete!")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("Check the 'output' directory for results.")
    print("=" * 60)


if __name__ == "__main__":
    main()
