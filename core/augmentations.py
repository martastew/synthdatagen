# core/augmentations.py

from PIL import Image, ImageEnhance, ImageFilter
import random
import numpy as np

def augment_image(image):
    """Apply basic brightness and contrast jitter."""
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(random.uniform(0.9, 1.1))

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(random.uniform(0.95, 1.05))

    return image

def add_camera_noise(image):
    """Add fake camera grain and slight blur."""
    image = image.convert("RGB")

    # Add noise
    noise = np.random.normal(0, 15, (image.height, image.width, 3)).astype("int16")
    img_np = np.array(image).astype("int16")
    noisy = np.clip(img_np + noise, 0, 255).astype("uint8")

    noisy_image = Image.fromarray(noisy)

    # Slight blur to simulate lens softness
    noisy_image = noisy_image.filter(ImageFilter.GaussianBlur(radius=0.6))

    return noisy_image