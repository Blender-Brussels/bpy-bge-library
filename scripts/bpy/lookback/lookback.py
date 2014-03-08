###################################################################
# this script 
# 1. loads a video file and scale it (keeping the  aspect ratio)
# 2. loads a list of image into the sequencer
# 3. use them as a mask on a plain color layer
# 4. launch the video rendering (here configure as a TIFF sequence) 
###################################################################

import bpy
import os

# folder containing image files to load
animation_folder = "//anim/"
animation_format = ".jpg"
# fine-tuning of the image
filter_brightness = 10
filter_contrast = 101
# color of the lines, RGB values ( 1 means full color, 0 means no color on the channel )
filter_color = ( 0,1,0 )

# video to place in background
background_folder = "//"
background_video = "capture.avi"
background_video_width = 640
background_video_height = 480

# output configuration
output_width = 200;
output_height = 200;
output_folder = "//output/"
output_format = "TIFF"

def createTransform( name, start, end ):
    bpy.ops.sequencer.effect_strip_add( frame_start=start, frame_end=end, type='TRANSFORM' )
    bpy.context.scene.sequence_editor.sequences_all["Transform"].name = name

def createColor( name, start, end, color ):
    bpy.ops.sequencer.effect_strip_add( frame_start=start, frame_end=end, type='COLOR' )
    bpy.context.scene.sequence_editor.sequences_all["Color"].name = name
    bpy.context.scene.sequence_editor.sequences_all[name].color = color

def loadImageSequence( name, start, directory, ext ):
    candidates = []
    c = 0
    lst = os.listdir( bpy.path.abspath( directory ) )
    for item in lst:
        fileName, fileExtension = os.path.splitext( lst[c] )
        if fileExtension == ext:
            candidates.append(item)
        c = c + 1
    candidates.sort()
    file = [{"name":i} for i in candidates]
    n = len(file)
    bpy.ops.sequencer.image_strip_add( directory = directory, files = file, frame_start=start, frame_end=start+n-1 )
    bpy.context.scene.sequence_editor.sequences_all[ file[ 0 ][ "name" ] ].name = name
    return start+n

def loadBackground( directory, video, vwith, vheight ):
    bpy.ops.sequencer.movie_strip_add( 
            filepath=directory,
            files=[{ "name": video }],
            sound=False )
    bpy.context.scene.sequence_editor.sequences_all[ video ].mute = True
    createTransform( "background_transform", 0, 25 )
    ratioscene = output_height / output_width
    ratiovideo = vheight / vwith
    if ( ratioscene < ratiovideo ):
        bpy.context.scene.sequence_editor.sequences_all["background_transform"].scale_start_y = ( vheight / vwith ) / ( output_height / output_width )
    else:
        bpy.context.scene.sequence_editor.sequences_all["background_transform"].scale_start_x = ( vwith / vheight ) / ( output_height / output_width )

bpy.data.scenes["Scene"].render.resolution_x = output_width 
bpy.data.scenes["Scene"].render.resolution_y = output_height 
bpy.data.scenes["Scene"].render.resolution_percentage = 100 

loadBackground( background_folder, background_video, background_video_width, background_video_height )

framecount = loadImageSequence( "animation", 0, animation_folder, animation_format )
bpy.ops.sequencer.strip_modifier_add( type='BRIGHT_CONTRAST' )
bpy.context.scene.sequence_editor.sequences_all[ "animation" ].modifiers["Bright/Contrast"].bright = filter_brightness
bpy.context.scene.sequence_editor.sequences_all[ "animation" ].modifiers["Bright/Contrast"].contrast = filter_contrast
bpy.context.scene.sequence_editor.sequences_all[ "animation" ].mute = True

createColor( "color", 0, framecount, filter_color )
bpy.ops.sequencer.strip_modifier_add( type='MASK' )
bpy.context.scene.sequence_editor.sequences_all[ "color" ].modifiers["Mask"].input_mask_strip = bpy.context.scene.sequence_editor.sequences_all[ "animation" ]
bpy.context.scene.sequence_editor.sequences_all[ "color" ].blend_type = 'ALPHA_OVER'

bpy.data.scenes["Scene"].frame_start = 0
bpy.data.scenes["Scene"].frame_end = framecount-1

bpy.data.scenes["Scene"].render.filepath = output_folder
bpy.data.scenes["Scene"].render.image_settings.file_format = output_format
bpy.ops.render.render( animation=True )
