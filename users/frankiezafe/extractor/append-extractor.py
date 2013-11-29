import bpy

print( "/////////////////////////////////////////" )

extractor = bpy.ops.text.open( filepath = "/home/frankiezafe/PROJECTS/blender-python/bpy-bge-library/users/frankiezafe/extractor/extractor.py", internal = True )

print( bpy.data.texts[0] )
print( extractor )
