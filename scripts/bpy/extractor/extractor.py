import bpy
import os

folder = bpy.path.abspath( "//" )

# creating subfolder for texts, scenes & objets
# note: all images will be unpacked in a 'textures' folder
foldertext = folder+ "texts/"
if not os.path.exists(foldertext):
    os.makedirs(foldertext)

folderscenes = folder+ "scenes/"
if not os.path.exists(folderscenes):
    os.makedirs(folderscenes)

folderobjects = folder+ "objects/"
if not os.path.exists(folderobjects):
    os.makedirs(folderobjects)

# extracting all text blocks found in .blend
for t in range( 0, len( bpy.data.texts ) ):
	ct = bpy.data.texts[ t ]
	f = open( foldertext + ct.name, 'w' )
	f.write( ct.as_string() )
	f.close()

# extracting each scene as .obj/.mtl
for s in bpy.data.scenes:
	bpy.context.screen.scene = s
	bpy.ops.export_scene.obj( filepath = folderscenes + s.name + ".obj", path_mode = "STRIP" )

# extracting each object as .stl
for o in bpy.data.objects:
	if o.type == "MESH":
		o.select = True
		bpy.ops.export_mesh.stl( filepath = folderobjects + o.name + ".stl" )
		o.select = False

# extracting all packed files
bpy.ops.file.unpack_all( method = "USE_LOCAL" )

