#!/usr/bin/python3

import sys
import bge
import random
import mathutils
import math

class ProcessingBlender:

	def __init__( self, scene, verbose=True ):
		self.verbose = verbose
		self.framecount = 0
		self.context = scene
		if ( self.verbose ):
			print( "processing/blender inititalised" )
			print( "ready to rock!" )
	
	def update( self ):
		self.framecount += 1
		if ( self.verbose ):
			print( "frame:", self.framecount )
	
###############
####### setters
###############

	def enableVerbose( self ):
		self.verbose = True
	
	def disableVerbose( self ):
		self.verbose = False

#######################
####### transformations
#######################

	def rotateX( self, name, value ):
		obj = self.getObjByName( name )
		if obj is not 0:
			mat_rot = obj.worldOrientation
			mat_rot *= mathutils.Matrix.Rotation( value, 3, 'X')
			obj.worldOrientation = mat_rot
			
	def rotateY( self, name, value ):
		obj = self.getObjByName( name )
		if obj is not 0:
			mat_rot = obj.worldOrientation
			mat_rot *= mathutils.Matrix.Rotation( value, 3, 'Y')
			obj.worldOrientation = mat_rot
			
	def rotateZ( self, name, value ):
		obj = self.getObjByName( name )
		if obj is not 0:
			mat_rot = obj.worldOrientation
			mat_rot *= mathutils.Matrix.Rotation( value, 3, 'Z')
			obj.worldOrientation = mat_rot

#############
####### utils
#############

	def getObjByName( self, name ):
		for obj in self.context.objects:
			if ( obj.name == name ):
				return obj
		if ( self.verbose ):
			print( "object named '", name, "' doesn't exist." )
		return 0
		
