"""
AI-powered image generation using templates and diffusion models
"""

import os
from typing import Optional, Dict, Any, List, Union
from pathlib import Path
import torch
from PIL import Image
import numpy as np

from ..templates.template_manager import Template, TemplateManager
from ..config import Config


class ImageGenerator:
    """
    AI-powered image generator using diffusion models and templates
    """
    
    def __init__(
        self,
        config: Optional[Config] = None,
        template_manager: Optional[TemplateManager] = None,
        device: Optional[str] = None
    ):
        """
        Initialize image generator
        
        Args:
            config: Configuration object
            template_manager: Template manager instance
            device: Device to run model on ('cuda', 'cpu', or None for auto)
        """
        from ..config import get_config
        
        self.config = config or get_config()
        self.template_manager = template_manager or TemplateManager()
        
        # Determine device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        self.pipeline = None
        self._model_loaded = False
    
    def _load_model(self) -> None:
        """Load the diffusion model (lazy loading)"""
        if self._model_loaded:
            return
        
        try:
            from diffusers import StableDiffusionPipeline
            
            model_name = self.config.get("generation.model")
            print(f"Loading model: {model_name}")
            
            # Load pipeline
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,  # Disable for faster inference
                requires_safety_checker=False
            )
            
            self.pipeline = self.pipeline.to(self.device)
            
            # Enable memory optimizations
            if self.device == "cuda":
                self.pipeline.enable_attention_slicing()
            
            self._model_loaded = True
            print(f"Model loaded successfully on {self.device}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Note: Model loading requires internet connection and HuggingFace access")
            raise
    
    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        num_inference_steps: Optional[int] = None,
        guidance_scale: Optional[float] = None,
        seed: Optional[int] = None,
        num_images: int = 1,
        output_path: Optional[str] = None
    ) -> Union[Image.Image, List[Image.Image]]:
        """
        Generate image from prompt
        
        Args:
            prompt: Text prompt for generation
            negative_prompt: Negative prompt
            width: Image width
            height: Image height
            num_inference_steps: Number of denoising steps
            guidance_scale: Guidance scale for classifier-free guidance
            seed: Random seed for reproducibility
            num_images: Number of images to generate
            output_path: Path to save generated image
        
        Returns:
            Generated image(s)
        """
        self._load_model()
        
        # Get parameters from config if not provided
        if negative_prompt is None:
            negative_prompt = self.config.get("generation.negative_prompt")
        
        if width is None or height is None:
            default_size = self.config.get("generation.default_size")
            width = width or default_size[0]
            height = height or default_size[1]
        
        num_inference_steps = num_inference_steps or self.config.get("generation.num_inference_steps")
        guidance_scale = guidance_scale or self.config.get("generation.guidance_scale")
        
        # Set seed for reproducibility
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        else:
            generator = None
        
        # Generate image
        print(f"Generating {num_images} image(s)...")
        print(f"Prompt: {prompt}")
        
        results = self.pipeline(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator,
            num_images_per_prompt=num_images
        )
        
        images = results.images
        
        # Save if output path provided
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            if num_images == 1:
                images[0].save(output_path)
                print(f"Image saved to: {output_path}")
            else:
                base_path = Path(output_path)
                for i, img in enumerate(images):
                    save_path = base_path.parent / f"{base_path.stem}_{i}{base_path.suffix}"
                    img.save(save_path)
                    print(f"Image {i+1} saved to: {save_path}")
        
        return images[0] if num_images == 1 else images
    
    def generate_from_template(
        self,
        template_name: str,
        template_vars: Optional[Dict[str, Any]] = None,
        output_path: Optional[str] = None,
        **generation_kwargs
    ) -> Union[Image.Image, List[Image.Image]]:
        """
        Generate image using a template
        
        Args:
            template_name: Name of template to use
            template_vars: Variables to format template prompt
            output_path: Path to save generated image
            **generation_kwargs: Additional generation parameters
        
        Returns:
            Generated image(s)
        """
        template = self.template_manager.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        # Format prompt with variables
        template_vars = template_vars or {}
        prompt = template.format_prompt(**template_vars)
        
        # Merge template parameters with generation kwargs
        params = template.parameters.copy()
        params.update(generation_kwargs)
        
        # Use template's negative prompt if not overridden
        if 'negative_prompt' not in params:
            params['negative_prompt'] = template.negative_prompt
        
        return self.generate(prompt=prompt, output_path=output_path, **params)
    
    def batch_generate(
        self,
        prompts: List[str],
        output_dir: str,
        **generation_kwargs
    ) -> List[Image.Image]:
        """
        Generate multiple images from a list of prompts
        
        Args:
            prompts: List of prompts
            output_dir: Directory to save images
            **generation_kwargs: Additional generation parameters
        
        Returns:
            List of generated images
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        images = []
        for i, prompt in enumerate(prompts):
            output_path = os.path.join(output_dir, f"image_{i:03d}.png")
            image = self.generate(prompt=prompt, output_path=output_path, **generation_kwargs)
            images.append(image)
        
        return images
    
    def get_available_templates(self) -> List[str]:
        """Get list of available template names"""
        return list(self.template_manager.templates.keys())
    
    def unload_model(self) -> None:
        """Unload model from memory"""
        if self._model_loaded:
            del self.pipeline
            self.pipeline = None
            self._model_loaded = False
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            print("Model unloaded from memory")
