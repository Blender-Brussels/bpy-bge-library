import bge
from mathutils import Vector
from operator import attrgetter

scene = bge.logic.getCurrentScene()
obj = bge.logic.getCurrentController().owner

def deactivateSlide( s ):
    if 'video_path' in s:
        s['play'] = False

def activateSlide( s ):
    if 'video_path' in s:
        s['play'] = True

if 'slides' not in obj:
    
    obj['slides'] = []
    
    for o in scene.objects:
        if o.name[0:6] == "slide_":
            obj['slides'].append( o )
            deactivateSlide( o )
            
    obj['slides'] = sorted( obj['slides'], key=attrgetter('name'))
    obj['current_slides'] = 0
    obj['keyn'] = False
    obj['keyp'] = False
    obj['target'] = Vector( ( 0, 0, obj.worldPosition.z ) )
    print( obj['slides'] )

if obj.sensors['key_N'].positive:
    if not obj['keyn']:
        deactivateSlide( obj['slides'][ obj['current_slides'] ] )
        obj['current_slides'] += 1
        if ( obj['current_slides'] >= len( obj['slides'] ) ):
            obj['current_slides'] = 0
        activateSlide( obj['slides'][ obj['current_slides'] ] )
        obj['target'] = Vector( ( obj['current_slides'] * 2, 0, obj.worldPosition.z ) )
        obj['keyn'] = True
else:
    obj['keyn'] = False
    
if obj.sensors['key_P'].positive:
    
    if not obj['keyp']:
        deactivateSlide( obj['slides'][ obj['current_slides'] ] )
        obj['current_slides'] -= 1
        if ( obj['current_slides'] < 0 ):
            obj['current_slides'] = len( obj['slides'] ) - 1
        activateSlide( obj['slides'][ obj['current_slides'] ] )
        obj['target'] = Vector( ( obj['current_slides'] * 2, 0, obj.worldPosition.z ) )
        obj['keyp'] = True
        
else:
    
    obj['keyp'] = False


obj.worldPosition = Vector( (
                             obj.worldPosition.x + ( obj['target'].x - obj.worldPosition.x ) * 0.1,
                             obj.worldPosition.y + ( obj['target'].y - obj.worldPosition.y ) * 0.1,
                             obj.worldPosition.z + ( obj['target'].z - obj.worldPosition.z ) * 0.1
                             ) )