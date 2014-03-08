import bpy

resx = 200; #1920 
resy = 200; #1080 
bpy.data.scenes["Scene"].render.resolution_x = resx 
bpy.data.scenes["Scene"].render.resolution_y = resy 
bpy.data.scenes["Scene"].render.resolution_percentage = 100 

bpy.ops.sequencer.movie_strip_add( 
    filepath="//capture.avi",
    relative_path=True,
    sound=False )

bpy.ops.sequencer.image_strip_add( 
    directory="//",
    files=[{"name":"typotitregros.png"}],
    relative_path=True,
    frame_start=0,
    frame_end=25,
    channel=4 )

bpy.context.scene.sequence_editor.sequences_all["typotitregros.png"].blend_type = 'ALPHA_OVER'

# print( bpy.context.scene.sequence_editor.sequences_all["typotitregros.png"].transform )
# print( bpy.context.scene.sequence_editor.sequences_all["//typotitregros.png"] )

for seq in bpy.context.scene.sequence_editor.sequences_all:
     if hasattr(seq, "elements"):
          for elem in seq.elements:
               print(elem, elem.orig_width, elem.orig_height)
               elem.orig_width = 100
