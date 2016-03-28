import bpy

# right and left markers
NEEDLE = "R_"
REPLACE = "L_"

# name of the armature and the related mesh
ARMATURE_NAME = 'armature_skeleton'
MESH_NAME = 'skeleton'

scn = bpy.context.scene
armature = scn.objects[ ARMATURE_NAME ].data
mesh = scn.objects[ MESH_NAME ]

# renaming all bones
print( "armature:", ARMATURE_NAME, armature )
for b in armature.bones:
    b.name = b.name.replace( NEEDLE, REPLACE )
    print( b.name )
    
# renaming all vertex groups
print( "mesh:", MESH_NAME, mesh )
for vg in mesh.vertex_groups:
    vg.name = vg.name.replace( NEEDLE, REPLACE )
    print( vg.name )
