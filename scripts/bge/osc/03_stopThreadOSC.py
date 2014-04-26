import bge
from ThreadOsc import *

# unregister & delete current Thread OSC
try:
    bge.threadosc.stop()
    bge.threadosc.killall()
    del bge.threadosc
    
except:
    print( "ThreadOsc is NOT started..." )