import bge
from random import random as rnd
import mathutils
import math

scene = bge.logic.getCurrentScene()
objprefix = "op"
objprefixlength = len(objprefix)

for obj in scene.objects:
    if( obj.name[:objprefixlength] == objprefix ):
        # rotation using a matrix
        mat_rot = obj.localOrientation
        mat_rot *= mathutils.Matrix.Rotation( 0.02 + ( -0.001 + rnd() * 0.002 ), 3, 'X')
        obj.localOrientation = mat_rot
        # translation
        obj.worldPosition.x += -0.1 + rnd() * 0.2 #-1.5+rnd()*3 
        obj.worldPosition.y += -0.1 + rnd() * 0.2 #-1.5 +rnd()*3
        obj.worldPosition.z += -0.1 + rnd() * 0.2 #-1.5 +rnd()*3
