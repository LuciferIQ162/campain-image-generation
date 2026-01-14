# Copilot Image AI - Campaign Image Generation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful template-based AI model for generating and enhancing images using state-of-the-art diffusion models. Perfect for creating campaign images, marketing materials, product photography, and more.

## 🌟 Features

- **Template-Based Generation**: Pre-built templates for common use cases (product photography, landscapes, portraits, campaigns, etc.)
- **AI-Powered Image Enhancement**: Automatic image enhancement with upscaling, denoising, sharpening, and color correction
- **Custom Templates**: Create and manage your own templates for specific needs
- **Flexible API**: Easy-to-use Python API and CLI interface
- **Multiple Styles**: Support for various artistic styles (realistic, artistic, abstract, marketing, etc.)
- **Batch Processing**: Generate or enhance multiple images at once
- **Reproducible Results**: Seed support for consistent generation

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Python API](#python-api)
  - [Command Line Interface](#command-line-interface)
- [Templates](#templates)
- [Configuration](#configuration)
- [Examples](#examples)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-capable GPU for faster generation

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/LuciferIQ162/campain-image-generation.git
cd campain-image-generation

# Install required packages
pip install -r requirements.txt
```

### First Run

The first time you run image generation, the AI model will be downloaded automatically (this may take a few minutes and requires an internet connection).

## 🎯 Quick Start

### Using Python API

```python
from copilot_image_ai import ImageGenerator, ImageEnhancer, TemplateManager

# Initialize components
generator = ImageGenerator()

# Generate an image using a template
image = generator.generate_from_template(
    template_name="product_photography",
    template_vars={"product": "wireless headphones"},
    output_path="output/headphones.png"
)

# Enhance an existing image
enhancer = ImageEnhancer()
enhanced = enhancer.auto_enhance(
    "input/image.jpg",
    output_path="output/enhanced.png"
)
```

### Using Command Line

```bash
# List available templates
python main.py templates

# Generate image using template
python main.py generate -t product_photography -v product="laptop" -o output/laptop.png

# Enhance an image
python main.py enhance input/image.jpg -o output/enhanced.jpg --auto

# Get system information
python main.py info
```

## 📖 Usage

### Python API

#### Image Generation

```python
from copilot_image_ai import ImageGenerator

generator = ImageGenerator()

# Generate from custom prompt
image = generator.generate(
    prompt="professional product photography of modern smartphone",
    width=512,
    height=512,
    seed=42,
    output_path="output/phone.png"
)

# Generate using template
image = generator.generate_from_template(
    template_name="landscape_art",
    template_vars={
        "landscape_type": "mountain",
        "time_of_day": "sunset"
    },
    output_path="output/landscape.png"
)

# Batch generation
prompts = [
    "professional portrait of a CEO",
    "modern office interior",
    "tech product showcase"
]
images = generator.batch_generate(
    prompts=prompts,
    output_dir="output/batch"
)
```

#### Image Enhancement

```python
from copilot_image_ai import ImageEnhancer

enhancer = ImageEnhancer()

# Auto enhancement
enhanced = enhancer.auto_enhance("input.jpg", output_path="output.jpg")

# Custom enhancement
enhanced = enhancer.enhance(
    "input.jpg",
    upscale_factor=2,
    denoise=True,
    sharpen=True,
    color_enhance=True,
    output_path="output.jpg"
)

# Super resolution
upscaled = enhancer.super_resolution("input.jpg", scale=4)

# Lighting adjustment
adjusted = enhancer.adjust_lighting(
    "input.jpg",
    brightness=0.2,
    contrast=1.3
)
```

#### Template Management

```python
from copilot_image_ai.templates import Template, TemplateManager

manager = TemplateManager()

# List available templates
templates = manager.list_templates()

# Filter by style or tag
marketing_templates = manager.list_templates(style="marketing")
photo_templates = manager.list_templates(tag="photography")

# Create custom template
custom_template = Template(
    name="my_template",
    description="My custom template",
    prompt="professional {subject} photography, studio lighting",
    style="realistic",
    tags=["custom", "photography"]
)

manager.add_template(custom_template)
manager.save_template(custom_template)

# Search templates
results = manager.search_templates("professional")
```

### Command Line Interface

#### Generate Images

```bash
# List available templates
python main.py templates

# Generate using template
python main.py generate \
  -t product_photography \
  -v product="smartwatch" \
  -o output/watch.png \
  --seed 42

# Generate from custom prompt
python main.py generate \
  -p "beautiful sunset landscape" \
  -o output/sunset.png \
  --width 1024 \
  --height 512

# Show template details
python main.py templates --show product_photography
```

#### Enhance Images

```bash
# Auto enhancement
python main.py enhance input.jpg --auto

# Custom enhancement
python main.py enhance input.jpg \
  -o output.jpg \
  --upscale 2 \
  --denoise \
  --sharpen \
  --brightness 0.1

# Without specific options
python main.py enhance input.jpg
```

#### Manage Templates

```bash
# List all templates
python main.py templates

# Filter by style
python main.py templates --style realistic

# Filter by tag
python main.py templates --tag marketing

# Search templates
python main.py templates --search "professional"

# Show template details
python main.py templates --show campaign_banner
```

## 📝 Templates

### Built-in Templates

The system comes with several pre-built templates:

| Template | Description | Style | Use Case |
|----------|-------------|-------|----------|
| `product_photography` | Professional product photos | Realistic | E-commerce, catalogs |
| `landscape_art` | Beautiful landscape artwork | Artistic | Backgrounds, art |
| `portrait_professional` | Professional portraits | Realistic | Business, LinkedIn |
| `social_media_post` | Eye-catching social posts | Graphic Design | Instagram, Facebook |
| `campaign_banner` | Marketing campaign banners | Marketing | Ads, promotions |
| `abstract_art` | Abstract artistic creations | Abstract | Art, decoration |

### Template Variables

Templates support variable substitution:

```python
# Template: "professional {style} photography of {subject}"

generator.generate_from_template(
    template_name="my_template",
    template_vars={
        "style": "studio",
        "subject": "product"
    }
)
```

### Creating Custom Templates

```python
from copilot_image_ai.templates import Template

template = Template(
    name="food_photography",
    description="Appetizing food photography",
    prompt="professional food photography, {dish}, delicious, well-lit",
    negative_prompt="blurry, unappetizing",
    style="realistic",
    tags=["food", "photography"],
    parameters={
        "guidance_scale": 8.0,
        "num_inference_steps": 60
    }
)
```

## ⚙️ Configuration

### Configuration File

Create a `config.yaml` file to customize settings:

```yaml
generation:
  model: "stabilityai/stable-diffusion-2-1"
  num_inference_steps: 50
  guidance_scale: 7.5
  default_size: [512, 512]

enhancement:
  upscale_factor: 2
  denoise_strength: 0.3
  sharpen_amount: 0.5

output:
  directory: "output"
  format: "png"
  quality: 95
```

### Using Configuration

```python
from copilot_image_ai.config import Config

config = Config("path/to/config.yaml")
generator = ImageGenerator(config=config)
```

## 📚 Examples

Check the `examples/` directory for complete examples:

- `basic_generation.py` - Basic image generation with templates
- `enhancement_example.py` - Various image enhancement techniques
- `template_management.py` - Creating and managing templates

Run examples:

```bash
cd examples
python basic_generation.py
python enhancement_example.py
python template_management.py
```

## 🏗️ Architecture

```
copilot_image_ai/
├── generators/          # Image generation modules
│   └── image_generator.py
├── enhancers/          # Image enhancement modules
│   └── image_enhancer.py
├── templates/          # Template management
│   └── template_manager.py
├── utils/              # Utility functions
│   └── image_utils.py
└── config.py           # Configuration management
```

## 🔧 Advanced Features

### Seed for Reproducibility

```python
# Same seed produces same image
image1 = generator.generate(prompt="...", seed=42)
image2 = generator.generate(prompt="...", seed=42)  # Identical to image1
```

### Batch Processing

```python
# Process multiple images
enhancer.enhance(
    "input/*.jpg",
    output_dir="output/enhanced/"
)
```

### Custom Models

```python
config.set("generation.model", "runwayml/stable-diffusion-v1-5")
generator = ImageGenerator(config=config)
```

## 🎨 Use Cases

- **E-commerce**: Product photography for online stores
- **Marketing**: Campaign banners and promotional materials
- **Social Media**: Eye-catching posts and stories
- **Content Creation**: Blog images, thumbnails
- **Art & Design**: Concept art, illustrations
- **Photography**: Enhancement and upscaling of existing photos

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🙏 Acknowledgments

- Built with [Stable Diffusion](https://github.com/CompVis/stable-diffusion)
- Powered by [Hugging Face Diffusers](https://github.com/huggingface/diffusers)
- Image processing with [Pillow](https://python-pillow.org/) and [OpenCV](https://opencv.org/)

---

Made with ❤️ by [LuciferIQ162](https://github.com/LuciferIQ162)