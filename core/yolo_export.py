def export_yolo(image_size, bbox, output_path, class_id=0):
    w, h = image_size
    x1, y1, x2, y2 = bbox

    x_center = (x1 + x2) / 2 / w
    y_center = (y1 + y2) / 2 / h
    box_w = (x2 - x1) / w
    box_h = (y2 - y1) / h

    with open(output_path, "w") as f:
        f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_w:.6f} {box_h:.6f}\\n")