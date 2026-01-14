"""
Utility functions for image processing and manipulation
"""

import os
from typing import List, Tuple, Union, Optional
from PIL import Image
import numpy as np


def load_image(path: str) -> Image.Image:
    """
    Load image from file
    
    Args:
        path: Path to image file
    
    Returns:
        PIL Image
    """
    return Image.open(path).convert('RGB')


def save_image(image: Image.Image, path: str, quality: int = 95) -> None:
    """
    Save image to file
    
    Args:
        image: PIL Image to save
        path: Output path
        quality: JPEG quality (1-100)
    """
    from pathlib import Path
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    image.save(path, quality=quality)


def resize_image(
    image: Image.Image,
    size: Union[Tuple[int, int], int],
    maintain_aspect: bool = True
) -> Image.Image:
    """
    Resize image
    
    Args:
        image: Input image
        size: Target size (width, height) or max dimension
        maintain_aspect: Maintain aspect ratio
    
    Returns:
        Resized image
    """
    if isinstance(size, int):
        # Single dimension provided - calculate other dimension
        if maintain_aspect:
            max_dim = max(image.size)
            if max_dim == 0:
                raise ValueError("Invalid image dimensions: width and height cannot be zero")
            ratio = size / max_dim
            new_size = tuple(int(dim * ratio) for dim in image.size)
        else:
            new_size = (size, size)
    else:
        new_size = size
    
    return image.resize(new_size, Image.Resampling.LANCZOS)


def crop_center(image: Image.Image, crop_size: Tuple[int, int]) -> Image.Image:
    """
    Crop image from center
    
    Args:
        image: Input image
        crop_size: (width, height) of crop
    
    Returns:
        Cropped image
    """
    width, height = image.size
    crop_width, crop_height = crop_size
    
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height
    
    return image.crop((left, top, right, bottom))


def batch_process_images(
    input_dir: str,
    output_dir: str,
    process_fn,
    extensions: List[str] = None
) -> List[str]:
    """
    Process all images in a directory
    
    Args:
        input_dir: Input directory path
        output_dir: Output directory path
        process_fn: Function to process each image
        extensions: List of file extensions to process
    
    Returns:
        List of processed file paths
    """
    from pathlib import Path
    
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    processed_files = []
    
    for filename in os.listdir(input_dir):
        if any(filename.lower().endswith(ext) for ext in extensions):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            try:
                image = load_image(input_path)
                processed_image = process_fn(image)
                save_image(processed_image, output_path)
                processed_files.append(output_path)
                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    return processed_files


def create_image_grid(
    images: List[Image.Image],
    grid_size: Optional[Tuple[int, int]] = None,
    padding: int = 5
) -> Image.Image:
    """
    Create a grid of images
    
    Args:
        images: List of PIL Images
        grid_size: (rows, cols) for grid layout
        padding: Padding between images in pixels
    
    Returns:
        Grid image
    """
    if not images:
        raise ValueError("No images provided")
    
    # Calculate grid size if not provided
    if grid_size is None:
        num_images = len(images)
        cols = int(np.ceil(np.sqrt(num_images)))
        rows = int(np.ceil(num_images / cols))
        grid_size = (rows, cols)
    
    rows, cols = grid_size
    
    # Get max dimensions
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)
    
    # Create grid canvas
    grid_width = cols * max_width + (cols + 1) * padding
    grid_height = rows * max_height + (rows + 1) * padding
    
    grid = Image.new('RGB', (grid_width, grid_height), color=(255, 255, 255))
    
    # Place images
    for idx, img in enumerate(images):
        if idx >= rows * cols:
            break
        
        row = idx // cols
        col = idx % cols
        
        x = col * (max_width + padding) + padding
        y = row * (max_height + padding) + padding
        
        # Resize image to fit cell if necessary
        if img.size != (max_width, max_height):
            img = img.resize((max_width, max_height), Image.Resampling.LANCZOS)
        
        grid.paste(img, (x, y))
    
    return grid


def compare_images(
    image1: Image.Image,
    image2: Image.Image,
    labels: Optional[Tuple[str, str]] = None
) -> Image.Image:
    """
    Create side-by-side comparison of two images
    
    Args:
        image1: First image
        image2: Second image
        labels: Optional labels for images
    
    Returns:
        Comparison image
    """
    # Resize to same height
    target_height = min(image1.height, image2.height)
    
    ratio1 = target_height / image1.height
    ratio2 = target_height / image2.height
    
    new_size1 = (int(image1.width * ratio1), target_height)
    new_size2 = (int(image2.width * ratio2), target_height)
    
    img1_resized = image1.resize(new_size1, Image.Resampling.LANCZOS)
    img2_resized = image2.resize(new_size2, Image.Resampling.LANCZOS)
    
    # Create comparison canvas
    total_width = img1_resized.width + img2_resized.width + 10
    comparison = Image.new('RGB', (total_width, target_height), color=(255, 255, 255))
    
    comparison.paste(img1_resized, (0, 0))
    comparison.paste(img2_resized, (img1_resized.width + 10, 0))
    
    return comparison


def image_to_numpy(image: Image.Image) -> np.ndarray:
    """Convert PIL Image to numpy array"""
    return np.array(image)


def numpy_to_image(array: np.ndarray) -> Image.Image:
    """Convert numpy array to PIL Image"""
    return Image.fromarray(array.astype('uint8'))


def get_image_info(image: Union[str, Image.Image]) -> dict:
    """
    Get information about an image
    
    Args:
        image: Path to image or PIL Image
    
    Returns:
        Dictionary with image information
    """
    if isinstance(image, str):
        img = load_image(image)
        file_size = os.path.getsize(image)
    else:
        img = image
        file_size = None
    
    return {
        'width': img.width,
        'height': img.height,
        'mode': img.mode,
        'format': img.format,
        'file_size': file_size,
        'aspect_ratio': img.width / img.height if img.height > 0 else 0
    }
