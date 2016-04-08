import bpy

# name of the armature and the related mesh
ARMATURE_NAME = 'armature_skeleton'
MESH_NAME = 'skeleton'
REMOVE_VERTEXGROUPS = True

scn = bpy.context.scene
armature = scn.objects[ ARMATURE_NAME ].data
mesh = scn.objects[ MESH_NAME ]

print( mesh.vertex_groups )

# creation of missing vertex groups
for b in armature.bones:
    found = False
    for vg in mesh.vertex_groups:
        if vg.name == b.name:
            found = True
    if found == False:
        mesh.vertex_groups.new( b.name )
        print( b.name, "vertex group created" )

# deletion of vertex groups
if REMOVE_VERTEXGROUPS == True:
    for vg in mesh.vertex_groups:
        found = False
        for b in armature.bones:
            if vg.name == b.name:
                found = True
        if found == False:
            print( vg.name, "vertex group removed" )
            mesh.vertex_groups.remove( vg )
