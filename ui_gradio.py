import gradio as gr
from PIL import Image, ImageEnhance
import numpy as np
import io
import random

def apply_weather_effect(image: Image.Image, weather: str) -> Image.Image:
    width, height = image.size
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))

    if weather == "Snow":
        for _ in range(500):
            x = random.randint(0, width)
            y = random.randint(0, height)
            overlay.putpixel((x, y), (255, 255, 255, 180))
    elif weather == "Rain":
        for _ in range(300):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 10)
            for i in range(10):
                overlay.putpixel((x, y + i), (100, 100, 255, 100))
    elif weather == "Fog":
        fog_layer = Image.new("RGBA", image.size, (200, 200, 200, 100))
        overlay = Image.alpha_composite(overlay, fog_layer)

    return Image.alpha_composite(image, overlay)

def render_model_placeholder(angle, scale):
    # This is a placeholder for true 3D rendering
    canvas = Image.new("RGBA", (512, 512), (150, 150, 150, 255))
    shape = Image.new("RGBA", (200, 100), (255, 0, 0, 255))
    shape = shape.rotate(angle, expand=True)
    shape = shape.resize((int(200 * scale), int(100 * scale)))
    canvas.paste(shape, (156, 206), shape)
    return canvas

def blend_model_with_background(model_file, background_image, angle, scale, weather):
    if not background_image:
        return "Please upload background image"

    # Render fake model
    model_image = render_model_placeholder(angle, scale)

    # Blend model onto background
    background = Image.open(background_image).convert("RGBA")
    background = background.resize((512, 512))
    composite = Image.alpha_composite(background, model_image)

    # Apply weather
    final = apply_weather_effect(composite, weather)
    return final

with gr.Blocks() as demo:
    gr.Markdown("Blending Pipeline with Weather Effects and Model Rotation")

    with gr.Row():
        model_file = gr.File(label="Upload MSLR 3D Model (stub)", file_types=[".obj", ".glb", ".fbx"])
        background_image = gr.Image(label="Upload Background Image")

    with gr.Row():
        angle = gr.Slider(0, 360, value=0, label="Rotation Angle (°)")
        scale = gr.Slider(0.1, 3.0, value=1.0, label="Scale")
        weather = gr.Radio(["None", "Snow", "Rain", "Fog"], label="Weather Effect")

    blend_button = gr.Button("Start Blending")
    output_image = gr.Image(label="Blended Output")

    blend_button.click(
        fn=blend_model_with_background,
        inputs=[model_file, background_image, angle, scale, weather],
        outputs=output_image
    )

    gr.Markdown("This demo uses placeholder rendering. For true rendering, integrate Three.js or Blender Python API to render .obj/.glb files with lighting and environment.")

demo.launch()
