from bge import logic as GameLogic
contr = GameLogic.getCurrentController()
obj = contr.owner

# -- Check if the "video" property has been defined on "GameLogic"
if 'video' in obj:
    # -- The video has to be refreshed every frame because
    #    it is not a background process
    # print( True )
    obj['video'].refresh(True)