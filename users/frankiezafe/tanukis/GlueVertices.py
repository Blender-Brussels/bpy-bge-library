# based on https://www.blender.org/api/blender_python_api_current/bpy.types.MeshVertex.html?highlight=meshvertex
# and http://blender.stackexchange.com/questions/7144/how-to-get-the-distance-between-two-objects-in-the-game-engine
import bpy
from bpy import context
from math import sqrt

TOLERANCE = 0.00001
MERGED_COUNT = 0

def getDistance( v1, v2 ):
    """
    return: float. Distance of the two vertices
    """
    distance = sqrt( (v1.co[0] - v2.co[0])**2 + (v1.co[1] - v2.co[1])**2 + (v1.co[2] - v2.co[2])**2)
    #print(distance)  # print distance to console, DEBUG
    return distance

def doMerge( vs ):
    global TOLERANCE
    global MERGED_COUNT
    vnum = len( vs )
    for i in range( 0, vnum ):
        v = vs[ i ]
        for j in range( i + 1, vnum ):
            vo = vs[ j ]
            if v is not vo:
                d = getDistance( v, vo )
                if d  < TOLERANCE:
                    v.select = True
                    vo.select = True
                    print( "merging vertices at", v.co, "and", vo.co )
                    bpy.ops.object.mode_set(mode="EDIT")
                    bpy.ops.mesh.merge(type='CENTER')
                    bpy.ops.mesh.select_all(action="DESELECT")
                    bpy.ops.object.mode_set(mode="OBJECT")
                    MERGED_COUNT += 1
                    return True
    return False

obj = context.active_object
print( "scanning", obj.data.vertices, "vertices" )

vpot = obj.data.vertices

bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="DESELECT")
bpy.context.tool_settings.mesh_select_mode = (True , False , False)
bpy.ops.object.mode_set(mode="OBJECT")

# seek vertices at the same position

while doMerge( vpot ):
    print( MERGED_COUNT )

print( "total:",  MERGED_COUNT, "vertices have been merged" )