"""
Example: Custom template creation and management
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from copilot_image_ai.templates import Template, TemplateManager


def main():
    """Demonstrate template management features"""
    
    print("=" * 60)
    print("Copilot Image AI - Template Management Example")
    print("=" * 60)
    print()
    
    # Initialize template manager
    template_manager = TemplateManager()
    
    # Example 1: Create custom template
    print("=" * 60)
    print("Example 1: Creating Custom Templates")
    print("=" * 60)
    print()
    
    custom_template = Template(
        name="tech_startup_logo",
        description="Modern tech startup logo design",
        prompt="modern tech startup logo, {company_name}, {industry}, minimalist design, professional, {color_scheme} colors, vector style, clean",
        negative_prompt="complex, cluttered, amateur, low quality",
        style="graphic_design",
        tags=["logo", "branding", "startup", "tech"],
        parameters={
            "guidance_scale": 8.0,
            "num_inference_steps": 60
        }
    )
    
    template_manager.add_template(custom_template)
    print(f"✓ Created template: {custom_template.name}")
    print(f"  Description: {custom_template.description}")
    print(f"  Tags: {', '.join(custom_template.tags)}")
    
    # Example 2: Save template to file
    print("\n" + "=" * 60)
    print("Example 2: Saving Template to File")
    print("=" * 60)
    print()
    
    template_manager.save_template(custom_template)
    print(f"✓ Template saved to: templates/{custom_template.name}.json")
    
    # Example 3: List templates by category
    print("\n" + "=" * 60)
    print("Example 3: Filtering Templates")
    print("=" * 60)
    print()
    
    # Filter by style
    print("Marketing style templates:")
    marketing_templates = template_manager.list_templates(style="marketing")
    for t in marketing_templates:
        print(f"  • {t.name}: {t.description}")
    
    print("\nArtistic style templates:")
    art_templates = template_manager.list_templates(style="artistic")
    for t in art_templates:
        print(f"  • {t.name}: {t.description}")
    
    # Filter by tag
    print("\nTemplates with 'photography' tag:")
    photo_templates = template_manager.list_templates(tag="photography")
    for t in photo_templates:
        print(f"  • {t.name}: {t.description}")
    
    # Example 4: Search templates
    print("\n" + "=" * 60)
    print("Example 4: Searching Templates")
    print("=" * 60)
    print()
    
    search_results = template_manager.search_templates("professional")
    print(f"Search results for 'professional':")
    for t in search_results:
        print(f"  • {t.name}: {t.description}")
    
    # Example 5: Format template prompt
    print("\n" + "=" * 60)
    print("Example 5: Using Template with Variables")
    print("=" * 60)
    print()
    
    template = template_manager.get_template("tech_startup_logo")
    if template:
        formatted_prompt = template.format_prompt(
            company_name="TechFlow",
            industry="AI and Machine Learning",
            color_scheme="blue and purple"
        )
        print("Formatted prompt:")
        print(f"  {formatted_prompt}")
    
    # Example 6: Create multiple custom templates
    print("\n" + "=" * 60)
    print("Example 6: Creating Multiple Custom Templates")
    print("=" * 60)
    print()
    
    templates_to_create = [
        {
            "name": "food_photography",
            "description": "Appetizing food photography template",
            "prompt": "professional food photography, {dish_name}, {style} style, delicious, appetizing, well-lit, high resolution, food magazine quality",
            "style": "realistic",
            "tags": ["food", "photography", "culinary"]
        },
        {
            "name": "character_concept",
            "description": "Character concept art template",
            "prompt": "character concept art, {character_type}, {setting}, detailed design, professional artwork, full body, {art_style} style",
            "style": "artistic",
            "tags": ["character", "concept", "art"]
        },
        {
            "name": "interior_design",
            "description": "Interior design visualization template",
            "prompt": "interior design, {room_type}, {design_style} style, modern, elegant, well-lit, architectural photography, high quality",
            "style": "realistic",
            "tags": ["interior", "design", "architecture"]
        }
    ]
    
    for template_data in templates_to_create:
        template = Template(
            name=template_data["name"],
            description=template_data["description"],
            prompt=template_data["prompt"],
            style=template_data.get("style", "general"),
            tags=template_data.get("tags", [])
        )
        template_manager.add_template(template)
        print(f"✓ Created: {template.name}")
    
    # Example 7: Export all custom templates
    print("\n" + "=" * 60)
    print("Example 7: Summary of All Templates")
    print("=" * 60)
    print()
    
    all_templates = template_manager.list_templates()
    print(f"Total templates: {len(all_templates)}")
    print("\nTemplate categories:")
    
    styles = {}
    for t in all_templates:
        if t.style not in styles:
            styles[t.style] = []
        styles[t.style].append(t.name)
    
    for style, templates in styles.items():
        print(f"\n{style.upper()}:")
        for name in templates:
            print(f"  • {name}")
    
    print("\n" + "=" * 60)
    print("Template management example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
