"""
Example: Basic image generation using templates
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from copilot_image_ai import ImageGenerator, TemplateManager


def main():
    """Demonstrate basic image generation with templates"""
    
    print("=" * 60)
    print("Copilot Image AI - Basic Generation Example")
    print("=" * 60)
    print()
    
    # Initialize components
    template_manager = TemplateManager()
    generator = ImageGenerator(template_manager=template_manager)
    
    # List available templates
    print("Available Templates:")
    print("-" * 60)
    for template_name in generator.get_available_templates():
        template = template_manager.get_template(template_name)
        print(f"• {template_name}")
        print(f"  Description: {template.description}")
        print(f"  Style: {template.style}")
        print()
    
    # Example 1: Generate using product photography template
    print("\n" + "=" * 60)
    print("Example 1: Product Photography")
    print("=" * 60)
    
    try:
        image = generator.generate_from_template(
            template_name="product_photography",
            template_vars={
                "product": "modern wireless headphones"
            },
            output_path="output/product_headphones.png",
            seed=42
        )
        print("✓ Image generated successfully!")
    except Exception as e:
        print(f"Note: {e}")
        print("(Image generation requires model download and GPU/CPU resources)")
    
    # Example 2: Generate using landscape template
    print("\n" + "=" * 60)
    print("Example 2: Landscape Art")
    print("=" * 60)
    
    try:
        image = generator.generate_from_template(
            template_name="landscape_art",
            template_vars={
                "landscape_type": "mountain",
                "time_of_day": "sunset"
            },
            output_path="output/landscape_sunset.png",
            seed=123
        )
        print("✓ Image generated successfully!")
    except Exception as e:
        print(f"Note: {e}")
        print("(Image generation requires model download and GPU/CPU resources)")
    
    # Example 3: Generate campaign banner
    print("\n" + "=" * 60)
    print("Example 3: Campaign Banner")
    print("=" * 60)
    
    try:
        image = generator.generate_from_template(
            template_name="campaign_banner",
            template_vars={
                "campaign_type": "summer sale",
                "brand_style": "modern minimalist"
            },
            output_path="output/campaign_banner.png",
            width=1024,
            height=512,
            seed=456
        )
        print("✓ Image generated successfully!")
    except Exception as e:
        print(f"Note: {e}")
        print("(Image generation requires model download and GPU/CPU resources)")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
