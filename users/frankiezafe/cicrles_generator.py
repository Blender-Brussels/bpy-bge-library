import bpy, os, random
import math
import mathutils

pointnum = 3
size = 1

me = bpy.data.meshes.new('circle')
ob = bpy.data.objects.new('circle', me)

ob.select = True
	
scn = bpy.context.scene
scn.objects.link(ob)
scn.objects.active = ob
	
verts = []
faces = []

a = 0
gapa = math.pi * 2 / pointnum
vindex = 0
v = 0

if pointnum > 2:
    for i in range( 0, pointnum ):
        v = mathutils.Vector(( math.cos(a) * size, math.sin(a) * size, 0 ))
        verts.append( v )
        a += gapa
    if pointnum == 3:
        faces.append( [ 0,1,2 ] )
    elif pointnum == 4:
        faces.append( [ 0,1,2 ] )
        faces.append( [ 2,3,0 ] )
    if pointnum > 4:
        v = mathutils.Vector(( 0,0,0 ))
        verts.append( v )
        

me.from_pydata( verts, [], faces )
