import bpy
import os

framecount = 100

resx = 500; #1920 
resy = 500; #1080

title_width = 502
title_height = 338

video_width = 640
video_height = 480

def createTransform( name, start, end ):
    bpy.ops.sequencer.effect_strip_add( frame_start=start, frame_end=end, type='TRANSFORM' )
    bpy.context.scene.sequence_editor.sequences_all["Transform"].name = name

def createColor( name, start, end, r, g, b ):
    bpy.ops.sequencer.effect_strip_add( frame_start=start, frame_end=end, type='COLOR' )
    bpy.context.scene.sequence_editor.sequences_all["Color"].name = name
    bpy.context.scene.sequence_editor.sequences_all[name].color = (r,g,b)

def loadImageSequence( name, start, directory ):
    candidates = []
    c = 0
    lst = os.listdir( bpy.path.abspath( directory ) )
    for item in lst:
        fileName, fileExtension = os.path.splitext( lst[c] )
        if fileExtension == ".jpg":
            candidates.append(item)
        c = c + 1
    candidates.sort()
    file = [{"name":i} for i in candidates]
    n = len(file)
    bpy.ops.sequencer.image_strip_add( directory = directory, files = file, frame_start=start, frame_end=start+n-1 )
    bpy.context.scene.sequence_editor.sequences_all[ file[ 0 ][ "name" ] ].name = name
    return start+n

def loadBackground( directory, video ):
    bpy.ops.sequencer.movie_strip_add( 
            filepath=directory,
            files=[{ "name": video }]
            relative_path=True,
            sound=False )
    bpy.context.scene.sequence_editor.sequences_all["capture.avi"].mute = True
    createTransform( "background_transform", 0, 25 )
    bpy.context.scene.sequence_editor.sequences_all["background_transform"].scale_start_x = 1
    bpy.context.scene.sequence_editor.sequences_all["background_transform"].scale_start_y = (video_height / video_width) / ( resy / resx )

bpy.data.scenes["Scene"].render.resolution_x = resx 
bpy.data.scenes["Scene"].render.resolution_y = resy 
bpy.data.scenes["Scene"].render.resolution_percentage = 100 

loadBackground( "//", "capture.avi" )

#createColor( "rouge", 0, 250, 1, 0, 0 )
framecount = loadImageSequence( "escargot", 0, "//anim" )
bpy.ops.sequencer.strip_modifier_add( type='BRIGHT_CONTRAST' )
bpy.context.scene.sequence_editor.sequences_all[ "escargot" ].modifiers["Bright/Contrast"].bright = 10
bpy.context.scene.sequence_editor.sequences_all[ "escargot" ].modifiers["Bright/Contrast"].contrast = 101

bpy.context.scene.sequence_editor.sequences_all[ "escargot" ].mute = True
createColor( "rouge", 0, framecount, 1,0,0 )
bpy.ops.sequencer.strip_modifier_add( type='MASK' )
bpy.context.scene.sequence_editor.sequences_all[ "rouge" ].modifiers["Mask"].input_mask_strip = bpy.context.scene.sequence_editor.sequences_all[ "escargot" ]
bpy.context.scene.sequence_editor.sequences_all[ "rouge" ].blend_type = 'ALPHA_OVER'


bpy.data.scenes["Scene"].frame_start = 0
bpy.data.scenes["Scene"].frame_end = framecount-1

bpy.data.scenes["Scene"].render.filepath = "//output/"
bpy.data.scenes["Scene"].render.image_settings.file_format = 'TIFF'
bpy.ops.render.render( animation=True ) 

'''
bpy.ops.sequencer.movie_strip_add( 
    filepath="//capture.avi",
    relative_path=True,
    sound=False )
#bpy.context.scene.sequence_editor.sequences_all["capture.avi"].use_translation = True
bpy.context.scene.sequence_editor.sequences_all["capture.avi"].mute = True
createTransform( "video_transform", 0, 25 )
#bpy.context.scene.sequence_editor.sequences_all["Transform"].blend_type = 'ALPHA_OVER'
bpy.context.scene.sequence_editor.sequences_all["video_transform"].scale_start_x = 1
bpy.context.scene.sequence_editor.sequences_all["video_transform"].scale_start_y = (video_height / video_width) / ( resy / resx )

bpy.ops.sequencer.image_strip_add( 
    directory="//",
    files=[{"name":"typotitregros.png"}],
    relative_path=True,
    frame_start=0,
    frame_end=25,
    channel=4 )
createTransform( "title_transform", 0, 25 )
bpy.context.scene.sequence_editor.sequences_all["typotitregros.png"].mute = True
bpy.context.scene.sequence_editor.sequences_all["title_transform"].blend_type = 'ALPHA_OVER'
bpy.context.scene.sequence_editor.sequences_all["title_transform"].scale_start_y = (title_height / title_width) / ( resy / resx )


bpy.data.scenes["Scene"].frame_end = framecount
bpy.data.scenes["Scene"].render.image_settings.file_format = 'AVI_JPEG' 
bpy.data.scenes["Scene"].render.filepath = "//" 
bpy.ops.render.render( animation=True ) 
'''

# print( bpy.context.scene.sequence_editor.sequences_all["typotitregros.png"].transform )
# print( bpy.context.scene.sequence_editor.sequences_all["//typotitregros.png"] )
'''
for seq in bpy.context.scene.sequence_editor.sequences_all:
     if hasattr(seq, "elements"):
          for elem in seq.elements:
               print(elem, elem.orig_width, elem.orig_height)
               elem.orig_width = 100
'''