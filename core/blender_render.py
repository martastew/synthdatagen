# core/blender_render.py

import bpy
import sys
import os
import uuid
from math import radians

argv = sys.argv[sys.argv.index("--") + 1:]

model_path = argv[0]
output_path = argv[1]
rot_x, rot_y, rot_z = map(float, argv[2:5])
scale = float(argv[5])
bg_path = argv[6] if len(argv) > 6 else None

# Clear the existing scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import the 3D model
ext = os.path.splitext(model_path)[-1].lower()
if ext == ".fbx":
    bpy.ops.import_scene.fbx(filepath=model_path)
elif ext == ".glb":
    bpy.ops.import_scene.gltf(filepath=model_path)
elif ext == ".obj":
    bpy.ops.import_scene.obj(filepath=model_path)
else:
    raise ValueError(f"Unsupported file format: {ext}")

# Group all imported objects
model_objects = [obj for obj in bpy.context.selected_objects if obj.type in {'MESH', 'EMPTY'}]
model = bpy.data.collections.new("Model")
bpy.context.scene.collection.children.link(model)
for obj in model_objects:
    bpy.context.scene.collection.objects.unlink(obj)
    model.objects.link(obj)

# Transform model
for obj in model.objects:
    obj.rotation_euler = [radians(rot_x), radians(rot_y), radians(rot_z)]
    obj.scale = (scale, scale, scale)

# Set camera above
cam_data = bpy.data.cameras.new(name="Camera")
cam_obj = bpy.data.objects.new("Camera", cam_data)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

cam_obj.location = (0, -6, 6)
cam_obj.rotation_euler = (radians(60), 0, 0)

# Add light
light_data = bpy.data.lights.new(name="Light", type='AREA')
light_obj = bpy.data.objects.new(name="Light", object_data=light_data)
bpy.context.scene.collection.objects.link(light_obj)
light_obj.location = (0, -2, 4)
light_data.energy = 1000

# Add background image as plane
if bg_path:
    bpy.ops.import_image.to_plane(files=[{"name": os.path.basename(bg_path)}], directory=os.path.dirname(bg_path))
    bg_plane = bpy.context.selected_objects[0]
    bg_plane.scale = (5, 5, 1)
    bg_plane.location = (0, 0, 0)
    for obj in model.objects:
        obj.location.z += 1.5  # lift model above plane

# Render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = output_path
scene.render.film_transparent = not bool(bg_path)

# Set resolution
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024

# Render
bpy.ops.render.render(write_still=True)
print(f"✅ Rendered: {output_path}")