#!/usr/bin/python3

# second version of the class

# developped with blessing of numediart.org & thierry dutoit
# contributors:
# juego@requiem4tv.com
# thierry ravet
# the bible: http://www.blender.org/documentation/blender_python_api_2_65_release/contents.html

import sys
import math
import random

# blender libs
import bge
import mathutils
import bgl
import blf

# external libs
import ProcessingBGE.ProcessingOSC as posc

#TODO's
# implement rasterizer!!! http://www.blender.org/documentation/blender_python_api_2_65_5/bge.render.html
# investigate http://blenderartists.org/forum/showthread.php?276746-Trying-to-fix-BGE-bug-27322-bge-render-bugs-Mist-Ambient-and-Mode-sets&highlight= for ambient and mist bug in bge
# investigate http://www.yofrankie.org/tag/bge/ ( https://svn.blender.org/svnroot/yofrankie/trunk/ )
# investigate http://solarlune-gameup.blogspot.be/2011/01/opengl-2d-screen-filters-in-bge-part-1.html (shaders)

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
		self.scene = 0
		# view
		self.width = 0
		self.height = 0
		self.view_orientation = 0
		# mouse
		self.input_mouse = bge.logic.mouse
		self.input_mouse.visible = True
		self.mouseX = 0
		self.mouseY = 0
		self.mouseLeft = False
		self.mouseMiddle = False
		self.mouseRight = False
		# keyboard
		self.input_keyboard = bge.logic.keyboard
		# keyboard events are not triggered fast enough: just_pressed and just_released are missed by this way to process them
		# a comparaison is made on update to fix that	
		self.input_keyboardEvents = {}
		for key in self.input_keyboard.events.keys():
			self.input_keyboardEvents[key] = self.input_keyboard.events[key]
		# OSC
		self.osc_manager = posc.ProcessingOSC.getInstance()
		# commodities
		self.PI = math.pi
		self.HALF_PI = math.pi * 0.5
		self.TWO_PI = math.pi * 2.0
		self.ARROW_UP = 	bge.events.UPARROWKEY
		self.ARROW_RIGHT = 	bge.events.RIGHTARROWKEY
		self.ARROW_DOWN = 	bge.events.DOWNARROWKEY
		self.ARROW_LEFT = 	bge.events.LEFTARROWKEY
	
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
		self.template_2D_circle = 0
		self.template_2D_square = 0
		self.template_2D_triangle = 0
		self.templates = {}
		self.generatedObjects = {}
		self.locateTemplates()

		self.configured = True

		# lines and text colors
		self.lcolor = self.rgb2vector( 255,0,0 )
		self.tcolor = self.rgb2vector( 255,255,255 )
		self.tsize = 50

		# setting default values in bge.render
		self.background( 255,255,255 )
		
		# not working in texture mode, wait a bug fix
		bge.render.disableMist()
		
		# loading default font
		font_path = bge.logic.expandPath('//ProcessingBGE/resources/TitilliumWeb-Regular.ttf')
		self.font = blf.load(font_path)

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
				elif oname == 'template_2D_circle':
					self.template_2D_circle = a.object
				elif oname == 'template_2D_square':
					self.template_2D_square = a.object
				elif oname == 'template_2D_triangle':
					self.template_2D_triangle = a.object
				else:
					self.templates[oname] = a.object					

		if self.verbose:
			print( "Template objects status:" )
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
			if self.template_2D_circle is 0:
				print( "\tCan not locate 'template_2D_circle' object" )
			else:
				print( "\t'template_2D_circle' loaded" )
			if self.template_2D_square is 0:
				print( "\tCan not locate 'template_2D_square' object" )
			else:
				print( "\t'template_2D_square' loaded" )
			if self.template_2D_triangle is 0:
				print( "\tCan not locate 'template_2D_triangle' object" )
			else:
				print( "\t'template_2D_triangle' loaded" )
			print( "Users templates:" )
			if len( self.templates.keys() ) == 0:
				print( "\t", "none" )
			for t in self.templates.keys():
				print( "\t'", self.templates[t] ,"' loaded" )
		

####### update

	def update( self ):
		if self.configured == False:
			print( "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nThere is a huge problem in the init script!\nCall 'configure()' to start correctly ProcessingBlender\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n" )
			return False
		# update width and height size
		self.width = bge.render.getWindowWidth()
		self.height = bge.render.getWindowHeight()
		# update keyboard and mouse
		self.inputs()
		self.framecount += 1
		self.view_orientation = bge.logic.getCurrentScene().active_camera.modelview_matrix


##############
####### inputs
##############
	
	# called by update, no need to make an explicit call
	def inputs( self ):
		
		# comparing keyboard events to local copy
		for key in self.input_keyboard.events.keys():
			if self.input_keyboard.events[key] != self.input_keyboardEvents[key]:
				if self.input_keyboard.events[key] == bge.logic.KX_INPUT_ACTIVE and self.input_keyboardEvents[key] == bge.logic.KX_INPUT_NONE:
					self.input_keyboardEvents[key] = bge.logic.KX_INPUT_JUST_ACTIVATED
				elif self.input_keyboard.events[key] == bge.logic.KX_INPUT_NONE and ( self.input_keyboardEvents[key] == bge.logic.KX_INPUT_JUST_ACTIVATED or self.input_keyboardEvents[key] == bge.logic.KX_INPUT_ACTIVE ):
					self.input_keyboardEvents[key] = bge.logic.KX_INPUT_JUST_RELEASED
				else:
					self.input_keyboardEvents[key] = self.input_keyboard.events[key]

		# relative position of the mouse ( viewport )
		self.mouseX = self.input_mouse.position[0]
		self.mouseY = self.input_mouse.position[1]
#TODO
# buttons requires a SCA_MouseSensor! -> should be done before, @ instanciation or configuration
		return True

	
	# methods to be used by users
	# return true or false depending on the characters given
	# can be used with ascii value of the key or a char
	def keyPressed( self, char ):
		caps = self.capsActive()
		if caps and self.isLowercase( char ):
			return False
		elif caps:
			char = self.char2lowercase( char )
		char_ascii = self.char2ascii( char )
		if char_ascii == -1:
			return False
		if self.input_keyboardEvents[ char_ascii ] == bge.logic.KX_INPUT_JUST_ACTIVATED :
			return True
		return False
		

	def keyReleased( self, char ):
		caps = self.capsActive()
		if caps and self.isLowercase( char ):
			return False
		elif caps:
			char = self.char2lowercase( char )
		char_ascii = self.char2ascii( char )
		if char_ascii == -1:
			return False
		if self.input_keyboardEvents[ char_ascii ] == bge.logic.KX_INPUT_JUST_RELEASED :
			return True
		return False

	def keyActive( self, char ):
		caps = self.capsActive()
		if caps and self.isLowercase( char ):
			return False
		elif caps:
			char = self.char2lowercase( char )
		char_ascii = self.char2ascii( char )
		if char_ascii == -1:
			return False
		if self.input_keyboardEvents[ char_ascii ] == bge.logic.KX_INPUT_ACTIVE :
			return True
		return False

	def capsActive( self ): 
		if self.input_keyboardEvents[124] == bge.logic.KX_INPUT_ACTIVE or self.input_keyboardEvents[124] == bge.logic.KX_INPUT_JUST_ACTIVATED:
			return True
		return False

################
####### creators
################

	def makeUnique( self, name ):
		increment = 0
		tmpname = 0
		unique = False
		while( unique is False and increment < 10000 ):
			if increment < 10:
				tmpname = name+".000"
			elif increment < 100:
				tmpname = name+".00"
			elif increment < 1000:
				tmpname = name+".0"
			tmpname += str( increment )
			if self.getGeneratedByName( tmpname ) is 0 and self.getObjectByName( tmpname ) is 0:
				return tmpname
			increment += 1
		return 0
			
			

	def storeGeneratedRef( self, o ):
		uniqueName = self.makeUnique( o.name )
		if  uniqueName is not 0:
			self.generatedObjects[uniqueName] = o
		elif self.verbose:
			print( "Impossible to create a unique name for ", o.name )
		return uniqueName

	# 3D OBJECTS

	def createPlane( self, x=0, y=0, z=0, time2live=0 ):
		if self.template_plane is 0:
			if self.verbose:
				print( "No plane template available." )
			return 0
		obj = self.scene.addObject( self.template_plane, self.root, time2live )
		self.move( obj, x,y,z )
		uname = self.storeGeneratedRef( obj )
		if self.verbose:
			print( "New plane named ", uname," successfully created." )
		return obj

	def createCube( self, x=0, y=0, z=0, time2live=0 ):
		if self.template_cube is 0:
			if self.verbose:
				print( "No cube template available." )
			return 0
		obj = self.scene.addObject( self.template_cube, self.root, time2live )
		self.move( obj, x,y,z )
		uname = self.storeGeneratedRef( obj )
		if self.verbose:
			print( "New cube named ", uname," successfully created." )
		return obj


	def createSphere( self, x=0, y=0, z=0, time2live=0 ):
		if self.template_sphere is 0:
			if self.verbose:
				print( "No sphere template available." )
			return 0
		obj = self.scene.addObject( self.template_sphere, self.root, time2live )
		self.move( obj, x,y,z )
		if self.verbose:
			print( "New sphere successfully created." )
		self.storeGeneratedRef( obj )
		return obj


	def createEmpty( self, x=0, y=0, z=0, time2live=0 ):
		if self.template_empty is 0:
			if self.verbose:
				print( "No empty template available." )
			return 0
		obj = self.scene.addObject( self.template_empty, self.root, time2live )
		self.move( obj, x,y,z )
		if self.verbose:
			print( "New empty successfully created." )
		self.storeGeneratedRef( obj )
		return obj

	def createSpot( self, x=0, y=0, z=0, time2live=0 ):
		if self.template_spot is 0:
			if self.verbose:
				print( "No spot template available." )
			return 0
		obj = self.scene.addObject( self.template_spot, self.root, time2live )
		self.move( obj, x,y,z )
		if self.verbose:
			print( "New spot successfully created." )
		self.storeGeneratedRef( obj )
		return obj

	def createCylinder( self, x=0, y=0, z=0, time2live=0 ):
		if self.template_cylinder is 0:
			if self.verbose:
				print( "No cylinder template available." )
			return 0
		obj = self.scene.addObject( self.template_cylinder, self.root, time2live )
		self.move( obj, x,y,z )
		if self.verbose:
			print( "New cylinder successfully created." )
		self.storeGeneratedRef( obj )
		return obj

	# 2D OBJECTS

	def createCircle( self, x=0, y=0, z=0, time2live=0 ):
		if self.template_2D_circle is 0:
			if self.verbose:
				print( "No circle template available." )
			return 0
		obj = self.scene.addObject( self.template_2D_circle, self.root, time2live )
		self.move( obj, x,y,z )
		if self.verbose:
			print( "New circle successfully created." )
		self.storeGeneratedRef( obj )
		return obj

	def createSquare( self, x=0, y=0, z=0, time2live=0 ):
		if self.template_2D_square is 0:
			if self.verbose:
				print( "No square template available." )
			return 0
		obj = self.scene.addObject( self.template_2D_square, self.root, time2live )
		self.move( obj, x,y,z )
		if self.verbose:
			print( "New square successfully created." )
		self.storeGeneratedRef( obj )
		return obj

	def createTriangle( self, x=0, y=0, z=0, time2live=0 ):
		if self.template_2D_triangle is 0:
			if self.verbose:
				print( "No triangle template available." )
			return 0
		obj = self.scene.addObject( self.template_2D_triangle, self.root, time2live )
		self.move( obj, x,y,z )
		if self.verbose:
			print( "New triangle successfully created." )
		self.storeGeneratedRef( obj )
		return obj

	def createFromTemplate( self, name, x=0, y=0, z=0, time2live=0 ):
		tmpl = 0		
		try:
			tmpl = self.templates[ name ]
		except KeyError:
			if self.verbose:
				print( "There is no", name, "in custom templates" )
			return 0
		obj = self.scene.addObject( tmpl, self.root, time2live )
		self.move( obj, x,y,z )
		if self.verbose:
			print( "New", name,"successfully created." )
		self.storeGeneratedRef( obj )
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
			obj = self.getObjectByName( o )
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
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0:
			return self.getOrientation( obj, absolute )

	def position( self, o, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0:
			return self.getPosition( obj, absolute )

#TODO
	def dimension( self, o ):
		obj = 0
		if type(o) is str:
			obj = self.getObjectByName( o )
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

	def showMouse( self ):
		self.input_mouse.visible = True

	def hideMouse( self ):
		self.input_mouse.visible = False			

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

	def textColor( self, arg1, arg2 = "NONE", arg3 = "NONE" ):

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
		self.tcolor = self.rgb2vector( r,g,b )

	def textSize( self, size ):
		self.tsize = size

	# arguments:
	# simple:
	# -	3 floats or 3 int
	# advanced:
	# -	if arg1 is a vector, it'll be used as a translation vector
	#	+ if arg2 is a vector also, it'll be used as rotation vector
	# -	if arg1 is an object or a string, the object position will
	#	be used as translation
	#	+ if arg2 is a vector, it'll be used as a translation vector
	#	+ if arg3 is a vector also, it'll be used as rotation vector
	# by default, text will be placed @ root
	def text( self, text, arg1=0, arg2=0, arg3=0 ):
		x = 0
		y = 0
		z = 0
		rx = 0
		ry = 0
		rz = 0

		if type( arg1 ) is mathutils.Vector():
			x = arg1.x
			y = arg1.y
			z = arg1.z
			if type( arg2 ) is mathutils.Vector():
				rx = arg2.x
				ry = arg2.y
				rz = arg2.z

		elif type( arg1 ) is bge.types.KX_GameObject or type( arg1 ) is str:
			if type( arg1 ) is str:
				arg1 = self.getObjectByName( arg1 )
			if arg1 is not 0:
				o = self.getPosition( arg1 )
				x = o.x
				y = o.y
				z = o.z
				# translation vector
				if type( arg2 ) is mathutils.Vector():
					x += arg2.x
					y += arg2.y
					z += arg2.z
				# rotation vector
				if type( arg3 ) is mathutils.Vector():
					rx = arg3.x
					ry = arg3.y
					rz = arg3.z
		
		elif type( arg1 ) is float and type( arg2 ) is float and type( arg3 ) is float:
			x = arg1
			y = arg2
			z = arg3

		elif type( arg1 ) is int and type( arg2 ) is int and type( arg3 ) is int:
			x = arg1
			y = arg2
			z = arg3
		
		width = bge.render.getWindowWidth()
		height = bge.render.getWindowHeight()
		ratiow = 1./width
		ratioh = 1./height
		bgl.glPushMatrix()
		bgl.glTranslatef( x,y,z )
#TODO transform angles to matrix!
		# bgl.glRotate( rx,ry,rz )
		bgl.glScalef( ratiow, ratioh, 0 )
		blf.position( self.font, 0,0,0 )
		blf.size( self.font, self.tsize, 300 )
		bgl.glColor3f( self.tcolor.x, self.tcolor.y, self.tcolor.z )
		blf.draw( self.font, text )
		bgl.glPopMatrix()
		

	def info( self, text, arg1=0, y=0, z=0 ):
		if self.configured is True and self.view_orientation is not 0:
			
			x = arg1
			if type( arg1 ) is mathutils.Vector():
				x = arg1.x
				y = arg1.y
				z = arg1.z
			elif type( arg1 ) is bge.types.KX_GameObject:
				o = self.getPosition( arg1 )
				x = o.x
				y = o.y
				z = o.z

			width = bge.render.getWindowWidth()
			height = bge.render.getWindowHeight()

			ratiow = 1./width
			ratioh = 1./height
			ratios = mathutils.Vector( ( self.view_orientation[0][3], self.view_orientation[1][3], self.view_orientation[2][3] ) ).length
			bgl.glPushMatrix()
			bgl.glTranslatef( x,y,z )
			buf = bgl.Buffer( bgl.GL_FLOAT, [16] )
			buf[0] = self.view_orientation[0][0]
			buf[1] = self.view_orientation[0][1]
			buf[2] = self.view_orientation[0][2]
			buf[3] = 0
			buf[4] = self.view_orientation[1][0]
			buf[5] = self.view_orientation[1][1]
			buf[6] = self.view_orientation[1][2]
			buf[7] = 0
			buf[8] = self.view_orientation[2][0]
			buf[9] = self.view_orientation[2][1]
			buf[10] = self.view_orientation[2][2]
			buf[11] = 0
			buf[12] = 0
			buf[13] = 0
			buf[14] = 0
			buf[15] = 1
			bgl.glMultMatrixf( buf )
			bgl.glScalef( ratiow, ratioh, 0 )
			blf.position( self.font, 0,0,0 )
			blf.size( self.font, self.tsize, 300 )
			bgl.glColor3f( self.tcolor.x, self.tcolor.y, self.tcolor.z )
			blf.draw( self.font, text )
			bgl.glPopMatrix()


##################
####### basic draw
##################

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
			o = self.getObjectByName( arg1 )
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
			o = self.getObjectByName( arg2 )
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
			obj = self.getObjectByName( o )
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
			obj = self.getObjectByName( o )
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
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0:
			vecscale = self.getScale( obj )
			vecscale.x = value
		
	def scaleY( self, o, value ):
		obj = 0
		if type(o) is str:
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0:
			vecscale = self.getScale( obj )
			vecscale.y += value
		
	def scaleZ( self, o, value ):
		obj = 0
		if type(o) is str:
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0:
			vecscale = self.getScale( obj )
			vecscale.z += value

####### translations

	def moveTo( self, o, arg1, y="NONE", z="NONE" ):
		obj = 0
		if type(o) is str:
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0 and ( y == "NONE" or z == "NONE" ):
			obj2 = self.getObjectByName( arg1 )
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
			obj = self.getObjectByName( o )
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
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			vecposition.x += value

	def moveY( self, o, value, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			vecposition.y += value
		
	def moveZ( self, o, value, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0:
			vecposition = self.getPosition( obj, absolute )
			vecposition.z += value

####### rotations

	def orient( self, o, neworientation  ):
		obj = 0
		if type(o) is str:
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0:
			self.applyOrientation( obj, neworientation )
			

	def pointTo( self, o, tracked ):
		obj = 0
		if type(o) is str:
			obj = self.getObjectByName( o )
		else:
			obj = o
		ot = 0
		if type(tracked) is str:
			ot = self.getObjectByName( tracked )
		else:
			ot = o
		if obj is not 0 and ot is not 0:
			vec1 = self.getPosition( obj, True )
			vec2 = self.getPosition( ot, True )
			vec = mathutils.Vector( ( vec2.x - vec1.x, vec2.y - vec1.y, vec2.z - vec1.z ) )			
			vec.normalize()
			print( vec )
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
			obj = self.getObjectByName( o )
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
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0:
			matorientation = self.getOrientation( obj, absolute )
			matorientation *= mathutils.Matrix.Rotation( value, 3, 'X')
			self.applyOrientation( obj, matorientation, absolute )
		
	def rotateY( self, o, value, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0:
			matorientation = self.getOrientation( obj, absolute )
			matorientation *= mathutils.Matrix.Rotation( value, 3, 'Y')
			self.applyOrientation( obj, matorientation, absolute )
		
	def rotateZ( self, o, value, absolute=True ):
		obj = 0
		if type(o) is str:
			obj = self.getObjectByName( o )
		else:
			obj = o
		if obj is not 0:
			matorientation = self.getOrientation( obj, absolute )
			matorientation *= mathutils.Matrix.Rotation( value, 3, 'Z')
			self.applyOrientation( obj, matorientation, absolute )


#############
####### utils
#############

	def isLowercase( self, char ):
		if type( char ) is str:
#TODO: test that char is lowercase!!!!
			if len( char ) == 0 :
				return True
			else:
				return False
		else:
			return True

	def char2lowercase( self, char ):
		if type( char ) is str and len( char ) == 1:
#TODO: transform char to lowercase!!!!
			char = char
		return char

	def char2ascii( self, char ):
		if type( char ) is str and len( char ) == 1:
			return ord( char )
		elif type( char ) is int:
			return char
		else:
			return -1

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

	def getGeneratedByName( self, name ):
		obj = 0
		try:
			obj = self.generatedObjects[name]
		except KeyError:
			obj = 0
		return obj

	def getObjectName( self, o ):
		for k in self.generatedObjects.keys():
			if o is self.generatedObjects[k]:
				return k
		for k in self.scene.objects.keys():
			if o is self.scene.objects[k]:
				return k
		return 0

	def getObjectByName( self, name ):
		obj = 0
		try:
			obj = self.generatedObjects[ name ]
		except KeyError:
			obj = 0
		if obj is 0:
			try:
				obj = self.scene.objects[ name ]
			except KeyError:
				obj = 0
			
		return obj
		
