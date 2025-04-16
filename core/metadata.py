import json, os
from pathlib import Path

def save_metadata(image_path, model, rotation, scale, output_dir="annotations"):
    metadata_file = os.path.join(output_dir, "metadata.json")
    Path(output_dir).mkdir(exist_ok=True)

    entry = {
        "image": image_path,
        "model": model,
        "rotation": {"x": rotation[0], "y": rotation[1], "z": rotation[2]},
        "scale": scale
    }

    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(metadata_file, "w") as f:
        json.dump(data, f, indent=4)