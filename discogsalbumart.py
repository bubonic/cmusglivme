#!/usr/bin/env python

import re
import os
import sys
import urllib
import urllib2
import os.path

from BeautifulSoup import BeautifulSoup


if len(sys.argv) < 4:
    print "Usage: %s 'Artist Name' 'Album Name' '/directory/of/album/" % sys.argv[0]
    sys.exit()


URLprefix = 'https://www.discogs.com/search/?q='
URLpostfix = '&type=release'
rootURL = 'https://www.discogs.com'
artistExclude =['Feat.', 'Featuring']
imagesURL = [ ]
Albums = {'title' : [], 'href' : []}
Artists = []
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
Artist = sys.argv[1].replace(' ','+')
Album = sys.argv[2].replace(' ','+')
AlbumDIR = sys.argv[3]

print "Artist search:\t %s" % sys.argv[1]
print "Search term:\t %s" % Album

searchURL = URLprefix + Album + URLpostfix

print "Search URL:\t %s" % searchURL

request = urllib2.Request(searchURL)
request.add_header('User-Agent', USER_AGENT)
try:
    f = urllib2.urlopen(request)
    HTML = f.read()
except urllib2.HTTPError:        
    print "urllib2 HTTPError"
    sys.exit()

soup = BeautifulSoup(HTML)
AlbumMatches = soup.findAll('a', {'class' : 'search_result_title'})
ArtistMatches = soup.findAll('spanitemprop')

#print "ArtistMatches Block: %s" % ArtistMatches

for albumCODE in AlbumMatches:
    Albums['title'].append(albumCODE['title'])
    Albums['href'].append(albumCODE['href'])

j=0
artist_re = re.compile(sys.argv[1], re.DOTALL | re.IGNORECASE)    
artistExclude_re = re.compile('|'.join(artistExclude), re.DOTALL | re.IGNORECASE)
artistExclude2_re = re.compile('A.K.A', re.DOTALL | re.IGNORECASE)
for artistCODE in ArtistMatches:
    aExcludeMatch = artistExclude_re.search(artistCODE.getText())
    if aExcludeMatch is not None:
        print "Contains other artists, skipping"
    else:
        aExcludeMatch2 = artistExclude2_re.search(artistCODE.getText())
        if aExcludeMatch2 is None:
            print "Artist %s:\t %s" % (j,artistCODE.a.getText())
            Artists.append(artistCODE.a.getText())
            artist_reMatch = artist_re.search(Artists[-1])
            if artist_reMatch is not None:
                albumURL = rootURL + Albums['href'][j]
                print "Artist Match:\t %s" % Artists[j]
                print "Album Match:\t %s" % Albums['title'][j]
                print "Album Match URL:\t %s" % Albums['href'][j]
                break
            j += 1
        else:
            print "Artist %s:\t %s" % (j,artistCODE.a.getText())
            Artists.append(artistCODE.a.getText())
            artist_reMatch = artist_re.search(Artists[-1])
            if artist_reMatch is not None:
                albumURL = rootURL + Albums['href'][j]
                print "Artist Match:\t %s" % Artists[j]
                print "Album Match:\t %s" % Albums['title'][j]
                print "Album Match URL:\t %s" % Albums['href'][j]
                break


#albumURL = rootURL + Albums['href'][0]
print "Album URL result:\t %s" % albumURL


request = urllib2.Request(albumURL)
request.add_header('User-Agent', USER_AGENT)
try:
    f = urllib2.urlopen(request)
    HTML = f.read()
except urllib2.HTTPError:        
    print "urllib2 HTTPError"
    sys.exit()

soup = BeautifulSoup(HTML)
moreImagesBLOCK = soup.find('p', {'class' : 'image_gallery_more'})

releaseImgHREF = moreImagesBLOCK.a['href']
releaseImgURL = rootURL + releaseImgHREF

print "Release Image URL:\t %s" % releaseImgURL


request = urllib2.Request(releaseImgURL)
request.add_header('User-Agent', USER_AGENT)
try:
    f = urllib2.urlopen(request)
    HTML = f.read()
except urllib2.HTTPError:        
    print "urllib2 HTTPError"
    sys.exit()

soup = BeautifulSoup(HTML)
ReleaseImagesBlock = soup.findAll('img')
i=0
for imgBlock in ReleaseImagesBlock:
    imagesURL.append(imgBlock['src'])
    i += 1
i=0
del imagesURL[-1]
del imagesURL[0]

for imgURL in imagesURL:
    print "Image url %s:\t %s" % (i,imgURL)
    i += 1


os.chdir(AlbumDIR)

for imgURL in imagesURL:
    filename = imgURL.split('/')[-1]
    if not os.path.isfile(filename): 
        print "Downloading:\t %s" % filename
        urllib.urlretrieve(imgURL, filename)

print "DONE."
