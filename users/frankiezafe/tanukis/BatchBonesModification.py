import bpy

# name of the armature
ARMATURE_NAME = 'armature_skeleton'
NAME_FILTER = [ '_body' ] # AND clause

def doContinue( name ):
    global NAME_FILTER
    if len(NAME_FILTER) == 0:
        return True
    allchecked = True
    for n in NAME_FILTER:
        if name.find( n ) == -1:
            allchecked = False
            break
    return allchecked

scn = bpy.context.scene
armature = scn.objects[ ARMATURE_NAME ]

# modification on bones
# modifiable params are listed in doc
# https://www.blender.org/api/blender_python_api_2_77_release/bpy.types.Bone.html#bpy.types.Bone
print( '**** bones:', len(armature.pose.bones) )
for b in armature.data.bones:
    if not doContinue( b.name ):
        continue
    print( b.name )
    b.use_inherit_rotation = True
    b.use_inherit_scale = False

# modification on pose bones
# modifiable params are listed in doc
# https://www.blender.org/api/blender_python_api_2_77_release/bpy.types.PoseBone.html
print( '**** pose bones:', len(armature.pose.bones) )
for pb in armature.pose.bones:
    if not doContinue( pb.name ):
        continue
    print( pb.name )
    pb.lock_location = (False,False,False)
    pb.lock_rotation = (False,False,False)
    pb.lock_scale = (False,False,False)
    
