Threaded OSC receiver
=================================

This class is intended to solve a problem i noticed in production:
When the OSC stream becomes important and the game engine is heavily loaded,
mixing netwok parsing and 3D rendering result in a dramatic fall of fps.

To avoid messages loss (and use two cores), the networking has been decoupled from the BGE thread.

To get the messages, you have to register a listener in the thread via the **addListener** method
The thread trusts the fact that you know what you're doing, so it doesn't check if listeners exist, 
meaning that you have to unregister the object in the thread via **removeListener** method before deleting it.

Each listener must have 2 data fields: **rcvmutex**(boolean) and **rcvdata**(list).
Once again, thread does not check if these fields are in the listener before accessing them.

If you are not familiar with multi-threading, the listener rcvmutex is used to pause the thread while copying the
values in the listener.

Suggested way to access data in the listener:

    self.rcvmutex = True
    tmp = list( self.rcvdata )
    self.rcvdata = []
    self.rcvmutex = False

This code is based [pyOSC](https://trac.v2.nl/wiki/pyOSC).

The **ThreadOsc.py** contains a OSC client that 
  - collects all the messages form one to many osc port, 
  - parse them,
  - send data to any object registered in it

The 3 steps examples will help you to understand the basics.

**To keep in mind** : The thread will not stop by itself when you stop the game engine > you have to stop it and kill it explicitly!
