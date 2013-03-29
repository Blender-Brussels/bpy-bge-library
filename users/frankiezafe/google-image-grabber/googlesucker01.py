import urllib2
import simplejson
import os
import datetime

# this script gets maximum 64 images per search string
# adapts the searchreqs (search requests) and run
# images will be dumped in local folder

searchreqs = ['glitch art','glitch png','glitch color']
restrit2png = True

def downloadImg(url):

	global imgCount
	global currentreq
	global googlelog
	
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
	fname = currentreq.replace( ' ', '_' )
	try: 
		f = open( prefix + str(imgCount) + '_' + fname + ext, 'wb' )
		f.write(urllib2.urlopen(url).read())
		f.close()
		logline = prefix + str(imgCount) + '_' + fname + ext + ' >> ' + url + '\n'
		googlelog.write( logline )
		googlelog.flush()
		imgCount += 1
	except urllib2.HTTPError, err:
		print 'Error in ', url, ' >> ', err
	except urllib2.URLError, err:
		print 'Error in ', url, ' >> ', err

def googleApiImageRequest( start, string ):
	
	string = string.replace( ' ', '%20' )
	url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
       'v=1.0&' + 
       'q=' + string +
       '&userip=127.0.0.1' + 
       '&start=' + str( start * 8 ) +
       '&rsz=8' )

	if restrit2png == True:
		url += '&as_filetype=png'

	#request = urllib2.Request(url, None, {'Referer': 'https://github.com'})
	request = urllib2.Request(url, None)
	response = urllib2.urlopen(request)

	results = simplejson.load(response)

	# print results
	if ( results['responseData'] ):
		if ( results['responseData']['results'] ):	
			for r in results['responseData']['results']:
				downloadImg(r['url'])

def timeStamped( fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}' ):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

currentreq = ''
imgCount = 0

# creating a log file with the urls of the images + local filename
googlelog = open(timeStamped('googlesucker_log.txt'),'w')

for req in searchreqs:
	i = 0
	while i < 8:
		i += 1
		currentreq = req
		googleApiImageRequest( i, req )

googlelog.close()
	

