import json, os, uuid

def export_coco(coco_path, image_path, bbox, category_id=1):
    w, h = 512, 512  # update if using dynamic sizes
    image_id = str(uuid.uuid4())
    x1, y1, x2, y2 = bbox

    coco_data = {
        "images": [
            {
                "id": image_id,
                "file_name": os.path.basename(image_path),
                "width": w,
                "height": h
            }
        ],
        "annotations": [
            {
                "id": str(uuid.uuid4()),
                "image_id": image_id,
                "category_id": category_id,
                "bbox": [x1, y1, x2 - x1, y2 - y1],
                "area": (x2 - x1) * (y2 - y1),
                "iscrowd": 0
            }
        ],
        "categories": [
            {
                "id": category_id,
                "name": "object"
            }
        ]
    }

    with open(coco_path, "w") as f:
        json.dump(coco_data, f, indent=4)