#!/usr/bin/python3

import sys
import socket
import ProcessingBGE.OSC as lib_osc

# SUB CLASSES
class posc_message( object ):
	def __init__( object ):
		address = 0
		data = []

class posc_oscclient( object ):
	
	def __init__( self ):
		self.port = 0
		self.socket = 0
		self.markers = []
		self.active = False

# MAIN CLASS

def singleton(cls):
 	return cls()

@singleton
class ProcessingOSC():
	
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
		self.osc_receivers = [] # list of posc_oscclient
		self.osc_senders = []
		self.osc_messages = [] # list of posc_message
		self.pending_messages = 0
		print( "OSC manager up and running!" )

	def getInstance( self ):
		return self

	def createOscReceiver( self, port=0, marker="/pbge" ):
		for oscr in self.osc_receivers:
			if oscr.port == port:
				for m in oscr.markers:
					if m == marker:
						return
						print("receiver", oscr.port,"already binded for this marker")
				else:
					oscr.markers.append( marker )
					print("receiver", oscr.port,"has a new marker:", oscr.markers)
					return
		tmpsocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		# the port may already be locked by a previous run =>
#TODO check unbind doc!!! 
#		tmpsocket.connect( ( self.localhost, port ) )			
#		tmpsocket.dup()
#		tmpsocket.close()
		print( tmpsocket,"- port:",port )
		try:
			tmpsocket.bind( ( self.localhost, port ) )
			tmpsocket.setblocking( self.blocking )
			tmpsocket.settimeout( self.timeout )
			tmpsocket.setsockopt( socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffer_size )
		except socket.error as e:
			print('Not connected to IP = {} Port = {}'.format( self.localhost, port), "error:", e )
			return
		# storing the socket in the list
		tmposcc = posc_oscclient()
		tmposcc.port = port			
		tmposcc.socket = tmpsocket
		tmposcc.markers.append( marker )
		tmposcc.active = True
		self.osc_receivers.append( tmposcc )
		print( "new osc receiver binded to ", port, "- markers:", tmposcc.markers )

	def update( self ):
		# clearing past messages
		self.osc_messages.clear()
		for oscr in self.osc_receivers:
			try:
				raw_data = oscr.socket.recv( self.buffer_size )
				data = lib_osc.decodeOSC(raw_data)
				tmpmarker = data[0]
				accepted = False
				for m in oscr.markers:
					if tmpmarker == m:
						# message is valid for this port
						# so adding it into the received messages list
						tmpmsg = posc_message()
						dcounter = 0
						accepted = True
						for d in data:
							if dcounter == 0:
								tmpmsg.address = d
							else:
								tmpmsg.data.append( d )
							dcounter += 1
						self.osc_messages.append( tmpmsg )
						break
				if accepted is False:
					print( "receiver", oscr.port,"is not accepting messages with'",tmpmarker,"' address" )
			except socket.error as e:
				print( "socket error on receiver", oscr.port, "error:", e )
				pass
	




