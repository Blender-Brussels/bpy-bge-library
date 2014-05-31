from bge import logic as GameLogic
contr = GameLogic.getCurrentController()
obj = contr.owner

# toggle playing
if obj['video'].source.status == 2 :
    obj['video'].source.stop()
    print( "Stop" )
elif obj['video'].source.status == 3 :
    obj['video'].source.play()
    print( "Play" )
else :
    print ( "Error on videoControls: GameLogic.video.source.status : " + obj['video'].source.status )
