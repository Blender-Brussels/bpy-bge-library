import bpy
import os

resx = 200;
resy = 200;

animation_folder = "//anim/"

background_folder = "//"
background_video = "capture.avi"
background_video_width = 640
background_video_height = 480

filter_brightness = 10
filter_contrast = 101
filter_color = ( 1,0,1 )

output_folder = "//output/"
output_format = "TIFF"

def createTransform( name, start, end ):
    bpy.ops.sequencer.effect_strip_add( frame_start=start, frame_end=end, type='TRANSFORM' )
    bpy.context.scene.sequence_editor.sequences_all["Transform"].name = name

def createColor( name, start, end, color ):
    bpy.ops.sequencer.effect_strip_add( frame_start=start, frame_end=end, type='COLOR' )
    bpy.context.scene.sequence_editor.sequences_all["Color"].name = name
    bpy.context.scene.sequence_editor.sequences_all[name].color = color

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

def loadBackground( directory, video, vwith, vheight ):
    bpy.ops.sequencer.movie_strip_add( 
            filepath=directory,
            files=[{ "name": video }],
            sound=False )
    bpy.context.scene.sequence_editor.sequences_all[ video ].mute = True
    createTransform( "background_transform", 0, 25 )
    ratioscene = resy / resx
    ratiovideo = vheight / vwith
    if ( ratioscene < ratiovideo ):
        bpy.context.scene.sequence_editor.sequences_all["background_transform"].scale_start_y = ( vheight / vwith ) / ( resy / resx )
    else:
        bpy.context.scene.sequence_editor.sequences_all["background_transform"].scale_start_x = ( vwith / vheight ) / ( resx / resy )

bpy.data.scenes["Scene"].render.resolution_x = resx 
bpy.data.scenes["Scene"].render.resolution_y = resy 
bpy.data.scenes["Scene"].render.resolution_percentage = 100 

loadBackground( background_folder, background_video, background_video_width, background_video_height )

framecount = loadImageSequence( "animation", 0, "//anim/" )
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