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
from math import pi
from  mathutils import Euler

for key in gl.attribution.keys():
    if hasattr(gl, key):
        print( key,"=", getattr(gl, key) )
print()

# Get owner
controller = gl.getCurrentController()
owner = controller.owner

# Get obj
scene = gl.getCurrentScene()
objList = scene.objects
# example
# blob1 = objList["Blob1"]


# ------------ variable from help.txt ---------------- #
n2_egg_right = gl.n2_egg_right
n2_egg_left = gl.n2_egg_left
n1_egg_left = gl.n1_egg_left
n0_spam_back = gl.n0_spam_back
n0_spam_forward = gl.n0_spam_forward
n1_egg_right = gl.n1_egg_right

# ------------ some usefull functions ---------------- #
# Adapt this function to your own case
def obj_orientation(obj, alpha, beta, gamma):
    '''Set obj orientation, angle in degrees'''
    alpha = alpha*pi/180
    beta = beta*pi/180
    gamma = gamma*pi/180
    rot_in_euler = Euler([alpha, beta, gamma])
    obj.worldOrientation = rot_in_euler.to_matrix()

def obj_apply_local_angle(obj, alpha, beta, gamma):
    '''Apply local orientation, angle in degrees'''
    # set amount to rotate
    rotation = [-alpha*pi/360,-beta*pi/360,gamma*pi/360]

    # move game object, true for local axis
    owner.applyRotation(rotation, True)

    # Set angle for display scene
    world_angle = owner.localOrientation.to_euler()

# Set position
#obj.worldPosition = (x,y,z)
