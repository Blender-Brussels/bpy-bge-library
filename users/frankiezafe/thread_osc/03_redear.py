import bge
from mathutils import Euler, Matrix

class OSCReader():
    
    def __init__(self):
        self.name = 'oscreader_default'
        # array to hold data from the OSC thread
        self.rcvdata = []
        # mutex to block the OSC thread while copying
        self.rcvmutex = False
        self.listening = False
        self.rot = Euler()
    
    def startListen(self, oscthread ):
        if self.listening:
            print( "you can, in theory, register this object in many threads, but why would you want to do so?" )
            return
        oscthread.addListener( self )
        self.listening = True
    
    def stopListen(self, oscthread = 0 ):
        if oscthread != 0:
            oscthread.removeListener( self )
        self.listening = False
    
    def update( self ):
        
        # the reader is not linked to a thread, no need to go further
        if not self.listening:
            return
        
        self.rcvmutex = True
        tmp = list( self.rcvdata )
        self.rcvdata = []
        self.rcvmutex = False
        
        if len( tmp ) == 0:
            return
        
        print( self.name, "received", len( tmp ), "message(s)" )
        for d in tmp:
            if d[0] == "/control/rotation":
                self.rot.x = -float( d[2] )
                self.rot.y = -float( d[3] )
                self.rot.z = -float( d[4] )

oscthreadExists = False
try:
    # required to link the reader to the thread...
    oscthreadExists = bge.threadosc.exists()
except:
    oscthreadExists = False

owner = bge.logic.getCurrentController().owner

if not 'oscr' in owner:
    
    owner[ 'oscr' ] = OSCReader()
    print( "OSC Reader instanciated for", owner.name )
    
else:
    
    oscr = owner[ 'oscr' ]
    oscr.update()
    owner.worldOrientation = oscr.rot.to_matrix()
    
    if oscthreadExists and not oscr.listening:
        oscr.startListen( bge.threadosc )
        print( "register" , oscr.name, "from", owner.name ,"in OSC thread" )
    
    elif not oscthreadExists and oscr.listening:
        oscr.stopListen()
        print( "unregister" , oscr.name, "from", owner.name ,"in OSC thread" )