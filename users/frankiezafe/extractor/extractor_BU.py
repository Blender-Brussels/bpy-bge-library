import bpy

print( "EXTRACTOR LOADED!!" )

folder = bpy.path.abspath( "//" )
# print( bpy.data.filepath )
# print( bpy.path.abspath( "//" ) )

print( "DATA: ", bpy.data )
print( "SCENES: ", len( bpy.data.scenes ), ":", bpy.data.scenes )
print( "OBJECTS: ", len( bpy.data.objects ), ":", bpy.data.texts )
print( "TEXTS: ", len( bpy.data.texts ), ":", bpy.data.texts )
print( "IMAGES: ", len( bpy.data.images ), ":", bpy.data.images )
print( "FILES: ", len( bpy.data.filepath ), ":", bpy.data.filepath )
print( "LIBRARIES: ", len( bpy.data.libraries ), ":", bpy.data.libraries )

print( "\nscenes\n******" )
for s in bpy.data.scenes:
	print( s )

print( "\nobjects\n******" )
for o in bpy.data.objects:
	print( o )

print( "\ntexts\n******" )
for t in range( 0, len( bpy.data.texts ) ):
	ct = bpy.data.texts[ t ]
	f = open( folder + ct.name, 'w' )
	f.write( ct.as_string() )
	f.close()
	print( ct.name , ">" , bpy.data.texts[ t ] )

print( "\nimages\n******" )
for o in bpy.data.images:
	print( o )

print( "\nlibraries\n******" )
for o in bpy.data.libraries:
	print( o )

