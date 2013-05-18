import bpy, os, random
import math
import mathutils

# script to generate 2D polygon at the center of the world, in the X Y plane
# with hole ( hole != 0 ) or without ( hole = 0 )
# notice: 
#   - hole is relative to the size: 0.5 means 50% of the size
#   - if hole is 1, nothing is added...
#   - if hole is bigger than 1, the size of the hole is the size value!
# trianglefaces is used only if:
#   - there is no hole and there is four points
#   - there is a hole
# startatzero should be set to false when you set a even number of faces
# -> the shape will be parallell to x & y axis
# by frankiezafe.org

## config
pointnum = 6
size = 1
hole = 0.2
startatzero = False
trianglefaces = False

## active code
me = bpy.data.meshes.new('polygon')
ob = bpy.data.objects.new('polygon', me)

ob.select = True
	
scn = bpy.context.scene
scn.objects.link(ob)
scn.objects.active = ob

verts = []
faces = []

a = 0
gapa = math.pi * 2 / pointnum
if startatzero is not True:
    a = gapa * 0.5
vindex = 0
v = 0

if pointnum > 2 and hole is not 1:
    for i in range( 0, pointnum ):
        v = mathutils.Vector(( math.cos(a) * size * 0.5, math.sin(a) * size * 0.5, 0 ))
        verts.append( v )
        a += gapa
    if hole == 0:
        if pointnum == 3:
            faces.append( [ 0,1,2 ] )
        elif pointnum == 4:
            if trianglefaces is True:
                faces.append( [ 0,1,2 ] )
                faces.append( [ 2,3,0 ] )
            else:
                faces.append( [ 0,1,2,3 ] )
        if pointnum > 4:
            v = mathutils.Vector(( 0,0,0 ))
            verts.append( v )
            for p in range( 0, pointnum ):
                pp = p+1
                if p == pointnum-1:
                    pp = 0
                faces.append( [ p,pp, pointnum ] )
    else:
       if startatzero is not True:
           a = gapa * 0.5
       hs = hole * size
       for i in range( 0, pointnum ):
            v = mathutils.Vector(( math.cos(a) * hs * 0.5, math.sin(a) * hs * 0.5, 0 ))
            verts.append( v )
            a += gapa
       for p in range( 0, pointnum ):
           pp = p+1
           if p == pointnum-1:
               pp = 0
           p1 = p + pointnum
           pp1 = pp + pointnum
           if trianglefaces is True:
               faces.append( [ p,pp,pp1 ] )
               faces.append( [ pp1,p1,p ] )
           else:
               faces.append( [ p,pp,pp1,p1 ] )


me.from_pydata( verts, [], faces )
