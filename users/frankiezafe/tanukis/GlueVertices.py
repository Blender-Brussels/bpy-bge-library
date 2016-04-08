# based on https://www.blender.org/api/blender_python_api_current/bpy.types.MeshVertex.html?highlight=meshvertex
# and http://blender.stackexchange.com/questions/7144/how-to-get-the-distance-between-two-objects-in-the-game-engine
import bpy
from bpy import context
from math import sqrt
from mathutils import Vector

# BEFORE launching script, SELECT the vertices to test

# config
TOLERANCE = 0.00001

# globals
MERGED_COUNT = 0
LAST_INDEX = 0
VSELECTED = []
VMERGES = {}
VMERGEPOS = []

def getDistance( v1, v2 ):
    distance = sqrt( (v1.co[0] - v2.co[0])**2 + (v1.co[1] - v2.co[1])**2 + (v1.co[2] - v2.co[2])**2)
    #print(distance)
    return distance

def getDistance2Vector( vertex, vector ):
    distance = sqrt( (vertex.co[0] - vector.x)**2 + (vertex.co[1] - vector.y)**2 + (vertex.co[2] - vector.z)**2)
    #print(distance)
    return distance

obj = context.active_object
print( "scanning", obj.data.vertices, "vertices" )

bpy.ops.object.mode_set(mode="OBJECT")

vall = obj.data.vertices
for v in vall:
    if v.select:
        VSELECTED.append( v )

print( "***********", len( VSELECTED ), "vertices to verify" )

# making merge groups
vselnum = len( VSELECTED )
i = 0
for v in VSELECTED:
    #print( v.co, i )
    for j in range( i + 1, vselnum ):
        if j >= vselnum:
            break
        vo = VSELECTED[ j ]
        d = getDistance( v, vo )
        if d < TOLERANCE:
            # retro seeking: v may have to be merged with a previous one!
            index = i
            for m in VMERGES:
                mlist = VMERGES[ m ]
                mcontinue = True
                for mc in mlist:
                    if mc == v:
                        index = m
                        mcontinue = False
                        #print( "retro-seek is successful", i, m )
                        break
                if not mcontinue:
                    break
            
            if i not in VMERGES:
                VMERGES[ index ] = [ v ]
            VMERGES[ index ].append( vo )
            
    i += 1

# rendering position of merge
for k in VMERGES:
    mlist = VMERGES[ k ]
    pos = Vector( (0,0,0) )
    for mc in mlist:
        pos.x += mc.co[0]
        pos.y += mc.co[1]
        pos.z += mc.co[2]
    pos.x /= len( mlist )
    pos.y /= len( mlist )
    pos.z /= len( mlist )
    #print( len(VMERGEPOS), ">>", len(mlist), ">>", pos )
    VMERGEPOS.append( pos )

print( "VMERGEPOS:",  len( VMERGEPOS ) )

bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="DESELECT")
bpy.context.tool_settings.mesh_select_mode = (True , False , False)
bpy.ops.object.mode_set(mode="OBJECT")

mcount = 0
for p in VMERGEPOS:
    vall = obj.data.vertices
    velected = 0
    for v in vall:
        d = getDistance2Vector( v, p )
        if d < TOLERANCE:
            v.select = True
            velected += 1
    if velected != 0:
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.merge(type='CENTER')
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        print( "merge done at", p.x, p.y, p.z, "vertex:", velected, "count:", mcount, "/", len(VMERGEPOS) )
    MERGED_COUNT += velected
    mcount += 1

print( "total:",  MERGED_COUNT, "vertices have been merged" )
