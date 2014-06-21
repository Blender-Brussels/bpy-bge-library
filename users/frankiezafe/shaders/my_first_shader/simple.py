import bge, random, mathutils

root = bge.logic.getCurrentScene().objects["root"]
cam = bge.logic.getCurrentScene().objects[ "Camera" ]
clight = bge.logic.getCurrentScene().objects[ "Camlight" ]

if "cam_rot" not in root:
    root["cam_rot"] = mathutils.Euler( (0,0,0), 'XYZ' )
    root["cam_pos"] = mathutils.Vector( cam.worldPosition )
    root["cam_ori"] = mathutils.Matrix( cam.worldOrientation )
    root["clight_pos"] = mathutils.Vector( clight.worldPosition )
    root["cam_ori"] = mathutils.Matrix( cam.worldOrientation )
    root["clight_ori"] = mathutils.Matrix( clight.worldOrientation )
    root["glitchspeed"] = -1
    
root["percentage"] = random.random()
root["timer"] = random.random() * 1000
# root["xmin"] = random.random() * 0.5
# root["xmax"] = 0.5 + random.random() * 0.5
ty1 = 0.2 + random.random() * 0.7
ty2 = random.random() * 0.25
root["ymin"] += ( ( ty1 - ty2 ) - root["ymin"] ) * 0.1
root["ymax"] += ( ( ty1 + ty2 ) - root["ymax"] ) * 0.1

newd = random.random() * 0.1
root["glitchdecal"] += ( newd - root["glitchdecal"] ) * 0.01
root["glitchdecalstart"] = 0.2 + random.random() * 0.2
root["glitchdecalend"] = 0.6 + random.random() * 0.2


root["glitchd"] += 0.0008 * root["glitchspeed"]
if root["glitchd"] > 0.17 :
    root["glitchd"] = 0.17
    root["glitchspeed"] *= -1
elif root["glitchd"] < 0.03 :
    root["glitchd"] = 0.03
    root["glitchspeed"] *= -1

root["cam_rot"].y += 0.003
root["cam_rot"].z += 0.002

np = mathutils.Vector( root["cam_pos"] )
np.rotate( root["cam_rot"] )
cam.worldPosition = np
np = mathutils.Matrix( root["cam_ori"] )
np.rotate( root["cam_rot"] )
cam.worldOrientation = np

np = mathutils.Vector( root["clight_pos"] )
np.rotate( root["cam_rot"] )
clight.worldPosition = np
np = mathutils.Matrix( root["clight_ori"] )
np.rotate( root["cam_rot"] )
clight.worldOrientation = np

# cube = bge.logic.getCurrentScene().objects[ "Cube.006" ]
# cube.worldPosition.x += 1 - random.random() * 2