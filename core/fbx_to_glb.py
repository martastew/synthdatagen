import bpy
import sys

fbx_in = sys.argv[-2]
glb_out = sys.argv[-1]

bpy.ops.import_scene.fbx(filepath=fbx_in)
bpy.ops.export_scene.gltf(filepath=glb_out, export_format='GLB')