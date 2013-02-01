# Muqarnas version 000.1 
# Find a name, discover size, duplicate, and place in circle
# not perfect yet 1/2/2013, inshaala  


import bpy
import math
from mathutils import Vector

obs = bpy.data.objects
scn = bpy.context.scene
n = 10

#bpy.ops.object.mode_set(mode='OBJECT')

anglestart = 0
angleend = math.pi * 2
anglestep = (  angleend - anglestart ) / n

angle = anglestart
radius = 1


def duplicateObject(scene, name, copyobj):
 
    # Create new mesh
    mesh = bpy.data.meshes.new(name)
 
    # Create new object associated with the mesh
    ob_new = bpy.data.objects.new(name, mesh)
 
    # Copy data block from the old object into the new object
    ob_new.data = copyobj.data.copy()
    ob_new.scale = copyobj.scale
    ob_new.location = copyobj.location
    ob_new.rotation_euler = copyobj.rotation_euler
 
    # Link new object to the given scene and select it
    scene.objects.link(ob_new)
    ob_new.select = True
 
    return ob_new

def getRealSize( o ):
    min = Vector ((0, 0, 0))
    max = Vector ((0, 0, 0))
    size = Vector ((0, 0, 0))
    first = True
    for v in o.data.vertices:
        if first:
            min[0] = v.co[0]
            min[1] = v.co[1]
            min[2] = v.co[2]
            max[0] = v.co[0]
            max[1] = v.co[1]
            max[2] = v.co[2]
            first = False
        else:
            if min[0] > v.co[0]:
                min[0] = v.co[0]
            if min[1] > v.co[1]:
                min[1] = v.co[1]
            if min[2] > v.co[2]:
                min[2] = v.co[2]
            if max[0] < v.co[0]:
                max[0] = v.co[0]
            if max[1] < v.co[1]:
                max[1] = v.co[1]
            if max[2] < v.co[2]:
                max[2] = v.co[2]
    size[0] = max[0] - min[0]
    size[1] = max[1] - min[1]
    size[2] = max[2] - min[2]
    return size

bpy.ops.object.select_all(action='DESELECT')
for ob in obs:
    
    if ( ob.name == "Cube" ):
        s = getRealSize (ob) 
        diag = math.sqrt(math.pow (s[0], 2 )+math.pow (s[1], 2 ))
        #diag *= 0.5
        print (s, ",", diag)
        radius = diag/math.tan(anglestep)
        
        
        
        #ob.select = True
        for i in range(n) :
            # scn.objects.active = ob
            
            tmpo = duplicateObject( scn, "copyofblock", ob )
            tmpo.location = ( ( math.cos( angle ) * radius ), ( math.sin( angle ) * radius ), 0 )
            tmpo.rotation_euler = ( 0, 0 , angle + math.pi*0.75 )
            print( tmpo )
            tmpo.select = False
            # bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(i, i, i)})
            # bpy.ops.object.transform_apply(location=False, rotation= 0.8, scale=False)
            
            angle += anglestep
        
        #ob.select = False
