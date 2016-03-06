import bpy, math
from mathutils import Vector, Matrix

# configuration
ARMATURE_NAME = 'makehuman'
BONE_NAME = 'RightArm'

# getting the right bone, no safety net...
scn = bpy.context.scene
armature = scn.objects[ ARMATURE_NAME ].data
bone = armature.bones[ BONE_NAME ]

# orientation of the bone is represented as a 4x4 matrix
# see https://www.blender.org/api/blender_python_api_2_59_0/bpy.types.Bone.html#bpy.types.Bone.matrix_local
bone_mat = bone.matrix_local

# getting the active object
target = scn.objects.active

# copy of the matrix
target.matrix_local = bone_mat
target.rotation_mode = 'QUATERNION'
target.rotation_mode = 'XYZ'
print( 'done, matrix of bone', armature.name, ':', bone.name, 'copied on',  target.name )
