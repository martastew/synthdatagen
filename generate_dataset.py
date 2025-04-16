from core.renderer import render_model
from core.mask_utils import apply_weather_effects
from core.augmentations import augment_image
from core.metadata import save_metadata
from core.yolo_export import export_yolo
from core.coco_export import export_coco

from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance
import os, random

def get_bbox(img):
    return [0, 0, img.width, img.height]

def apply_camera_noise(image):
    image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
    image = ImageEnhance.Brightness(image).enhance(random.uniform(0.95, 1.05))
    image = ImageEnhance.Contrast(image).enhance(random.uniform(0.9, 1.1))
    return image

def generate_synthetic_dataset(fbx_path, backgrounds_dir, output_dir="generated", num=10, weather="none", selected_bg_path=None):
    Path(output_dir).mkdir(exist_ok=True)

    bgs = [selected_bg_path] if selected_bg_path else [
        os.path.join(backgrounds_dir, f)
        for f in os.listdir(backgrounds_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    for i in range(int(num)):
        rot = [random.uniform(0, 360) for _ in range(3)]
        scale = round(random.uniform(0.7, 1.5), 2)
        bg_path = random.choice(bgs) if bgs else None

        print(f"[{i+1}/{num}] Rendering {fbx_path} with weather={weather}, rot={rot}, scale={scale}")

        rendered = render_model(fbx_path, output_dir, *rot, scale)
        model_img = Image.open(rendered).convert("RGBA")

        if bg_path:
            bg = Image.open(bg_path).convert("RGBA").resize(model_img.size)
        else:
            bg = Image.new("RGBA", model_img.size, (128, 128, 128, 255))

        bg.paste(model_img, (0, 0), model_img)

        if weather != "none":
            final = apply_weather_effects(bg, weather)
        else:
            final = bg

        final = apply_camera_noise(final)
        final = augment_image(final)

        final_path = rendered.replace(".png", "_final.png")
        final.save(final_path)
        print(f"Saved: {final_path}")

        save_metadata(final_path, os.path.basename(fbx_path), rot, scale)

        yolo_out = os.path.join("annotations/yolo", Path(final_path).stem + ".txt")
        export_yolo(final.size, get_bbox(final), yolo_out)
        print(f"YOLO annotation: {yolo_out}")

        coco_path = os.path.join("annotations/coco", "dataset.json")
        export_coco(coco_path, final_path, get_bbox(final))
        print(f"COCO annotation updated in: {coco_path}")

    print("✅ Dataset generation complete.")