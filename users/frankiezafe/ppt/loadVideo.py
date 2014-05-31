import VideoTexture
from bge import logic as  GameLogic
contr = GameLogic.getCurrentController()
obj = contr.owner

# -- Check if the "video" property has been defined in the object
if 'video' not in obj:
    #-- Get the material that is using our texture
    #matID = VideoTexture.materialID(obj, 'MAa_video2014-02-20-17-41-16-163')
    # -- Create the video texture
    # GameLogic.video = VideoTexture.Texture(obj, matID)
    # Suppose 1st material is the video one
    obj['video'] = VideoTexture.Texture(obj, 0) 
    
    # -- Get the path to the video file from the 'video_path' object property
    movie = GameLogic.expandPath(obj['video_path'])

    # -- Load the file
    obj['video'].source = VideoTexture.VideoFFmpeg(movie)

    # play video in loop
    obj['video'].source.repeat = -1 

    # -- play the video
    obj['video'].source.play()
