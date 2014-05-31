import bge

scene = bge.logic.getCurrentScene()
obj = bge.logic.getCurrentController().owner

if 'slides' not in obj:
    for o in scene.objects:
        print( o )