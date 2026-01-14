# Getting Started Guide

## Quick Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LuciferIQ162/campain-image-generation.git
   cd campain-image-generation
   ```

2. **Install basic dependencies:**
   ```bash
   pip install Pillow numpy opencv-python pyyaml click
   ```

3. **For full image generation capabilities, install AI dependencies:**
   ```bash
   pip install torch torchvision transformers diffusers accelerate
   ```
   
   Or install all at once:
   ```bash
   pip install -r requirements.txt
   ```

## First Steps

### 1. Test Image Enhancement (No GPU Required)

Enhancement works without heavy ML models:

```bash
# Run the enhancement example
python examples/enhancement_example.py
```

This will create sample images and demonstrate various enhancement techniques.

### 2. Explore Templates

List all available templates:

```bash
python main.py templates
```

Show details of a specific template:

```bash
python main.py templates --show product_photography
```

### 3. Template Management

Run the template management example:

```bash
python examples/template_management.py
```

This demonstrates creating, saving, and using custom templates.

### 4. Enhance Your Images

```bash
# Auto enhancement
python main.py enhance input.jpg --auto

# Custom enhancement
python main.py enhance input.jpg --upscale 2 --sharpen --brightness 0.1
```

### 5. Image Generation (Requires PyTorch and GPU)

Once you have PyTorch installed:

```bash
# Generate using a template
python main.py generate -t product_photography -v product="laptop" -o output/laptop.png

# Generate from custom prompt
python main.py generate -p "beautiful mountain landscape at sunset" -o output/landscape.png
```

Or use the Python API:

```python
from copilot_image_ai import ImageGenerator

generator = ImageGenerator()
image = generator.generate_from_template(
    template_name="campaign_banner",
    template_vars={
        "campaign_type": "summer sale",
        "brand_style": "modern minimalist"
    },
    output_path="output/banner.png"
)
```

## Common Use Cases

### E-commerce Product Photos

```python
from copilot_image_ai import ImageGenerator

generator = ImageGenerator()
image = generator.generate_from_template(
    template_name="product_photography",
    template_vars={"product": "wireless earbuds"},
    output_path="output/earbuds.png"
)
```

### Marketing Campaigns

```python
image = generator.generate_from_template(
    template_name="campaign_banner",
    template_vars={
        "campaign_type": "holiday sale",
        "brand_style": "elegant minimalist"
    },
    width=1024,
    height=512,
    output_path="output/campaign.png"
)
```

### Image Enhancement for Existing Photos

```python
from copilot_image_ai import ImageEnhancer

enhancer = ImageEnhancer()

# Auto enhance
enhanced = enhancer.auto_enhance("input.jpg", output_path="enhanced.jpg")

# Or with custom settings
enhanced = enhancer.enhance(
    "input.jpg",
    upscale_factor=2,
    denoise=True,
    sharpen=True,
    color_enhance=True,
    output_path="enhanced.jpg"
)
```

## Tips

1. **First Run**: Image generation model will download on first use (~5GB). Requires internet connection.

2. **GPU Acceleration**: For faster generation, use a CUDA-capable GPU. The system automatically detects and uses it.

3. **Memory Usage**: Image generation is memory-intensive. Close other applications if you encounter memory errors.

4. **Reproducibility**: Use the `seed` parameter to generate identical images:
   ```python
   image = generator.generate(prompt="...", seed=42)
   ```

5. **Templates**: Start with built-in templates and customize them for your needs.

## Troubleshooting

### "No module named 'torch'"
- Install PyTorch: `pip install torch torchvision`
- Or use CPU-only version: `pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu`

### "CUDA out of memory"
- Reduce image size: use smaller width/height
- Close other GPU-using applications
- Use CPU instead: The system will automatically fall back to CPU

### Model Download Fails
- Check internet connection
- The model is downloaded from HuggingFace (~5GB)
- Retry after ensuring stable connection

## Next Steps

- Read the full [README.md](README.md) for comprehensive documentation
- Check [API.md](docs/API.md) for detailed API reference
- Explore [examples/](examples/) directory for more code examples
- Create your own custom templates for specific needs

## Support

For issues or questions, please open an issue on GitHub:
https://github.com/LuciferIQ162/campain-image-generation/issues
