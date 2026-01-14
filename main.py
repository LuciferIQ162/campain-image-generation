"""
Main CLI application for Copilot Image AI
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import click


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Copilot Image AI - Template-based AI Image Generation and Enhancement"""
    pass


@cli.command()
@click.option('--list', 'list_templates', is_flag=True, help='List available templates')
@click.option('--template', '-t', help='Template name to use')
@click.option('--prompt', '-p', help='Custom prompt (without template)')
@click.option('--vars', '-v', multiple=True, help='Template variables (format: key=value)')
@click.option('--output', '-o', default='output/generated.png', help='Output path')
@click.option('--width', '-w', type=int, help='Image width')
@click.option('--height', '-h', type=int, help='Image height')
@click.option('--seed', '-s', type=int, help='Random seed for reproducibility')
@click.option('--steps', type=int, help='Number of inference steps')
def generate(list_templates, template, prompt, vars, output, width, height, seed, steps):
    """Generate images using AI"""
    
    from copilot_image_ai.templates import TemplateManager
    
    template_manager = TemplateManager()
    
    if list_templates:
        click.echo("\nAvailable Templates:")
        click.echo("=" * 60)
        for t in template_manager.list_templates():
            click.echo(f"\n{t.name}")
            click.echo(f"  Description: {t.description}")
            click.echo(f"  Style: {t.style}")
            click.echo(f"  Tags: {', '.join(t.tags)}")
        return
    
    if not template and not prompt:
        click.echo("Error: Either --template or --prompt must be provided")
        return
    
    from copilot_image_ai import ImageGenerator
    generator = ImageGenerator(template_manager=template_manager)
    
    # Parse template variables
    template_vars = {}
    if vars:
        for var in vars:
            if '=' in var:
                key, value = var.split('=', 1)
                template_vars[key] = value
    
    kwargs = {}
    if width:
        kwargs['width'] = width
    if height:
        kwargs['height'] = height
    if seed:
        kwargs['seed'] = seed
    if steps:
        kwargs['num_inference_steps'] = steps
    
    try:
        if template:
            click.echo(f"\nGenerating image using template: {template}")
            generator.generate_from_template(
                template_name=template,
                template_vars=template_vars,
                output_path=output,
                **kwargs
            )
        else:
            click.echo(f"\nGenerating image from prompt...")
            generator.generate(
                prompt=prompt,
                output_path=output,
                **kwargs
            )
        
        click.echo(f"\n✓ Image generated successfully: {output}")
        
    except Exception as e:
        click.echo(f"\n✗ Error: {e}")
        sys.exit(1)


@cli.command()
@click.argument('input_path')
@click.option('--output', '-o', help='Output path')
@click.option('--upscale', '-u', type=int, help='Upscale factor (2, 4, etc.)')
@click.option('--denoise/--no-denoise', default=True, help='Apply denoising')
@click.option('--sharpen/--no-sharpen', default=True, help='Apply sharpening')
@click.option('--color/--no-color', 'color_enhance', default=True, help='Enhance colors')
@click.option('--contrast/--no-contrast', 'contrast_enhance', default=True, help='Enhance contrast')
@click.option('--brightness', type=float, help='Brightness adjustment (-1.0 to 1.0)')
@click.option('--auto', is_flag=True, help='Use automatic enhancement')
def enhance(input_path, output, upscale, denoise, sharpen, color_enhance, 
            contrast_enhance, brightness, auto):
    """Enhance existing images"""
    
    if not os.path.exists(input_path):
        click.echo(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    if not output:
        base, ext = os.path.splitext(input_path)
        output = f"{base}_enhanced{ext}"
    
    from copilot_image_ai import ImageEnhancer
    enhancer = ImageEnhancer()
    
    try:
        click.echo(f"\nEnhancing image: {input_path}")
        
        if auto:
            enhancer.auto_enhance(input_path, output_path=output)
        else:
            kwargs = {
                'denoise': denoise,
                'sharpen': sharpen,
                'color_enhance': color_enhance,
                'contrast_enhance': contrast_enhance,
            }
            
            if upscale:
                kwargs['upscale_factor'] = upscale
            if brightness is not None:
                kwargs['brightness_adjust'] = brightness
            
            enhancer.enhance(input_path, output_path=output, **kwargs)
        
        click.echo(f"\n✓ Image enhanced successfully: {output}")
        
    except Exception as e:
        click.echo(f"\n✗ Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--show', '-s', help='Show specific template details')
@click.option('--create', '-c', is_flag=True, help='Create new template interactively')
@click.option('--delete', '-d', help='Delete template by name')
@click.option('--search', help='Search templates')
@click.option('--style', help='Filter by style')
@click.option('--tag', help='Filter by tag')
def templates(show, create, delete, search, style, tag):
    """Manage image generation templates"""
    
    from copilot_image_ai.templates import TemplateManager
    template_manager = TemplateManager()
    
    if show:
        template = template_manager.get_template(show)
        if template:
            click.echo(f"\nTemplate: {template.name}")
            click.echo("=" * 60)
            click.echo(f"Description: {template.description}")
            click.echo(f"Style: {template.style}")
            click.echo(f"Tags: {', '.join(template.tags)}")
            click.echo(f"\nPrompt:")
            click.echo(f"  {template.prompt}")
            click.echo(f"\nNegative Prompt:")
            click.echo(f"  {template.negative_prompt}")
            click.echo(f"\nParameters:")
            for key, value in template.parameters.items():
                click.echo(f"  {key}: {value}")
        else:
            click.echo(f"Template '{show}' not found")
        return
    
    if delete:
        if template_manager.delete_template(delete):
            click.echo(f"✓ Template '{delete}' deleted")
        else:
            click.echo(f"Template '{delete}' not found")
        return
    
    if search:
        results = template_manager.search_templates(search)
        click.echo(f"\nSearch results for '{search}':")
        for t in results:
            click.echo(f"  • {t.name}: {t.description}")
        return
    
    # List templates with optional filters
    templates_list = template_manager.list_templates(tag=tag, style=style)
    
    click.echo("\nAvailable Templates:")
    click.echo("=" * 60)
    
    for t in templates_list:
        click.echo(f"\n{t.name}")
        click.echo(f"  {t.description}")
        click.echo(f"  Style: {t.style} | Tags: {', '.join(t.tags)}")


@cli.command()
def info():
    """Show system information"""
    
    click.echo("\nCopilot Image AI - System Information")
    click.echo("=" * 60)
    click.echo(f"Version: 1.0.0")
    click.echo(f"Python: {sys.version.split()[0]}")
    
    try:
        import torch
        click.echo(f"PyTorch: {torch.__version__}")
        click.echo(f"CUDA Available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            click.echo(f"CUDA Version: {torch.version.cuda}")
            click.echo(f"GPU: {torch.cuda.get_device_name(0)}")
    except ImportError:
        click.echo("PyTorch: Not installed (required for image generation)")
    
    click.echo("\nConfiguration:")
    from copilot_image_ai.config import Config
    config = Config()
    click.echo(f"  Model: {config.get('generation.model')}")
    click.echo(f"  Default Size: {config.get('generation.default_size')}")
    click.echo(f"  Output Directory: {config.get('output.directory')}")


if __name__ == '__main__':
    cli()
