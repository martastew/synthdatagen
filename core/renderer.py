# core/renderer.py

import subprocess
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Path to Blender executable from .env
BLENDER_PATH = os.getenv("BLENDER_PATH")

def render_model(model_path, output_dir, rot_x=0, rot_y=0, rot_z=0, scale=1.0, bg_path=None):
    """
    Launches Blender in background mode to render the model with given rotation and scale.
    Optionally includes a background image.

    Parameters:
    - model_path: Path to .fbx/.glb/.obj 3D model
    - output_dir: Where to save the rendered PNG
    - rot_x/y/z: Euler rotation in degrees
    - scale: Scale factor
    - bg_path: Optional path to a background image

    Returns:
    - Path to rendered .png file
    """
    render_id = str(uuid.uuid4())
    out_path = os.path.abspath(os.path.join(output_dir, f"{render_id}.png"))

    args = [
        BLENDER_PATH,
        "--background",
        "--python", "core/blender_render.py",  # ✅ Correct Blender script filename
        "--",
        model_path,
        out_path,
        str(rot_x),
        str(rot_y),
        str(rot_z),
        str(scale)
    ]

    if bg_path:
        args.append(bg_path)

    subprocess.run(args, check=True)
    return out_path