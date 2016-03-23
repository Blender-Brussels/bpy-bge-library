import bpy, os, random
import math
import mathutils

# script to generate a sphere having nearly squre faces
# by oppositon to the UV sphere where faces becomes more and more triangular towards the poles
# this script maintains 3 edges of each faces at the same size
# by frankiezafe.org

## config
# number of edges on longitudes
pointnum = 80
# diameter of the sphere
size = 1
# describe the hole at the top of the sphere
# if 0.5, the number of might be INIFINITE!
caps = 0.48

## active code
me = bpy.data.meshes.new('squared-sphere')
ob = bpy.data.objects.new('squared-sphere', me)

ob.select = True
	
scn = bpy.context.scene
scn.objects.link(ob)
scn.objects.active = ob

verts = []
edges = []
faces = []

a = 0
gapa = math.pi * 2 / pointnum
vindex = 0
v = 0

arc_size = 0
# size of the arc at first level
# thanks to: http://www.mathopenref.com/chord.html
chord_size = size * math.sin( gapa * 0.5 )
# inverse: cs / size = sin( gapa )
# asin( cs / size ) = gapa
# gapa = asin( cs / size )
print( 'sphererx' )
print( chord_size, gapa, math.asin( chord_size / size ) * 2 )

def addVertice( row, column, x, y, z ):
    global verts
    global edges
    global faces
    global pointnum
    v = mathutils.Vector(( x,y,z ))
    verts.append( v )
    # equator, no faces
    if row == 0:
        return
    # first positive row
    elif row == 1 and column > 0:
        v1 = len(verts) - 1
        v2 = v1-1
        v3 = v2 - pointnum
        v4 = v3 + 1
        faces.append( [ v1, v2, v3, v4 ] )
        if column == pointnum - 1:
            v1 = len(verts) - 1
            v2 = v1 - (pointnum - 1)
            v3 = v4
            v4 = v3 - (pointnum - 1)
            faces.append( [ v2, v1, v3, v4 ] )
    # first negative row
    elif row == -1 and column > 0:
        v1 = len(verts)-1
        v2 = v1-1
        v3 = column - 1
        v4 = v3 + 1
        faces.append( [ v2, v1, v4, v3 ] )
        if column == pointnum - 1:
            v1 = len(verts) - 1
            v2 = v1 - (pointnum - 1)
            v3 = v4
            v4 = v3 - (pointnum - 1)
            faces.append( [ v1, v2, v4, v3 ] )
    # all other positive rows
    elif row > 1 and column > 0:
        v1 = len(verts) - 1
        v2 = v1-1
        v3 = v2 - pointnum * 2
        v4 = v3 + 1
        faces.append( [ v1, v2, v3, v4 ] )
        if column == pointnum - 1:
            v1 = len(verts) - 1
            v2 = v1 - (pointnum - 1)
            v3 = v4
            v4 = v3 - (pointnum - 1)
            faces.append( [ v2, v1, v3, v4 ] )
    # all other negative rows
    elif row < -1 and column > 0:
        v1 = len(verts) - 1
        v2 = v1-1
        v3 = v2 - pointnum * 2
        v4 = v3 + 1
        faces.append( [ v2, v1, v4, v3 ] )
        if column == pointnum - 1:
            v1 = len(verts) - 1
            v2 = v1 - (pointnum - 1)
            v3 = v4
            v4 = v3 - (pointnum - 1)
            faces.append( [ v1, v2, v4, v3 ] )
    return

zenitha = 0
z = 0
while zenitha < math.pi * caps:
    zpos = math.sin( zenitha ) * size * 0.5
    radius = math.cos( zenitha ) * size
    zenithgap = math.asin( chord_size / size ) * 2
    zenitha += zenithgap
    chord_size = math.cos( zenitha ) * size * math.sin( gapa * 0.5 )
    a = 0
    if chord_size < 0:
        chord_size *= -1
    print( 'level', z, 'zenith', zenitha, 'arc size', chord_size )
    for x in range( 0, pointnum ):
        addVertice( z, x, math.cos(a) * radius * 0.5, math.sin(a) * radius * 0.5, zpos )
        a += gapa
    if z  != 0:
        for x in range( 0, pointnum ):
            addVertice( -z, x, math.cos(a) * radius * 0.5, math.sin(a) * radius * 0.5, -zpos )
            a += gapa
    z += 1

me.from_pydata( verts, edges, faces )