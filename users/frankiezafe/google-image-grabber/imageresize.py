import os
import sys
from PIL import Image

outputpath = 'thumbs'
maxwidth = 400
maxheight = 400

def resize(folder, fileName):
	
	global outputpath
	
	try:
	
		filePath = os.path.join(folder, fileName)
		im = Image.open(filePath)
		w, h  = im.size
		thumbw, thumbh = im.size
		
		if w > h and w > maxwidth:
			thumbw = maxwidth
			thumbh = float(h) * ( float(maxwidth) / float(w) )
		elif h > maxheight:
			thumbw = float(w) * ( float(maxheight) / float(h) )
			thumbh = maxheight
		
		thumbsize = int(thumbw), int(thumbh)
		print thumbsize
		newIm = im.resize( thumbsize, Image.NEAREST )
		# i am saving a copy, you can overrider orginal, or save to other folder
		if ( outputpath.__len__() > 0 ):
			filePath = outputpath + '/' + filePath
		newIm.save(filePath+"_thumb.png")
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
	except ValueError:
		print "Could not convert data to an integer."
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise

def bulkResize(imageFolder):
    imgExts = ["png", "bmp", "jpg", "gif"]
    for path, dirs, files in os.walk(imageFolder):
    	if len(dirs) > 0:  
            dirs.pop()
        for fileName in files:
            ext = fileName[-3:].lower()
            if ext not in imgExts:
                continue
            resize(path, fileName)

if __name__ == "__main__":
    imageFolder = '.'
    if not os.path.exists(outputpath):
    	os.makedirs(outputpath) 
    bulkResize(imageFolder)
