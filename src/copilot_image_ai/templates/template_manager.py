"""
Template management system for image generation prompts and styles
"""

import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path


class Template:
    """Represents an image generation template"""
    
    def __init__(
        self,
        name: str,
        description: str,
        prompt: str,
        negative_prompt: Optional[str] = None,
        style: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Initialize template
        
        Args:
            name: Template name
            description: Template description
            prompt: Base prompt for image generation
            negative_prompt: Negative prompt to avoid unwanted features
            style: Style identifier (e.g., 'realistic', 'artistic', 'cartoon')
            parameters: Additional generation parameters
            tags: Tags for categorization
        """
        self.name = name
        self.description = description
        self.prompt = prompt
        self.negative_prompt = negative_prompt or ""
        self.style = style or "general"
        self.parameters = parameters or {}
        self.tags = tags or []
    
    def format_prompt(self, **kwargs) -> str:
        """
        Format template prompt with custom variables
        
        Args:
            **kwargs: Variables to substitute in prompt
        
        Returns:
            Formatted prompt string
        """
        try:
            return self.prompt.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required template variable: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "style": self.style,
            "parameters": self.parameters,
            "tags": self.tags,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Template':
        """Create template from dictionary"""
        return cls(
            name=data["name"],
            description=data["description"],
            prompt=data["prompt"],
            negative_prompt=data.get("negative_prompt"),
            style=data.get("style"),
            parameters=data.get("parameters"),
            tags=data.get("tags"),
        )


class TemplateManager:
    """Manages image generation templates"""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize template manager
        
        Args:
            template_dir: Directory containing template files
        """
        self.template_dir = template_dir or "templates"
        self.templates: Dict[str, Template] = {}
        self._initialize_default_templates()
        
        if os.path.exists(self.template_dir):
            self.load_templates()
    
    def _initialize_default_templates(self) -> None:
        """Initialize default built-in templates"""
        default_templates = [
            Template(
                name="product_photography",
                description="Professional product photography template",
                prompt="professional product photography of {product}, studio lighting, white background, high detail, commercial quality, 8k",
                negative_prompt="blurry, low quality, amateur, distorted, dark",
                style="realistic",
                tags=["product", "commercial", "photography"],
                parameters={"guidance_scale": 8.0}
            ),
            Template(
                name="landscape_art",
                description="Beautiful landscape artwork template",
                prompt="beautiful {landscape_type} landscape, {time_of_day}, dramatic lighting, detailed, artstation, concept art, smooth, sharp focus",
                negative_prompt="blurry, ugly, distorted, low quality",
                style="artistic",
                tags=["landscape", "nature", "art"],
                parameters={"guidance_scale": 7.5}
            ),
            Template(
                name="portrait_professional",
                description="Professional portrait photography template",
                prompt="professional portrait photograph of {subject}, studio lighting, bokeh background, detailed face, high quality, 50mm lens, professional photography",
                negative_prompt="blurry, low quality, distorted, amateur, bad anatomy",
                style="realistic",
                tags=["portrait", "professional", "photography"],
                parameters={"guidance_scale": 7.0}
            ),
            Template(
                name="social_media_post",
                description="Eye-catching social media post template",
                prompt="modern social media post design, {theme}, vibrant colors, professional, clean layout, trending style, high engagement",
                negative_prompt="cluttered, ugly, low quality, amateur",
                style="graphic_design",
                tags=["social_media", "marketing", "design"],
                parameters={"guidance_scale": 7.5}
            ),
            Template(
                name="campaign_banner",
                description="Marketing campaign banner template",
                prompt="marketing campaign banner for {campaign_type}, {brand_style}, eye-catching, professional design, high impact, commercial quality",
                negative_prompt="cluttered, low quality, amateur, generic",
                style="marketing",
                tags=["campaign", "marketing", "banner"],
                parameters={"guidance_scale": 8.0}
            ),
            Template(
                name="abstract_art",
                description="Abstract artistic creation template",
                prompt="abstract art, {color_scheme}, {mood}, flowing shapes, creative, unique, artstation quality",
                negative_prompt="realistic, photographic, boring, low quality",
                style="abstract",
                tags=["abstract", "art", "creative"],
                parameters={"guidance_scale": 7.0}
            ),
        ]
        
        for template in default_templates:
            self.templates[template.name] = template
    
    def add_template(self, template: Template) -> None:
        """Add a template to the manager"""
        self.templates[template.name] = template
    
    def get_template(self, name: str) -> Optional[Template]:
        """Get template by name"""
        return self.templates.get(name)
    
    def list_templates(self, tag: Optional[str] = None, style: Optional[str] = None) -> List[Template]:
        """
        List all templates, optionally filtered by tag or style
        
        Args:
            tag: Filter by tag
            style: Filter by style
        
        Returns:
            List of matching templates
        """
        templates = list(self.templates.values())
        
        if tag:
            templates = [t for t in templates if tag in t.tags]
        
        if style:
            templates = [t for t in templates if t.style == style]
        
        return templates
    
    def save_template(self, template: Template, filepath: Optional[str] = None) -> None:
        """
        Save template to file
        
        Args:
            template: Template to save
            filepath: Custom filepath (optional)
        """
        if filepath is None:
            Path(self.template_dir).mkdir(parents=True, exist_ok=True)
            filepath = os.path.join(self.template_dir, f"{template.name}.json")
        
        with open(filepath, 'w') as f:
            json.dump(template.to_dict(), f, indent=2)
    
    def load_template(self, filepath: str) -> Template:
        """Load template from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        template = Template.from_dict(data)
        self.templates[template.name] = template
        return template
    
    def load_templates(self, directory: Optional[str] = None) -> None:
        """Load all templates from directory"""
        directory = directory or self.template_dir
        
        if not os.path.exists(directory):
            return
        
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                try:
                    self.load_template(filepath)
                except Exception as e:
                    print(f"Error loading template {filename}: {e}")
    
    def delete_template(self, name: str) -> bool:
        """Delete template by name"""
        if name in self.templates:
            del self.templates[name]
            
            # Also delete file if it exists
            filepath = os.path.join(self.template_dir, f"{name}.json")
            if os.path.exists(filepath):
                os.remove(filepath)
            
            return True
        return False
    
    def search_templates(self, query: str) -> List[Template]:
        """
        Search templates by query in name, description, or tags
        
        Args:
            query: Search query
        
        Returns:
            List of matching templates
        """
        query = query.lower()
        results = []
        
        for template in self.templates.values():
            if (query in template.name.lower() or
                query in template.description.lower() or
                any(query in tag.lower() for tag in template.tags)):
                results.append(template)
        
        return results
