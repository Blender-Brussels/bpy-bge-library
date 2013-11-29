import bpy
import os

folder = bpy.path.abspath( "//" )

# creating subfolder for texts
foldertext = folder+ "texts/"
if not os.path.exists(foldertext):
    os.makedirs(foldertext)

# extracting all text blocks found in .blend
for t in range( 0, len( bpy.data.texts ) ):
	ct = bpy.data.texts[ t ]
	f = open( foldertext + ct.name, 'w' )
	f.write( ct.as_string() )
	f.close()

# extracting all packed files
bpy.ops.file.unpack_all( method = "USE_LOCAL" )
