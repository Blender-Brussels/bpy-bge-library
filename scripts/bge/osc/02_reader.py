import bge

class OSCReader():
    
    def __init__(self):
        self.name = 'oscreader_default'
        # array to hold data from the OSC thread
        self.rcvdata = []
        # mutex to block the OSC thread while copying
        self.rcvmutex = False
        self.listening = False
    
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
            i = 0
            for m in d:
                print( "[", i ,"]: ", m )
                i += 1

oscthreadExists = False
try:
    # required to link the reader to the thread...
    oscthreadExists = bge.threadosc.exists()
except:
    oscthreadExists = False

owner = bge.logic.getCurrentController().owner

if not 'oscreader1' in owner:
    
    owner[ 'oscreader1' ] = OSCReader()
    owner[ 'oscreader1' ].name ="OSCr1"
    
    owner[ 'oscreader2' ] = OSCReader()
    owner[ 'oscreader2' ].name ="OSCr2"
    
    print( "OSC Readers instanciated" )
    
else:
    
    oscr1 = owner[ 'oscreader1' ]
    oscr1.update()
    
    if oscthreadExists and not oscr1.listening:
        oscr1.startListen( bge.threadosc )
        print( "register" , oscr1.name ,"in OSC thread" )
    
    elif not oscthreadExists and oscr1.listening:
        oscr1.stopListen()
        print( "unregister" , oscr1.name ,"in OSC thread" )
    
    oscr2 = owner[ 'oscreader2' ]
    oscr2.update()
    
    if oscthreadExists and not oscr2.listening:
        oscr2.startListen( bge.threadosc )
        print( "register" , oscr2.name ,"in OSC thread" )
    
    elif not oscthreadExists and oscr2.listening:
        oscr2.stopListen()
        print( "unregister" , oscr2.name ,"in OSC thread" )
