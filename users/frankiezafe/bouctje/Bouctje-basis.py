import math
from mathutils import Vector, Euler, Quaternion

# def form http://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines-in-python#20679579

def line( p1, p2 ):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection( a, b, c, d ):
    L1 = line( a, b )
    L2 = line( c, d )
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False

def render_face_verts(
    height = 1.0,
    depth = 1.0,
    theta = 0.0,
    bottom_retrait = 0.5
    ):
        
    q = Quaternion( (1.0, 0.0, 0.0), math.radians(theta) )
    
    vecs = []
    vecs.append( Vector(( 0.0, -1, 1 )) )
    vecs.append( Vector(( 0.0, 1, 1 )) )
    vecs.append( Vector(( 0.0, 1, -1 )) )
    vecs.append( Vector(( 0.0, -1, -1 )) )
    for i in range(0, len( vecs )):
        vecs[ i ].y *= depth * 0.5
        vecs[ i ].z *= height * 0.5
        vecs[ i ].rotate( q )
    flat = False
    
    if theta % 90 == 0:
        print( "FLAT!" )
        flat = True
        
    if flat == False:
        # selection of the lower one
        loweri = 0
        deeperi = 0
        minz = 0
        miny = 0
        for i in range(0, len( vecs )):
            if minz > vecs[ i ].z:
                loweri = i
                minz = vecs[ i ].z
            if miny > vecs[ i ].y:
                deeperi = i
                miny = vecs[ i ].y
        
        print( miny, deeperi, minz, loweri )
        
        topi = int( deeperi + 1 ) % 4
        fronti = int( deeperi + 2 ) % 4
        # bottom vector
        # opposite to deeperi
        bottomdir = ( vecs[ loweri ] - vecs[ fronti ] )
        frontdir = ( vecs[ fronti ] - vecs[ topi ] )
        bottomv = vecs[ fronti ] + bottomdir * bottom_retrait
        vecs.append( bottomv )
        
        groundv = bottomv + frontdir
        # generation of 4 points
        intera = Vector((bottomv.y, bottomv.z, 0 ))
        interb = Vector((groundv.y, groundv.z, 0 ))
        interc = Vector(( -100000000, vecs[ loweri ].z, 0 ))
        interd = Vector(( 100000000, vecs[ loweri ].z, 0 ))
        res = intersection( intera, interb, interc, interd )
        
        groundv.y = res[0]
        groundv.z = res[1]
        vecs.append( groundv )
        
        # copying the bottom one
        bottomcp = Vector( vecs[ loweri ] )
        
        #moving the lower one to deepest y
        vecs[ loweri ].y = vecs[ deeperi ].y
    
        # organising output
        tmp = vecs
        vecs = []
        vecs.append( tmp[ deeperi ] )   # 0 - top back
        vecs.append( tmp[ topi ] )      # 1 - top front 
        vecs.append( tmp[ fronti ] )    # 2 - bottom front
        vecs.append( bottomv )          # 3 - top of foot
        vecs.append( groundv )          # 4 - bottom of foot
        vecs.append( tmp[ loweri ] )    # 5 - bottom back
        vecs.append( bottomcp )         # 6 - not used for faces

    return vecs

def plank( 
    face_vs, 
    thickness, 
    offset = Vector(( 0,0,0 ))
    ):
    
    verts = []
    faces = []
    
    if len( face_vs ) == 4:
        
        for j in range( 0,2 ):
            for v in face_vs:
                vv = Vector( v )
                if j == 0:
                    vv.x = vv.x - thickness * 0.5
                else:
                    vv.x = vv.x + thickness * 0.5
                vv += offset
                verts.append( ( vv.x, vv.y, vv.z ) )
        faces = [ 
            (0,1,2,3), 
            (7,6,5,4), 
            (0,3,7,4),
            (0,1,5,4),
            (1,2,6,5),
            (2,3,7,6)
        ]
        
    elif len( face_vs ) == 7:
        
        for j in range( 0,2 ):
            for i in range( 0, 6 ):
                vv = Vector( face_vs[ i ] )
                if j == 0:
                    vv.x = vv.x - thickness * 0.5
                else:
                    vv.x = vv.x + thickness * 0.5
                vv += offset
                verts.append( ( vv.x, vv.y, vv.z ) )
        faces = [ 
            (0,1,2,3), (3,4,5,0), 
            (9,8,7,6), (6,11,10,9),
            (0,1,7,6),
            (1,2,8,7),
            (2,3,9,8),
            (3,4,10,9),
            (4,5,11,10),
            (5,0,6,11)
            ]
    
    return verts, faces

def bottom_plate( 
    face_vs, 
    thickness,
    length,
    offset = Vector(( 0,0,0 ))
    ):
    
    verts = []
    faces = []
    
    # bottom plate
    if len( face_vs ) == 4:
        
        v = Vector( face_vs[3] )
        verts.append( v + offset )
        v = Vector( face_vs[3] )
        v.x += length
        verts.append( v + offset )
        v = Vector( face_vs[2] )
        v.x += length
        verts.append( v + offset )
        v = Vector( face_vs[2] )
        verts.append( v + offset )
        for i in range( 0,4 ):
            v = Vector( verts[i] )
            v.z += thickness
            verts.append( v )
    
    elif len( face_vs ) == 7:
        
        v = Vector( face_vs[6] )
        verts.append( v + offset )
        v = Vector( face_vs[6] )
        v.x += length
        verts.append( v + offset )
        v = Vector( face_vs[2] )
        v.x += length
        verts.append( v + offset )
        v = Vector( face_vs[2] )
        verts.append( v + offset )
        # direction from bottom front to top front
        topdir = face_vs[1] - face_vs[2]
        topdir.normalize()
        topdir *= thickness
        for i in range( 0,4 ):
            v = Vector( verts[i] )
            v += topdir
            verts.append( v )
    
    faces = [ 
        (3,2,1,0), 
        (4,5,6,7), 
        (0,3,7,4),
        (0,1,5,4),
        (1,2,6,5),
        (2,3,7,6)
    ]
    
    return verts, faces

def top_plate( 
    face_vs, 
    thickness,
    length,
    offset = Vector(( 0,0,0 ))
    ):
    
    verts = []
    faces = []
    
    # bottom plate
    if len( face_vs ) == 4:
        
        v = Vector( face_vs[0] )
        verts.append( v + offset )
        v = Vector( face_vs[0] )
        v.x += length
        verts.append( v + offset )
        v = Vector( face_vs[1] )
        v.x += length
        verts.append( v + offset )
        v = Vector( face_vs[1] )
        verts.append( v + offset )
        for i in range( 0,4 ):
            v = Vector( verts[i] )
            v.z -= thickness
            verts.append( v )
    
    elif len( face_vs ) == 7:
        
        v = Vector( face_vs[0] )
        verts.append( v + offset )
        v = Vector( face_vs[0] )
        v.x += length
        verts.append( v + offset )
        v = Vector( face_vs[1] )
        v.x += length
        verts.append( v + offset )
        v = Vector( face_vs[1] )
        verts.append( v + offset )
        # direction from top front to bottom front
        topdir = face_vs[2] - face_vs[1]
        topdir.normalize()
        topdir *= thickness
        for i in range( 0,4 ):
            v = Vector( verts[i] )
            v += topdir
            verts.append( v )
    faces = [ 
        (0,1,2,3), 
        (7,6,5,4), 
        (0,3,7,4),
        (0,1,5,4),
        (1,2,6,5),
        (2,3,7,6)
    ]
    
    return verts, faces

def back_plate( 
    face_vs, 
    thickness,
    height,
    length,
    offset = Vector(( 0,0,0 ))
    ):
    
    verts = []
    faces = []
    
    # bottom plate
    if len( face_vs ) == 4:
        
        v = Vector( face_vs[3] )
        verts.append( v + offset )
        v = Vector( face_vs[3] )
        v.x += length
        verts.append( v + offset )
        v = Vector( face_vs[3] )
        v.x += length
        v.z += height
        verts.append( v + offset )
        v = Vector( face_vs[3] )
        v.z += height
        verts.append( v + offset )
        for i in range( 0,4 ):
            v = Vector( verts[i] )
            v.y += thickness
            verts.append( v )
        faces = [ 
            (0,1,2,3), 
            (7,6,5,4), 
            (0,3,7,4),
            (0,1,5,4),
            (1,2,6,5),
            (2,3,7,6)
        ]
    
    elif len( face_vs ) == 7:
        
        # direction from bottom front to top front
        topdir = face_vs[1] - face_vs[2]
        topdir.normalize()
        
        tmpv = Vector( topdir )
        offset += tmpv * thickness
        totop = Vector( topdir )
        totop *= height
        
        v = Vector( face_vs[6] )
        verts.append( v + offset )
        v = Vector( face_vs[6] )
        v.x += length
        verts.append( v + offset )
        v = Vector( face_vs[6] )
        v.x += length
        v += totop
        verts.append( v + offset )
        v = Vector( face_vs[6] )
        v += totop
        verts.append( v + offset )
        
        frontdir = face_vs[2] - face_vs[6]
        frontdir.normalize()
        frontdir *= thickness
        for i in range( 0,4 ):
            v = Vector( verts[i] )
            v += frontdir
            verts.append( v )
        faces = [ 
            (0,1,2,3), 
            (7,6,5,4), 
            (0,3,7,4),
            (0,1,5,4),
            (1,2,6,5),
            (2,3,7,6)
        ]
    
    return verts, faces

def flat_plank( face_vs ):
    
    verts = []
    if len( face_vs ) == 4:
        for v in face_vs:
            nv = Vector( (v.y,v.z,0) )
            verts.append( nv )
            
    elif len( face_vs ) == 7:
        for i in range( 0,6 ):
            v = face_vs[i]
            nv = Vector( (v.y,v.z,0) )
            verts.append( nv )
            
    verts.append( Vector((face_vs[0].y, face_vs[0].z, 0)) )
    return verts

def adddata(
    pl_verts, pl_faces,
    out_vs, out_fs
    ):
    foffset = len( out_vs )
    for v in pl_verts:
        out_vs.append( v )
    for f in pl_faces:
        lf = []
        for i in f:
            lf.append( i + foffset )
        out_fs.append( lf )

def adddata_tuple(
    pl_verts, 
    out_vs
    ):
    for v in pl_verts:
        out_vs.append( (v.x, v.y, v.z) )

def sv_main(
    width = 0.0,
    height = 1.0,
    depth = 1.0,
    thickness = 0.1,
    theta = 0.0,
    bottom_retrait = 0.5,
    back_retrait = 0.8
    ):
    # press Ctrl+I, look in console
    
    # checking values
    width = abs(width)
    height = abs(height)
    depth = abs(depth)
    theta = abs(theta)
    thickness = abs(thickness)
    bottom_retrait = abs(bottom_retrait)
    back_retrait = abs(back_retrait)
    
    real_height = height
    real_depth = depth
    
    face_vs = render_face_verts( height, depth, theta, bottom_retrait )
    
    info = ""    
    if len( face_vs ) == 4:
        info = "profile :: width(x): " + str( depth ) + ", height(y): " + str( height )
    elif len( face_vs ) == 7:
        fronty = face_vs[2].y
        if fronty < face_vs[4].y:
            fronty = face_vs[4].y
        real_depth = fronty - face_vs[0].y
        real_height = face_vs[1].z - face_vs[5].z
        info = "profile :: width(x): " + str( real_depth ) + ", height(y): " + str( real_height )
    
    #serialisation for viewer
    out_vs = []
    out_fs = []
    profile2d_vs = []
    top2d_vs = []
    bottom2d_vs = []
    back2d_vs = []
    
    # rendering flat face
    f_verts = flat_plank( face_vs )
    adddata_tuple( f_verts, profile2d_vs )
    
    if ( width > thickness * 2 ):
        
        offs = Vector(( -( width - thickness ) * 0.5, 0, 0 ))
        pl_verts, pl_faces = plank( face_vs, thickness, offs )
        adddata( pl_verts, pl_faces, out_vs, out_fs )
        
        poffs = Vector( offs )
        poffs.x += thickness * 0.5
        length = ( offs.x + thickness * 0.5 ) * 2
        pl_verts, pl_faces = bottom_plate( face_vs, thickness, -length, poffs )
        adddata( pl_verts, pl_faces, out_vs, out_fs )

        pl_verts, pl_faces = top_plate( face_vs, thickness, -length, poffs )
        adddata( pl_verts, pl_faces, out_vs, out_fs )

        # poffs.z += thickness
        pheight = ( height * back_retrait ) - ( thickness * 2 )
        pl_verts, pl_faces = back_plate( face_vs, thickness, pheight, -length, poffs )
        adddata( pl_verts, pl_faces, out_vs, out_fs )
        
        offs.x = -offs.x
        pl_verts, pl_faces = plank( face_vs, thickness, offs )
        adddata( pl_verts, pl_faces, out_vs, out_fs )
        
        # 2d plates
        off2d = Vector((0,0,0))
        off2d.x = face_vs[2].y
        if len( face_vs ) == 7 and off2d.x < face_vs[4].y:
            off2d.x = face_vs[4].y
        off2d.x += 1
        
        plate_height = width - thickness * 2
        
        # top plate
        v = Vector(( 0, plate_height * 0.5, 0 )) + off2d
        top2d_vs.append( ( v.x, v.y, v.z ) )
        v = Vector(( depth, plate_height * 0.5, 0 )) + off2d
        top2d_vs.append( ( v.x, v.y, v.z ) )
        v = Vector(( depth, -plate_height * 0.5, 0 )) + off2d
        top2d_vs.append( ( v.x, v.y, v.z ) )
        v = Vector(( 0, -plate_height * 0.5, 0 )) + off2d
        top2d_vs.append( ( v.x, v.y, v.z ) )
        top2d_vs.append( ( top2d_vs[0][0], top2d_vs[0][1], top2d_vs[0][2] ) )
        
        off2d.x += depth + 1
        
        # bottom plate ( similar to top plate )
        v = Vector(( 0, plate_height * 0.5, 0 )) + off2d
        bottom2d_vs.append( ( v.x, v.y, v.z ) )
        v = Vector(( depth, plate_height * 0.5, 0 )) + off2d
        bottom2d_vs.append( ( v.x, v.y, v.z ) )
        v = Vector(( depth, -plate_height * 0.5, 0 )) + off2d
        bottom2d_vs.append( ( v.x, v.y, v.z ) )
        v = Vector(( 0, -plate_height * 0.5, 0 )) + off2d
        bottom2d_vs.append( ( v.x, v.y, v.z ) )
        bottom2d_vs.append( ( bottom2d_vs[0][0], bottom2d_vs[0][1], bottom2d_vs[0][2] ) )
        
        off2d.x += depth + 1
        
        # back plate
        plate_width = (height - thickness * 2) * back_retrait
        v = Vector(( 0, plate_height * 0.5, 0 )) + off2d
        back2d_vs.append( ( v.x, v.y, v.z ) )
        v = Vector(( plate_width, plate_height * 0.5, 0 )) + off2d
        back2d_vs.append( ( v.x, v.y, v.z ) )
        v = Vector(( plate_width, -plate_height * 0.5, 0 )) + off2d
        back2d_vs.append( ( v.x, v.y, v.z ) )
        v = Vector(( 0, -plate_height * 0.5, 0 )) + off2d
        back2d_vs.append( ( v.x, v.y, v.z ) )
        back2d_vs.append( ( back2d_vs[0][0], back2d_vs[0][1], back2d_vs[0][2] ) )
            
    else:
        
        pl_verts, pl_faces = plank( face_vs, thickness )
        for v in pl_verts:
            out_vs.append( v )
        for f in pl_faces:
            out_fs.append( f )

    in_sockets = [
        ['s','width', width ],
        ['s','height', height ],
        ['s','depth', depth ],
        ['s','thickness', thickness ],
        ['s','theta', theta ],
        ['s','bottom_retrait', bottom_retrait ],
        ['s','back_retrait', back_retrait ]
    ]

    out_sockets = [
        ['v','verts', out_vs ],
        ['s','faces', out_fs ],
        ['v','profile (2d)', profile2d_vs ],
        ['v','top plank (2d)', top2d_vs ],
        ['v','bottom plank (2d)', bottom2d_vs ],
        ['v','back plank (2d)', back2d_vs ],
        ['s','info', info ]
    ]

    return in_sockets, out_sockets
