#!/usr/bin/python3

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
		self.context = 0
		# mouse
		self.mouseX = 0
		self.mouseY = 0
		self.mouseLeft = False
		self.mouseMiddle = False
		self.mouseRight = False
	
	def isconfigured( self ):
		return self.configured

####### configure
	
	def configure( self, scene=0, resourcescene=0, verbose=True ):
	
		if self.configured:
			return
	
		self.verbose = verbose
		self.framecount = 0
		
		if scene is 0:
			scenes = bge.logic.getSceneList()
			for sc in scenes:
				if sc.name == "render":
					self.context = sc
					break
		else:
			self.context = scene
			
		if resourcescene is 0:
			scenes = bge.logic.getSceneList()
			for sc in scenes:
				if sc.name == "resources":
					self.resources = sc
					break
		else:
			self.resources = resourcescene
		
		if self.resources is 0 or self.context is 0:
			print( "UNABLE TO LOCATE SCENES!" )
			print( "Verify the scenes names (should be 'render' and 'resources')" )
			print( "Or pass the scene object in args to this method!" )
			print( "scenes:", bge.logic.getSceneList() )
			return
		
		self.configured = True
		self.defaultLineColor = self.rgb2vector( 255,0,0 )

		# setting default values in bge.render
		self.background( 255,255,255 )
		
		# not working in texture mode, wait a bug fix
		bge.render.disableMist()
		
		if ( self.verbose ):
			print( "processing/blender inititalised" )
			print( "ready to rock!" )

####### update

	def update( self ):
		if self.configured == False:
			print( "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nThere is a huge problem in the init script!\nCall 'configure()' to start correctly ProcessingBlender\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n" )
			return False
		self.framecount += 1


################
####### creators
################

#TODO
	def duplicate( self, name, newname ):
		newobj = self.context.addObject( self.context.objects[name], bge.logic.getCurrentController().owner, 0 )
		newobj.name = newname
		return newobj

#TODO
	def createBox( self ):
		obj = self.getResourceByName( "default_cube" )
		print( obj )
		if obj is not 0:
			print( self.context.addObject( obj, bge.logic.getCurrentController().owner, 0 ) )

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
			

###############
####### getters
###############

	def orientation( self, name, absolute=True ):
		obj = self.getObjByName( name )
		if obj is not 0:
			return self.getOrientation( obj, absolute )

	def position( self, name, absolute=True ):
		obj = self.getObjByName( name )
		if obj is not 0:
			return self.getPosition( obj, absolute )

#TODO
	def dimension( self, name ):
		obj = self.getObjByName( name )
		if obj is not 0:
			vecscale = self.getScale( obj )
			


###############
####### setters
###############

	def enableVerbose( self ):
		self.verbose = True

	def disableVerbose( self ):
		self.verbose = False


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

	def changeColor( self, name, red=255, green=255, blue=255, alpha=255 ):
		obj = self.getObjByName( name )
		if obj is not 0:
			newcolor = self.rgba2vector( red, green, blue, alpha )
			obj.color = newcolor


#######################
####### transformations
#######################

####### scaling

	def scale( self, name, value, optY="NONE", optZ="NONE" ):
		obj = self.getObjByName( name )
		if optY == "NONE":
			optY = value
		if optZ == "NONE":
			optZ = value
		if obj is not 0:
			vecscale = self.getScale( obj )
			vecscale.x = value
			vecscale.y = optY
			vecscale.z = optZ
	
	def scaleX( self, name, value ):
		obj = self.getObjByName( name )
		if obj is not 0:
			vecscale = self.getScale( obj )
			vecscale.x = value
		
	def scaleY( self, name, value ):
		obj = self.getObjByName( name )
		if obj is not 0:
			vecscale = self.getScale( obj )
			vecscale.y += value
		
	def scaleZ( self, name, value ):
		obj = self.getObjByName( name )
		if obj is not 0:
			vecscale = self.getScale( obj )
			vecscale.z += value

####### translations

	def moveTo( self, name, arg1, y="NONE", z="NONE" ):
		obj = self.getObjByName( name )
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

	def move( self, name, x=0, y=0, z=0, absolute=True ):
		obj = self.getObjByName( name )
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			translation = mathutils.Vector( (x,y,z) )
			if not absolute:
				translation.rotate( self.getOrientation( obj, absolute ) )
			vecposition += translation

	def moveX( self, name, value, absolute=True ):
		obj = self.getObjByName( name )
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			vecposition.x += value

	def moveY( self, name, value, absolute=True ):
		obj = self.getObjByName( name )
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			vecposition.y += value
		
	def moveZ( self, name, value, absolute=True ):
		obj = self.getObjByName( name )
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			vecposition.z += value

####### rotations

	def orient( self, name, neworientation  ):
		obj = self.getObjByName( name )
		if obj is not 0:
			self.applyOrientation( obj, neworientation )
			

	def pointTo( self, name, tracked ):
		obj = self.getObjByName( name )
		ot = self.getObjByName( tracked )
		if obj is not 0 and ot is not 0:
			vec1 = self.getPosition( obj )
			vec2 = self.getPosition( ot )
			translation = mathutils.Vector( ( vec2.x - vec1.x, vec2.y - vec1.y, vec2.z - vec1.z ) )
#TODO
			# bge.render.drawLine( vec1, vec2, self.defaultLineColor )
	
	def point( self, name, x=0, y=0, z=0 ):
		obj = self.getObjByName( name )
		if obj is not 0:
			vecposition = self.getPosition( obj )
			translation = mathutils.Vector( ( x - vecposition.x, y - vecposition.y, z - vecposition.z ) )
#TODO
			# matorientation = mathutils.Matrix
			# transform matrix to make it point to the 3D position
			# self.applyOrientation( obj, matorientation )

	def rotateX( self, name, value, absolute=True ):
		obj = self.getObjByName( name )
		if obj is not 0:
			matorientation = self.getOrientation( obj, absolute )
			matorientation *= mathutils.Matrix.Rotation( value, 3, 'X')
			self.applyOrientation( obj, matorientation, absolute )
		
	def rotateY( self, name, value, absolute=True ):
		obj = self.getObjByName( name )
		if obj is not 0:
			matorientation = self.getOrientation( obj, absolute )
			matorientation *= mathutils.Matrix.Rotation( value, 3, 'Y')
			self.applyOrientation( obj, matorientation, absolute )
		
	def rotateZ( self, name, value, absolute=True ):
		obj = self.getObjByName( name )
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
		for obj in self.context.objects:
			if ( obj.name == name ):
				return obj
		if ( self.verbose ):
			print( "object named '", name, "' doesn't exist in render." )
		return 0
		
