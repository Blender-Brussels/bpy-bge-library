from bge import logic as GameLogic
contr = GameLogic.getCurrentController()
obj = contr.owner

# -- Check if the "video" property has been defined on "GameLogic"
if 'video' in obj:
    # -- The video has to be refreshed every frame because
    #    it is not a background process
    # print( True )
    if obj['play'] == True and obj['video_was_playing'] == False:
        obj['video'].source.play()
        obj['video_was_playing'] = True
    
    if obj['play'] == False and obj['video_was_playing'] == True:
        obj['video'].source.stop()
        obj['video_was_playing'] = False
    
    if obj['play']:
        obj['video'].refresh(True)