'''
-------------------------------------------------------------------------------
Threaded OSC receiver for Python
-------------------------------------------------------------------------------
-----------------
Original Comments
-----------------
> Open SoundControl for Python
> Copyright (C) 2002 Daniel Holth, Clinton McChesney
>
> This library is free software; you can redistribute it and/or modify it under
> the terms of the GNU Lesser General Public License as published by the Free
> Software Foundation; either version 2.1 of the License, or (at your option) any
> later version.
>
> This library is distributed in the hope that it will be useful, but WITHOUT ANY
> WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
> PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
> details.
> You should have received a copy of the GNU Lesser General Public License along
> with this library; if not, write to the Free Software Foundation, Inc., 59
> Temple Place, Suite 330, Boston, MA 02111-1307 USA
> For questions regarding this module contact Daniel Holth <dholth@stetson.edu>
> or visit http://www.stetson.edu/~ProctoLogic/

This code is based [pyOSC](https://trac.v2.nl/wiki/pyOSC).

SimpleOSC:
	Copyright (c) Daniel Holth & Clinton McChesney.
pyOSC:
	Copyright (c) 2008-2010, Artem Baguinski <artm@v2.nl> et al., Stock, V2_Lab, Rotterdam, Netherlands.
Streaming support (OSC over TCP):
	Copyright (c) 2010 Uli Franke <uli.franke@weiss.ch>, Weiss Engineering, Uster, Switzerland.
Threading:
	Copyright (c) 2014 Frankie Zafe <frankie@frankiezafe.org>, Belgium
		
-------------------------------------------------------------------------------
'''

import re
import socket
import select
import string
import struct
import sys
import threading
import datetime
import time
import types
import array
import errno
import inspect
import math
import random
from contextlib import closing

##########################################OSC LIB - start

global version
version = ("0.3","6", "$Rev: 6382 $"[6:-2])

global FloatTypes
FloatTypes = [float]

global IntTypes
IntTypes = [int]

global NTP_epoch
from calendar import timegm
NTP_epoch = timegm((1900,1,1,0,0,0)) # NTP time started in 1 Jan 1900
del timegm

global NTP_units_per_second
NTP_units_per_second = 0x100000000 # about 232 picoseconds

try:
    from numpy import typeDict

    for ftype in ['float32', 'float64', 'float128']:
        try:
            FloatTypes.append(typeDict[ftype])
        except KeyError:
            pass
        
    for itype in ['int8', 'int16', 'int32', 'int64']:
        try:
            IntTypes.append(typeDict[itype])
            IntTypes.append(typeDict['u' + itype])
        except KeyError:
            pass
        
    # thanks for those...
    del typeDict, ftype, itype
    
except ImportError:
    pass

class OSCError(Exception):
    """Base Class for all OSC-related errors
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

def _readString(data):
    """Reads the next (null-terminated) block of data
    """
    length   = data.find(b'\0')
    nextData = int(math.ceil((length+1) / 4.0) * 4)
    return (data[0:length].decode('latin1'), data[nextData:])

def _readBlob(data):
    """Reads the next (numbered) block of data
    """
    
    length   = struct.unpack(">i", data[0:4])[0]
    nextData = int(math.ceil((length) / 4.0) * 4) + 4
    return (data[4:length+4], data[nextData:])

def _readInt(data):
    """Tries to interpret the next 4 bytes of the data
    as a 32-bit integer. """
    
    if(len(data)<4):
        print("Error: too few bytes for int", data, len(data))
        rest = data
        integer = 0
    else:
        integer = struct.unpack(">i", data[0:4])[0]
        rest    = data[4:]

    return (integer, rest)

def _readLong(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit signed integer.
     """

    high, low = struct.unpack(">ll", data[0:8])
    big = (int(high) << 32) + low
    rest = data[8:]
    return (big, rest)

def _readTimeTag(data):
    """Tries to interpret the next 8 bytes of the data
    as a TimeTag.
     """
    high, low = struct.unpack(">LL", data[0:8])
    if (high == 0) and (low <= 1):
        time = 0.0
    else:
        time = int(NTP_epoch + high) + float(low / NTP_units_per_second)
    rest = data[8:]
    return (time, rest)

def _readFloat(data):
    """Tries to interpret the next 4 bytes of the data
    as a 32-bit float. 
    """
    
    if(len(data)<4):
        print("Error: too few bytes for float", data, len(data))
        rest = data
        float = 0
    else:
        float = struct.unpack(">f", data[0:4])[0]
        rest  = data[4:]

    return (float, rest)

def _readDouble(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit float. 
    """
    
    if(len(data)<8):
        print("Error: too few bytes for double", data, len(data))
        rest = data
        float = 0
    else:
        float = struct.unpack(">d", data[0:8])[0]
        rest  = data[8:]

    return (float, rest)

def _readFalse(data):
    """In case of boolean: False"""
    return(False, data )

def _readTrue(data):
    """In case of boolean: True"""
    return(True, data)

def decodeOSC( data ):
    """Converts a binary OSC message to a Python list. 
    """
    table = {"i":_readInt, "f":_readFloat, "s":_readString, "b":_readBlob, "d":_readDouble, "t":_readTimeTag, "F":_readFalse, "T":_readTrue}
    decoded = []
    address,  rest = _readString(data)
    if address.startswith(","):
        typetags = address
        address = ""
    else:
        typetags = ""

    if address == "#bundle":
        time, rest = _readTimeTag(rest)
        decoded.append(address)
        decoded.append(time)
        while len(rest)>0:
            length, rest = _readInt(rest)
            decoded.append(decodeOSC(rest[:length]))
            rest = rest[length:]

    elif len(rest)>0:
        if not len(typetags):
            typetags, rest = _readString(rest)
        decoded.append(address)
        decoded.append(typetags)
        if typetags.startswith(","):
            for tag in typetags[1:]:
                value, rest = table[tag](rest)
                decoded.append(value)
        else:
            raise OSCError("OSCMessage's typetag-string lacks the magic ','")

    return decoded

######
#
# Utility functions
#
######

def hexDump(bytes):
    """ Useful utility; prints the string in hexadecimal.
    """
    print("byte   0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F")

    if isinstance(bytes,str):
        bytes = bytes.encode('latin1')
    num = len(bytes)
    for i in range(num):
        if (i) % 16 == 0:
            line = "%02X0 : " % (i/16)
        line += "%02X " % bytes[i]
        if (i+1) % 16 == 0:
            print("%s: %s" % (line, repr(bytes[i-15:i+1])))
            line = ""

    bytes_left = num % 16
    if bytes_left:
        print("%s: %s" % (line.ljust(54), repr(bytes[-bytes_left:])))

##########################################OSC LIB - end

class ThreadOsc( threading.Thread ):
    
    def exists(self):
        return True
    
    def launchOSCs(self, config):
        self.__stop = False
        self.listeners = []
        self.max_delay_for_listeners = 5 # ~ 5 millis
        self.status = "NOT CONNECTED"
        self.connected = []
        self.socket = []
        self.config = config
        for i in range( len( self.config ) ):
            self.connected.append(False)
            self.socket.append(0)
            # ------------ set some var ---------------- #
            self.tempo = 0
            # ------------ connecting ---------------- #
            if not self.connected[i] :
                self.socket[i] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    # self.socket[i].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, self.config[i][2] )
                    self.socket[i].setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.config[i][2] )
                    self.socket[i].bind(( self.config[i][0], self.config[i][1] ))
                    self.socket[i].setblocking(0)
                    self.socket[i].settimeout(0.01)
                    print('Plug : IP = {} Port = {} Buffer Size = {} Instance = {}'.format( self.config[i][0], self.config[i][1], self.config[i][2], i))
                    self.connected[i] = True
                except:
                    print('No connected to IP = {} Port = {}'.format( self.config[i][0], self.config[i][1] ))
        
        cnum = len( self.config )
        cconn = 0
        for i in range( len( self.config ) ):
            if self.connected[i]:
                cconn += 1
        if cconn == cnum:
            self.status = "ALL CONNECTED"
            print( "ThreadOsc status: ALL CONNECTED {}/{}".format( cconn, cnum ) )
        elif cconn > 0:
            self.status = "FAILED TO CONNECT"
            print( "ThreadOsc status: FAILED TO CONNECT, up & runnig:  {}/{}".format( cconn, cnum ) )
        else:
            print( "ThreadOsc status: NOT CONNECTED {}/{}".format( cconn, cnum ) )
    
    def stop(self):
        self.__stop = True
    
    def killall(self):
        # trying to end all sockets correctly
        for i in range( len( self.config ) ):
                if self.connected[i] :
                    try:
                        print( "closing socket", self.config[i][0], self.config[i][1] )
                        # self.socket[i].shutdown(1) -> doesn't work, don't know why...
                        self.socket[i].close()
                        del self.socket[i]
                        print( "socket", self.config[i][0], self.config[i][1], "closed" )
                    except:
                        print( "fucked up the sockets shutdown..." )
        self.config = []
        self.connected = []
        self.socket = []
    
    def addListener( self, obj ):
        self.listeners.append( obj )
        
    def removeListener( self , obj ):
        for l in self.listeners:
            if l == obj:
                self.listeners.remove( obj )
    
    def run(self):
        while not self.__stop :
            time.sleep( 0.001 )
            # print( "thread runs!:", len( config ), ">", type( root ), "&", type( tanuki ) )
            for i in range( len( self.config ) ):
                if self.connected[i] :
                    try:
                        while 1:
                            raw_data = self.socket[i].recv( self.config[i][2] )
                            data = decodeOSC( raw_data )
                            for l in self.listeners:
                                # listener could be locked while data copy
                                # waiting for it to be unlocked, but not too long :)
                                enabled = True
                                if l.rcvmutex:
                                    delay = 0
                                    while l.rcvmutex and delay < self.max_delay_for_listeners:
                                        time.sleep( 0.001 )
                                        delay += 1
                                    if l.rcvmutex:
                                        enabled = False
                                # YES! unlocked -> let's dump data into it
                                if enabled:
                                    l.rcvdata.append( data )
                            # a bit of security
                            if self.__stop:
                                return
                    except socket.error:
                        e = 1
                    except socket.timeout:
                        e = 2
                    # a bit of security
                    if self.__stop:
                        return
        print( "stopping thread" )

