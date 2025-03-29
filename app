import gradio as gr
from PIL import Image, ImageEnhance
import numpy as np
import io

def blend_model_with_background(model_file, background_image, angle, scale):
    if not model_file or not background_image:
        return "Please upload both model and background"

    # Mock result: overlay simulation
    background = Image.open(background_image).convert("RGBA")
    overlay = Image.new("RGBA", background.size, (255, 0, 0, 100))  # translucent red for model area

    # Simulate angle + scale by modifying brightness as a placeholder
    enhancer = ImageEnhance.Brightness(overlay)
    overlay = enhancer.enhance(0.5 + scale * 0.1)

    blended = Image.alpha_composite(background, overlay)
    return blended

with gr.Blocks() as demo:
    gr.Markdown("MLRS Blending Pipeline")

    with gr.Row():
        model_file = gr.File(label="Upload MSLR 3D Model (stub)", file_types=[".obj", ".glb", ".fbx"])
        background_image = gr.Image(label="Upload Background Image")

    with gr.Row():
        angle = gr.Slider(0, 360, value=0, label="Rotation Angle (°)")
        scale = gr.Slider(0.1, 3.0, value=1.0, label="Scale")

    blend_button = gr.Button("Start Blending")
    output_image = gr.Image(label="Blended Output")

    blend_button.click(
        fn=blend_model_with_background,
        inputs=[model_file, background_image, angle, scale],
        outputs=output_image
    )

    gr.Markdown("Next steps: add real 3D rendering, segmentation mask integration, and export functions.")

demo.launch()
