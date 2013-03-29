import urllib2
import simplejson
import os

# this script gets maximum 64 images per search string
# adapts the searchreqs (search requests) and run
# images will be dumped in local folder

searchreqs = ['microsoft logo','linux logo','mac logo']
restrit2png = True

def downloadImg(url):
	global imgCount
	global tag
	
	prefix = ''
	if ( imgCount < 10 ):
		prefix = '000'
	elif ( imgCount < 100 ):
		prefix = '00'
	elif ( imgCount < 1000 ):
		prefix = '0'
		
	ext = '.png'
	if restrit2png == False:
		if url.find('.jpg') != -1 or url.find('.JPG') != -1 :
			ext = '.jpg'
		if url.find('.gif') != -1 or url.find('.GIF') != -1 :
			ext = '.gif'
			
	print imgCount, ' >> ', url
	try: 
		f = open( prefix + str(imgCount) + '_' + currentreq + ext, 'wb' )
		f.write(urllib2.urlopen(url).read())
		f.close()
		imgCount += 1
	except urllib2.HTTPError, err:
		print 'Error in ', url, ' >> ', err
	except urllib2.URLError, err:
		print 'Error in ', url, ' >> ', err

def googleApiImageRequest( label, string ):
	
	string = string.replace( ' ', '%20' )
	url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
       'v=1.0&' + 
       'q=' + string +
       '&userip=127.0.0.1' + 
       '&label=' + str( label ) +
       '&rsz=8' )

	if restrit2png == True:
		url += '&as_filetype=png'

	#request = urllib2.Request(url, None, {'Referer': 'https://github.com'})
	request = urllib2.Request(url, None)
	response = urllib2.urlopen(request)

	results = simplejson.load(response)

	# print results
	for r in results['responseData']['results']:
		downloadImg(r['url'])

currentreq = ''
imgCount = 0
for req in searchreqs:
	i = 0
	while i < 8:
		i += 1
		currentreq = req
		googleApiImageRequest( i, req )
	

