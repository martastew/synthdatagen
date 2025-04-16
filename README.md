# SynthTarget

Generate synthetic datasets using 3D models, AI backgrounds, weather effects and export YOLO/COCO annotations.

## Features

- Load FBX 3D models
- Render with Blender using Python API
- Add fog, rain, or snow effects
- Use DALL·E or static backgrounds
- Export YOLO and COCO annotation formats
- Store generation metadata (rotation, scale, file info)

## Installation

```bash
git clone <your_repo_url>
cd synthtarget
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt