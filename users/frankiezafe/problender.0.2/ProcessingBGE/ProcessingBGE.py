#!/usr/bin/python3

# second version of the class

# developped with blessing of numediart.org & thierry dutoit
# contributors:
# juego@requiem4tv.com
# thierry ravet
# the bible: http://www.blender.org/documentation/blender_python_api_2_65_release/contents.html

import sys
import bge
import random
import mathutils
import math

#TODO's
# implement rasterizer!!! http://www.blender.org/documentation/blender_python_api_2_65_5/bge.render.html
# investigate http://blenderartists.org/forum/showthread.php?276746-Trying-to-fix-BGE-bug-27322-bge-render-bugs-Mist-Ambient-and-Mode-sets&highlight= for ambient and mist bug in bge

# resources for singleton class
# http://code.activestate.com/recipes/52558/

# tuto game engine
# http://cgcookies.com/

# import opengl lib
import bgl
import blf

def singleton(cls):
 	return cls()


@singleton
class ProcessingBGE(object):
	
	def __init__(self):
		# general
		self.configured = False
		self.verbose = False
		self.framecount = 0
		self.resources = 0
		self.scene = 0
		# mouse
		self.mouseX = 0
		self.mouseY = 0
		self.mouseLeft = False
		self.mouseMiddle = False
		self.mouseRight = False
		# commodities
		self.PI = math.pi
		self.HALF_PI = math.pi * 0.5
		self.TWO_PI = math.pi * 2.0
	
	def isconfigured( self ):
		return self.configured

####### configure
	
	def configure( self, verbose=True ):
	
		if self.configured:
			return
	
		self.verbose = verbose
		self.framecount = 0
		
		self.scene = bge.logic.getCurrentScene()
		self.root =  bge.logic.getCurrentController().owner
		self.template_cube = 0
		self.template_cylinder = 0
		self.template_empty = 0
		self.template_plane = 0
		self.template_sphere = 0
		self.template_spot = 0
		self.templates = {}
		self.locateTemplates()

		self.configured = True
		self.lcolor = self.rgb2vector( 255,0,0 )

		# setting default values in bge.render
		self.background( 255,255,255 )
		
		# not working in texture mode, wait a bug fix
		bge.render.disableMist()
		
		# loading default font
		font_path = bge.logic.expandPath('//ProcessingBGE/resources/TitilliumWeb-Regular.ttf')
		self.font_id = blf.load(font_path)

		if ( self.verbose ):
			print( "processing/blender inititalised" )
			print( "ready to rock!" )

	def locateTemplates( self ):

		for a in self.root.actuators:
			
			if type(a) is bge.types.KX_SCA_AddObjectActuator:
				
				if a.object is None:
					if self.verbose:
						print( "acturator '", a, "' has no object defined" )
					continue
				oname = a.object.name
				if oname == 'template_cube':
					self.template_cube = a.object
				elif oname == 'template_cylinder':
					self.template_cylinder = a.object
				elif oname == 'template_empty':
					self.template_empty = a.object
				elif oname == 'template_plane':
					self.template_plane = a.object
				elif oname == 'template_sphere':
					self.template_sphere = a.object
				elif oname == 'template_spot':
					self.template_spot = a.object
				else:
					self.templates[oname] = a.object					

		if self.verbose:
			print( "Templates object status:" )
			if self.template_cube is 0:
				print( "\tCan not locate 'template_cube' object" )
			else:
				print( "\t'template_cube' loaded" )
			if self.template_cube is 0:
				print( "Can not locate 'template_cylinder' object" )
			else:
				print( "\t'template_cylinder' loaded" )
			if self.template_empty is 0:
				print( "\tCan not locate 'template_empty' object" )
			else:
				print( "\t'template_empty' loaded" )
			if self.template_plane is 0:
				print( "\tCan not locate 'template_plane' object" )
			else:
				print( "\t'template_plane' loaded" )
			if self.template_sphere is 0:
				print( "\tCan not locate 'template_sphere' object" )
			else:
				print( "\t'template_sphere' loaded" )
			if self.template_spot is 0:
				print( "\tCan not locate 'template_spot' object" )
			else:
				print( "\t'template_spot' loaded" )
			print( "Users templates:" )
			for t in self.templates.keys():
				print( "\t'", self.templates[t] ,"' loaded" )
		

####### update

	def update( self ):
		if self.configured == False:
			print( "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nThere is a huge problem in the init script!\nCall 'configure()' to start correctly ProcessingBlender\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n" )
			return False
		self.framecount += 1


################
####### creators
################


	def createPlane( self, x=0, y=0, z=0, time2live=0 ):
		if self.template_plane is 0:
			if self.verbose:
				print( "No plane template available." )
			return 0
		obj = self.scene.addObject( self.template_plane, self.root, time2live )
		self.move( obj, x,y,z )
		if self.verbose:
			print( "New plane successfully created." )
		return obj

	def createCube( self, x=0, y=0, z=0, time2live=0 ):
		if self.template_cube is 0:
			if self.verbose:
				print( "No cube template available." )
			return 0
		obj = self.scene.addObject( self.template_cube, self.root, time2live )
		self.move( obj, x,y,z )
		if self.verbose:
			print( "New cube successfully created." )
		return obj

	# convenient way to create colors, always return a RGBA color (a veector with 4 positions)
	# the method take 0, 1, 2, 3 or 4 arguments
	# if
	#    0: opaque black
	#    1: opaque grey
	#    2: transparent grey
	#    3: opaque color
	#    4: transparent color
	def color( self, v1="NONE", v2="NONE", v3="NONE", v4="NONE" ):
		if v1 == "NONE":
			return self.rgba2vector( 0,0,0,255 )
		else:
			if v2 == "NONE":
				return self.rgba2vector( v1,v1,v1 )
			else:
				if v3 == "NONE":
					return self.rgba2vector( v1,v1,v1,v2 )
				else:
					if v4 == "NONE":
						return self.rgba2vector( v1,v2,v3 )
					else:
						return self.rgba2vector( v1,v2,v3,v4 )

	
	def getColor( self, o ):
		if type( o ) is str:
			obj = self.getObjByName( o )
			if obj is not 0:
				return obj.color * 255
			else:	
				return self.color() * 255
		elif type( o ) is bge.types.KX_GameObject:
			return o.color * 255
		else:
			return self.color() * 255
			
			

###############
####### getters
###############

	def orientation( self, o, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			return self.getOrientation( obj, absolute )

	def position( self, o, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			return self.getPosition( obj, absolute )

#TODO
	def dimension( self, o ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			vecscale = self.getScale( obj )
			


###############
####### setters
###############

	def enableVerbose( self ):
		self.verbose = True

	def disableVerbose( self ):
		self.verbose = False
			

#################
####### delegates
#################

	def vector( self, x = "NONE", y = "NONE", z = "NONE" ):
		if x != "NONE" and y != "NONE" and z != "NONE":
			return mathutils.Vector( ( x,y,z ) )
		else:
			return mathutils.Vector()

############
####### text
############

	def text( self, text ):
		if self.configured is True:
			width = bge.render.getWindowWidth()
			height = bge.render.getWindowHeight()
			bgl.glMatrixMode(bgl.GL_PROJECTION)
			bgl.glLoadIdentity()
			bgl.gluOrtho2D(0, width, 0, height)
			bgl.glMatrixMode(bgl.GL_MODELVIEW)
			bgl.glLoadIdentity()
			font_id = self.font_id
			blf.position( font_id, 20, 20, 0)
			blf.size( font_id, 300, 300)
			blf.draw( font_id, "Hello World")


############
####### text
############

	def lineColor( self, arg1, arg2 = "NONE", arg3 = "NONE" ):

		r = arg1
		g = 0
		b = 0
		if type( arg1 ) is mathutils.Color:
			self.lcolor = self.rgb2vector( arg1.r, arg1.v, arg1.b )
			return
		elif type( arg1 ) is mathutils.Vector:
			self.lcolor = self.rgb2vector( arg1.x, arg1.y, arg1.z )
			return
		elif type( arg2 ) is not "NONE" and arg3 is not "NONE":
			g = arg2
			b = arg3
		self.lcolor = self.rgb2vector( r,g,b )

	def line( self, arg1, arg2 = "NONE", arg3 = "NONE", arg4 = "NONE", arg5 = "NONE", arg6 = "NONE" ):

		v1 = "NONE"
		v2 = "NONE"

		if type( arg1 ) is mathutils.Vector:
			v1 = arg1
		elif type( arg1 ) is str:
			o = self.getObjByName( arg1 )
			if o is not 0:
				v1 = self.getPosition( o )
		elif type( arg1 ) is bge.types.KX_GameObject:
			v1 = self.getPosition( arg1 )
		
		if v1 == "NONE":
			if ( type( arg1 ) is float or type( arg1 ) is int ) and ( type( arg2 ) is float or type( arg2 ) is int ) and ( type( arg3 ) is float or type( arg3 ) is int ):
				v1 = mathutils.Vector( ( arg1,arg2,arg3 ) )
			else:
				return

		if type( arg2 ) is mathutils.Vector:
			v2 = arg2
		elif type( arg2 ) is str:
			o = self.getObjByName( arg2 )
			if o is not 0:
				v2 = self.getPosition( o )
		elif type( arg2 ) is bge.types.KX_GameObject:
			v2 = self.getPosition( arg2 )

		if v1 != "NONE" and v2 == "NONE":
			if ( type( arg2 ) is float or type( arg2 ) is int ) and ( type( arg3 ) is float or type( arg4 ) is int ) and ( type( arg4 ) is float or type( arg4 ) is int ):
				v2 = mathutils.Vector( ( arg2,arg3,arg4 ) )
			else:
				v2 = mathutils.Vector( ( 0,0,0 ) )
		
		bge.render.drawLine( v1, v2, self.lcolor )

##############
####### colors
##############

####### world

	def background( self, red=0, green=0, blue=0, alpha=255 ):
		newcolor = self.rgba2vector( red, green, blue, alpha )
		bge.render.setBackgroundColor( newcolor )

	def ambient( self, red=0, green=0, blue=0 ):
		newcolor = self.rgb2vector( red, green, blue )
		bge.render.setAmbientColor( newcolor )
		
	def mist( self, red=0, green=0, blue=0 ):
		newcolor = self.rvectorgb2( red, green, blue )
		bge.render.setMistColor( newcolor )
		
####### objects

	def changeColor( self, o, red=255, green=255, blue=255, alpha=255 ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			newcolor = self.rgba2vector( red, green, blue, alpha )
			obj.color = newcolor


#######################
####### transformations
#######################

####### scaling

	def scale( self, o, value, optY="NONE", optZ="NONE" ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if optY == "NONE":
			optY = value
		if optZ == "NONE":
			optZ = value
		if obj is not 0:
			vecscale = self.getScale( obj )
			vecscale.x = value
			vecscale.y = optY
			vecscale.z = optZ
	
	def scaleX( self, o, value ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			vecscale = self.getScale( obj )
			vecscale.x = value
		
	def scaleY( self, o, value ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			vecscale = self.getScale( obj )
			vecscale.y += value
		
	def scaleZ( self, o, value ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			vecscale = self.getScale( obj )
			vecscale.z += value

####### translations

	def moveTo( self, o, arg1, y="NONE", z="NONE" ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0 and ( y == "NONE" or z == "NONE" ):
			obj2 = self.getObjByName( arg1 )
			if obj2 is not 0:
				vt = self.getPosition( obj )			
				vs = self.getPosition( obj2 )
				vt.x = vs.x
				vt.y = vs.y
				vt.z = vs.z
			return
		elif obj is not 0:
			vecposition = self.getPosition( obj )
			vecposition.x = arg1
			vecposition.y = y
			vecposition.z = z

	def move( self, o, x=0, y=0, z=0, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			translation = mathutils.Vector( (x,y,z) )
			if not absolute:
				translation.rotate( self.getOrientation( obj, absolute ) )
			vecposition += translation

	def moveX( self, o, value, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			vecposition.x += value

	def moveY( self, o, value, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			vecposition.y += value
		
	def moveZ( self, o, value, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			vecposition.z += value

####### rotations

	def orient( self, o, neworientation  ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			self.applyOrientation( obj, neworientation )
			

	def pointTo( self, o, tracked ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		ot = 0
		if type(tracked) is str:
			ot = self.getObjByName( tracked )
		else:
			ot = o
		if obj is not 0 and ot is not 0:
			vec1 = self.getPosition( obj, True )
			vec2 = self.getPosition( ot, True )
			vec = mathutils.Vector( ( vec2.x - vec1.x, vec2.y - vec1.y, vec2.z - vec1.z ) )			
			vec.normalize()
			# getting angles, via thierry ravet, my math master
			theta = math.atan( math.sqrt( (vec.x * vec.x) + (vec.y * vec.y) ) / vec.z )
			phi = math.atan( (vec.y * vec.y) / vec.x )
			costheta = math.cos( theta )
			sintheta = math.sin( theta )
			cosphi = math.cos( phi )
			sinphi = math.sin( phi )
			mat = mathutils.Matrix()
			# x line			
			mat[0][0] = costheta * cosphi
			mat[0][1] = -sinphi
			mat[0][2] = sintheta * cosphi
			# y line			
			mat[1][0] = costheta * sinphi
			mat[1][1] = cosphi
			mat[1][2] = sintheta * sinphi
			# z line			
			mat[2][0] = -sintheta
			mat[2][1] = 0
			mat[2][2] = costheta
			vec.x = 0
			vec.y = 0
			vec.z = 1
			vec.rotate( mat )
			self.applyOrientation( obj, vec )
	
	def point( self, o, x=0, y=0, z=0 ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			vecposition = self.getPosition( obj )
			vectarget = mathutils.Vector( ( x,y,z ) )
			vec = mathutils.Vector( ( x - vecposition.x, y - vecposition.y, z - vecposition.z ) )
			vec.normalize()
			# getting angles, via thierry ravet, my math master
			theta = math.atan( math.sqrt( (vec.x * vec.x) + (vec.y * vec.y) ) / vec.z )
			phi = math.atan( (vec.y * vec.y) / vec.x )
			costheta = math.cos( theta )
			sintheta = math.sin( theta )
			cosphi = math.cos( phi )
			sinphi = math.sin( phi )
			mat = mathutils.Matrix()
			# x line			
			mat[0][0] = costheta * cosphi
			mat[0][1] = -sinphi
			mat[0][2] = sintheta * cosphi
			# y line			
			mat[1][0] = costheta * sinphi
			mat[1][1] = cosphi
			mat[1][2] = sintheta * sinphi
			# z line			
			mat[2][0] = -sintheta
			mat[2][1] = 0
			mat[2][2] = costheta
			vec.x = 0
			vec.y = 0
			vec.z = 1
			vec.rotate( mat )
			self.applyOrientation( obj, vec )
#TODO read doc of drawline, not clear how it is working...
			# bge.render.drawLine( mathutils.Vector((0,0,0)), mathutils.Vector((5,5,5)), mathutils.Color((0.0, 0.0, 1.0)) )
			

	def rotateX( self, o, value, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			matorientation = self.getOrientation( obj, absolute )
			matorientation *= mathutils.Matrix.Rotation( value, 3, 'X')
			self.applyOrientation( obj, matorientation, absolute )
		
	def rotateY( self, o, value, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			matorientation = self.getOrientation( obj, absolute )
			matorientation *= mathutils.Matrix.Rotation( value, 3, 'Y')
			self.applyOrientation( obj, matorientation, absolute )
		
	def rotateZ( self, o, value, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjByName( o )
		else:
			obj = o
		if obj is not 0:
			matorientation = self.getOrientation( obj, absolute )
			matorientation *= mathutils.Matrix.Rotation( value, 3, 'Z')
			self.applyOrientation( obj, matorientation, absolute )


#############
####### utils
#############

	def rgba2vector( self, r=255, g=255, b=255, a=255 ):
		r = self.prepareColor( r )
		g = self.prepareColor( g )
		b = self.prepareColor( b )
		a = self.prepareColor( a )
		return mathutils.Vector( ( r,g,b,a ) )
	
	def rgb2vector( self, r=255, g=255, b=255 ):
		r = self.prepareColor( r )
		g = self.prepareColor( g )
		b = self.prepareColor( b )
		return mathutils.Vector( ( r,g,b ) )
			
	def prepareColor( self, c ):
		if c < 0:
			return 0
		if c > 255:
			return 1
		return ( c / 255. )

	def getScale( self, obj ):
		return obj.localScale

	def applyOrientation( self, obj, matorientation, absolute=True ):
		if absolute:
			obj.worldOrientation = matorientation
		else:
			obj.localOrientation = matorientation

	def getPosition( self, obj, absolute=True ):
		if absolute:
			return obj.worldPosition
		else:
			return obj.localPosition

	def getOrientation( self, obj, absolute=True ):
		if absolute:
			return obj.worldOrientation
		else:
			return obj.localOrientation

	def getResourceByName( self, name ):
		return self.resources.objects[name]

	def getObjByName( self, name ):
		obj = 0
		try:
			obj = self.scene.objects[ name ]
		except KeyError:
			obj = 0
		return obj
		
