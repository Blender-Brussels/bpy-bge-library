# to apply : 
# - me = bpy.context.active_object.data
# - me.materials.append( mat )
# - me.update()
# frankiezafe@gmail.com

def generateMaterial():
	texturefolder = "//folder/"
	texturefile = "filename.tiff"
	texturename = "text_name"
	materialname = "mat_name"
	bpy.ops.image.open( filepath = texturefolder+texturefile, relative_path = True )
	textureimage = bpy.data.images[texturefile]
	iTex = bpy.data.textures.new(texturename, type = 'IMAGE')
	iTex.image = textureimage
	iTex.use_alpha = 0
	mat = bpy.data.materials.new( materialname )
	mat.diffuse_color = ( 0,0,0 )
	mat.specular_intensity = 0
	mat.use_transparency = True
	mat.transparency_method = 'Z_TRANSPARENCY'
	mat.alpha = 0
	mtex = mat.texture_slots.add()
	mtex.texture = iTex
	# comment line below to use basic coords (generated)
	mtex.texture_coords = 'UV'
	mtex.use_map_color_diffuse = False
	mtex.use_map_alpha = True
	mtex.mapping = 'FLAT'
	mtex.offset = [ 0, 0, 0 ]
	mtex.scale = [ 1, 1, 1 ]
	return mat
