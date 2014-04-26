import bge
from ThreadOsc import *

# register a Thread OSC
try:
    bge.threadosc.exists()
    print( "bge.threadosc already started on", bge.threadosc.config )
    
except:
    bge.threadosc = ThreadOsc()
    oscConfs = { 0: ('127.0.0.1', 23000, 1024) }
    bge.threadosc.launchOSCs( oscConfs )
    bge.threadosc.start()
    print( "ThreadOsc is started" )