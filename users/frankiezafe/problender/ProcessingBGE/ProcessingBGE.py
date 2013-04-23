#!/usr/bin/python3

# the bible: http://www.blender.org/documentation/blender_python_api_2_65_release/contents.html

import sys
import bge
import random
import mathutils
import math

# todo:
# move local! -> create vector and multiply it by orientation matrix
# implement rasterizer!!! http://www.blender.org/documentation/blender_python_api_2_65_5/bge.render.html
# investigate http://blenderartists.org/forum/showthread.php?276746-Trying-to-fix-BGE-bug-27322-bge-render-bugs-Mist-Ambient-and-Mode-sets&highlight= for ambient and mist bug in bge

# resources for singleton class
# http://code.activestate.com/recipes/52558/

def singleton(cls):
 	return cls()


@singleton
class ProcessingBGE(object):
	
	def __init__(self):
		self.verbose = False
		self.framecount = 0
		self.resources = 0
		self.context = 0
		self.configured = False
	
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

	def createBox( self ):
		obj = self.getResourceByName( "default_cube" )
		print( obj )
		if obj is not 0:
			print( self.context.addObject( obj, bge.logic.getCurrentController().owner, 0 ) )
			

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
		newcolor = self.rgb2vector( red, green, blue )
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

	def scale( self, name, value ):
		obj = self.getObjByName( name )
		if obj is not 0:
			vecscale = self.getScale( obj )
			vecscale.x = value
			vecscale.y = value
			vecscale.z = value
	
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

	def position( self, name, x=0, y=0, z=0, absolute=True ):
		obj = self.getObjByName( name )
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			vecposition.x = x
			vecposition.y = y
			vecposition.z = z

	def move( self, name, x=0, y=0, z=0, absolute=True ):
		obj = self.getObjByName( name )
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			vecposition.x += x
			vecposition.y += y
			vecposition.z += z

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

	def applyOrientation( self, obj, matorientation, absolute=True ):
		if absolute:
			obj.worldOrientation = matorientation
		else:
			obj.localOrientation = matorientation

	def getResourceByName( self, name ):
		return self.resources.objects[name]

	def getObjByName( self, name ):
		for obj in self.context.objects:
			if ( obj.name == name ):
				return obj
		if ( self.verbose ):
			print( "object named '", name, "' doesn't exist in render." )
		return 0
		
