def selectVertices( o ):
	# http://blenderartists.org/forum/archive/index.php/t-207542.html see "Crouch" first post
	# first of all: selecting the object
	bpy.ops.object.mode_set(mode='OBJECT')
	o.select = True
	# switching to edit, deselecting everything and setting the mode to vertices (tool_settings)
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.context.tool_settings.mesh_select_mode = (True, False, False)
	bpy.ops.mesh.select_all(action = 'DESELECT')
	# everything is deselected -> to update python object, has to switch back to object mode
	bpy.ops.object.mode_set(mode = 'OBJECT')
	# now we can select the vertices
	o.data.vertices[0].select = True
	o.data.vertices[1].select = True
	# and go back to edit mode to apply transformations
	bpy.ops.object.mode_set(mode = 'EDIT')
	bpy.ops.mesh.merge(type='CENTER', uvs=False)
	# to finish nicely: deselecting everything and switch to object mode
	bpy.ops.mesh.select_all(action = 'DESELECT')
	bpy.ops.object.mode_set(mode = 'OBJECT')
