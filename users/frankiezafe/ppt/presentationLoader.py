import bpy
import os
import xml.etree.ElementTree as ET

from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       FloatProperty,
                       CollectionProperty,
                       )

from bpy_extras.image_utils import load_image


# copy/paste and dirty hack of blender-2.70-linux-glibc211-x86_64/2.70/scripts/addons/io_import_images_as_planes.py 

def set_texture_options( context, texture ):
    #texture.image.use_alpha = BoolProperty(name="Use Alpha", default=False, description="Use alphachannel for transparency")
    texture.image.use_alpha = False
    #texture.image_user.use_auto_refresh = bpy.types.ImageUser.bl_rna.properties["use_auto_refresh"]
    texture.image_user.use_auto_refresh = True
    ctx = context.copy()
    ctx["edit_image"] = texture.image
    ctx["edit_image_user"] = texture.image_user
    bpy.ops.image.match_movie_length(ctx)

def set_material_options( material, slot):
    material.alpha = 1.0
    material.specular_alpha = 1.0
    slot.use_map_alpha = False
    #material.use_transparency = BoolProperty(name="Use Alpha", default=False, description="Use alphachannel for transparency")
    material.use_transparency = False
    #t = bpy.types.Material.bl_rna.properties["transparency_method"]
    #items = tuple((it.identifier, it.name, it.description) for it in t.enum_items)
    #material.transparency_method = EnumProperty(name="Transp. Method", description=t.description, items=items)
    #t = bpy.types.Material.bl_rna.properties["use_shadeless"]
    #material.use_shadeless = BoolProperty(name=t.name, default=False, description=t.description)
    #t = bpy.types.Material.bl_rna.properties["use_transparent_shadows"]
    #material.use_transparent_shadows = BoolProperty(name=t.name, default=False, description=t.description)

def create_image_textures( context, image):
    fn_full = os.path.normpath(bpy.path.abspath(image.filepath))
    # look for texture with importsettings
    for texture in bpy.data.textures:
        if texture.type == 'IMAGE':
            tex_img = texture.image
            if (tex_img is not None) and (tex_img.library is None):
                fn_tex_full = os.path.normpath(bpy.path.abspath(tex_img.filepath))
                if fn_full == fn_tex_full:
                    set_texture_options(context, texture)
                    return texture

    # if no texture is found: create one
    name_compat = bpy.path.display_name_from_filepath(image.filepath)
    texture = bpy.data.textures.new(name=name_compat, type='IMAGE')
    texture.image = image
    set_texture_options(context, texture)
    return texture

def create_material_for_texture( texture):
    # look for material with the needed texture
    for material in bpy.data.materials:
        slot = material.texture_slots[0]
        if slot and slot.texture == texture:
            set_material_options(material, slot)
            return material

    # if no material found: create one
    name_compat = bpy.path.display_name_from_filepath(texture.image.filepath)
    material = bpy.data.materials.new(name=name_compat)
    slot = material.texture_slots.add()
    slot.texture = texture
    slot.texture_coords = 'UV'
    set_material_options(material, slot)
    return material

def img2plane( folder, filename ):
    
    if filename not in bpy.data.images:
        # no need to reload the image, it is already in the memory!
        f = load_image( bpy.path.abspath( folder + filename ) )
    
    if filename not in bpy.data.images:
        print( "filename:", filename, "NOT FOUND!" )
        return
    
    img = bpy.data.images[ filename ]
    #print( img, img.generated_width, img.generated_height, img.size )
    
    ratio = img.size[ 0 ] / img.size[ 1 ]
    #print( ratio )
    
    scalew = ratio
    scaleh = 1
    '''
    if ratio > 1:
        scaleh = 1 / ratio
    else:
        scalew = 1 / ratio
    '''
    
    texture = create_image_textures( bpy.context, img )
    material = create_material_for_texture( texture )
    
    bpy.ops.mesh.primitive_plane_add('INVOKE_REGION_WIN')
    plane = bpy.context.scene.objects.active
    if plane.mode is not 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    plane.dimensions = scalew, scaleh, 0.0
    plane.name = material.name
    bpy.ops.object.transform_apply(scale=True)
    plane.data.uv_textures.new()
    plane.data.materials.append(material)
    plane.data.uv_textures[0].data[0].image = img
    
    material.game_settings.use_backface_culling = False
    material.game_settings.alpha_blend = 'ALPHA'
    
    return plane

def video2plane( folder, filename ):
    
    if "video_init" not in bpy.data.texts:
        print( "creation of a 'video_init' text block" )
    
    if "video_update" not in bpy.data.texts:
        print( "creation of a 'video_init' text block" )
    
    p = img2plane( folder, filename )
    bpy.ops.object.select_all( action='DESELECT' )
    p.select = True
    if p.mode is not 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.game_property_new( type='STRING', name="video_path" )
    prop = p.game.properties['video_path']
    prop.value = bpy.path.abspath( folder + filename )
    
    bpy.ops.logic.controller_add( type='PYTHON', name='py_init')
    p.game.controllers['py_init'].text = bpy.data.texts["loadVideo.py"]

    bpy.ops.logic.controller_add( type='PYTHON', name='py_update')
    p.game.controllers['py_update'].text = bpy.data.texts["updateVideo.py"]

    bpy.ops.logic.sensor_add( type='ALWAYS', name='init' )
    p.game.sensors[ 'init' ].link( p.game.controllers['py_init'] )
    
    bpy.ops.logic.sensor_add( type='ALWAYS', name='update' )
    p.game.sensors[ 'update' ].link( p.game.controllers['py_update'] )
    p.game.sensors[ 'update' ].use_pulse_true_level = True
    
    return p

slides = []
page = ET.parse( bpy.path.abspath( '//' + 'presentation.xml' ) )

slideIndex = 0
for p in page.getiterator():
    
    if p.tag == "img":
        print( "loading image: ", p.attrib["src"] )
        s = img2plane( "//", p.attrib["src"] )
        s.name = "slide_" + slideIndex
        slides.append( s )
        slideIndex += 1
        
    if p.tag == "text":
        '''
        in
        '''
        
    if p.tag == "video":
        print( "loading video: ", p.attrib["src"] )
        s = video2plane( "//", p.attrib["src"] )
        s.name = "slide_" + slideIndex
        slides.append( s )
        slideIndex += 1
        
# rearrange sildes
offsetx = 0
for s in slides:
    print( "moving", s.name )
    bpy.ops.object.select_all( action='DESELECT' )
    s.select = True
    if s.mode is not 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.transform.translate( value = ( offsetx * 2, 0, 0 ) )
    offsetx += 1
    

for i in bpy.data.images:
    print( i )
for i in bpy.data.movieclips:
    print( i )