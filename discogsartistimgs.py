#!/usr/bin/env python

import re
import os
import sys
import urllib
import urllib2

from BeautifulSoup import BeautifulSoup

if len(sys.argv) < 3:
	print "Usage: %s 'Artist Name' '/directory/of/artist/images/" % sys.argv[0]
	sys.exit()


URLprefix = 'https://www.discogs.com/search/?q='
URLpostfix = '&type=artist'
rootURL = 'https://www.discogs.com'
imagesURL = [ ]
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
Artist = sys.argv[1].replace(' ','+')
imageDIR = sys.argv[2]

print "Artist search:\t %s" % sys.argv[1]
print "Search term:\t %s" % Artist

artistDIR = imageDIR + sys.argv[1]
searchURL = URLprefix + Artist + URLpostfix

request = urllib2.Request(searchURL)
request.add_header('User-Agent', USER_AGENT)
try:
	f = urllib2.urlopen(request)
	HTML = f.read()
except urllib2.HTTPError:        
        print "urllib2 HTTPError"
	sys.exit()

soup = BeautifulSoup(HTML)
firstMatch = soup.find('a', {'class' : 'search_result_title'})
artistMatchURL = firstMatch['href']

artistURL = rootURL + artistMatchURL
artistImagesURL = artistURL + '/images'

print "Artist URL:\t %s" % artistURL

request = urllib2.Request(artistImagesURL)
request.add_header('User-Agent', USER_AGENT)
try:
        f = urllib2.urlopen(request)
        HTML = f.read()
except urllib2.HTTPError:        
        print "urllib2 HTTPError"
	sys.exit()

soup = BeautifulSoup(HTML)

artistImagesBlock = soup.findAll('img')
i=0
for imgBlock in artistImagesBlock:
	imagesURL.append(imgBlock['src'])
	i += 1
i=0
del imagesURL[-1]
del imagesURL[0]

for imgURL in imagesURL:
	print "Image url %s:\t %s" % (i,imgURL)
	i += 1

print "Directory:\t %s" % artistDIR
if not os.path.exists(artistDIR):
    os.makedirs(artistDIR)

os.chdir(artistDIR)

for imgURL in imagesURL:
	filename = imgURL.split('/')[-1]
	print "Downloading:\t %s" % filename
	urllib.urlretrieve(imgURL, filename)

print "DONE."
