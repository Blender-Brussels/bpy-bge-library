#!/usr/bin/python3

import sys
import socket
import ProcessingBGE.OSC as lib_osc

# SUB CLASSES
class posc_oscclient( object ):
	
	def __init__( self ):
		self.port = 0
		self.socket = 0
		self.marker = []
		self.active = False

# MAIN CLASS

def singleton(cls):
 	return cls()

@singleton
class ProcessingOSC(object):

	def __init__(self):
		# basis configuration
		self.localhost = "127.0.0.1"
		self.blocking = 0
		self.timeout = 0.01
		# sockets
		self.sockets = []
		# buffer (may need adaptations)
		self.buffer_size = 1024
		# OSC objects
		self.osc_clients = [] # list of posc_oscclient
		self.osc_servers = []
		print( "OSC manager up and running!" )

	def getInstance( self ):
		return self

	def createOscClient( self, port=0, marker="/pbge" ):
		for oc in self.osc_clients:
			if oc.port == port:
				if oc.marker == marker:
					print("port already binded for this marker")
		tmpsocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		print( tmpsocket,"- port:",port )
		try:
			tmpsocket.bind(( self.localhost, port ))
			tmpsocket.setblocking( self.blocking )
			tmpsocket.settimeout( self.timeout )
			tmpsocket.setsockopt( socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffer_size )
			print('OSC port plugged: IP = {} Port = {} Buffer Size = {}'.format( self.localhost, port, self.buffer_size ))
		except:
			print('Not connected to IP = {} Port = {}'.format( self.localhost, port))
			return
		# storing the socket in the list
		tmposcc = posc_oscclient()
		tmposcc.port = port			
		tmposcc.socket = tmpsocket
		tmposcc.marker.append( marker )
		tmposcc.active = True
		self.osc_clients.append( tmposcc )




