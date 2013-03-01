# Copyright (C) Labomedia February 2012
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#############################################################################

import GameLogic as gl
from OSC.OSC import OSCClient, OSCMessage

# Get controller and owner
controller = gl.getCurrentController()
owner = controller.owner

client = OSCClient()
msg = OSCMessage()

# Example
a = owner['x']

# gl.send_to is a tuple in gl with ip and port
msg.setAddress("/blender/x")
msg.append(a)
client.sendto(msg, gl.send_to)
print('Send message example =', msg, "to ", gl.send_to)
