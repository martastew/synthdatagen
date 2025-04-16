import gradio as gr
import os
import shutil
import subprocess
from generate_dataset import generate_synthetic_dataset
from core.ai_background import generate_background

UPLOAD_DIR = "uploads"
BACKGROUND_DIR = "backgrounds"
GENERATED_DIR = "generated"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(BACKGROUND_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)

def convert_fbx_to_glb(fbx_path):
    glb_path = fbx_path.replace(".fbx", ".glb")
    blender_script = "core/fbx_to_glb.py"
    subprocess.run([
        "blender", "--background", "--python", blender_script, "--", fbx_path, glb_path
    ], check=True)
    return glb_path

def pipeline(fbx_file, prompt, selected_bg, num_images, weather_effect):
    if fbx_file is None:
        return "❌ Please upload a 3D model", [], None

    ext = os.path.splitext(fbx_file.name)[-1].lower()
    fbx_path = os.path.join(UPLOAD_DIR, os.path.basename(fbx_file.name))
    shutil.copyfile(fbx_file.name, fbx_path)

    if ext == ".fbx":
        try:
            model_preview = convert_fbx_to_glb(fbx_path)
        except Exception as e:
            model_preview = None
    else:
        model_preview = fbx_path

    bg_path = None
    if selected_bg is not None:
        bg_path = os.path.join(BACKGROUND_DIR, os.path.basename(selected_bg.name))
        shutil.copyfile(selected_bg.name, bg_path)
    elif prompt:
        try:
            bg_path = generate_background(prompt, size="1024x1024", save_dir=BACKGROUND_DIR)
        except Exception as e:
            return f"⚠️ Failed to generate background: {str(e)}", [], model_preview

    generate_synthetic_dataset(
        fbx_path=fbx_path,
        backgrounds_dir=BACKGROUND_DIR,
        selected_bg_path=bg_path,
        num=num_images,
        weather=weather_effect
    )

    previews = sorted([
        os.path.join(GENERATED_DIR, f)
        for f in os.listdir(GENERATED_DIR)
        if f.endswith("_final.png")
    ], key=os.path.getmtime, reverse=True)[:3]

    return f"✅ Generated {num_images} images from: {os.path.basename(fbx_file.name)}", previews, model_preview

with gr.Blocks() as demo:
    gr.Markdown("# 🛠️ SynthTarget: Synthetic 3D Dataset Generator")

    with gr.Row():
        fbx_file = gr.File(label="Upload .fbx, .glb or .obj 3D Model", file_types=[".fbx", ".glb", ".obj"])
        model_viewer = gr.Model3D(label="Preview Model")

    with gr.Row():
        prompt = gr.Textbox(label="Prompt for AI background (optional)", placeholder="futuristic desert base")
        selected_bg = gr.File(label="Or Upload Custom Background", file_types=[".jpg", ".jpeg", ".png"])

    with gr.Row():
        weather_effect = gr.Radio(label="Weather Effect", choices=["none", "fog", "rain", "snow"], value="none")
        num_images = gr.Slider(minimum=1, maximum=10, value=3, label="Number of images")

    generate_btn = gr.Button("Generate Dataset")
    status = gr.Textbox(label="Status")
    gallery = gr.Gallery(label="Preview of Generated Images", columns=3, rows=1, height=200)

    generate_btn.click(
        pipeline,
        inputs=[fbx_file, prompt, selected_bg, num_images, weather_effect],
        outputs=[status, gallery, model_viewer]
    )

if __name__ == "__main__":
    demo.launch(share=True)