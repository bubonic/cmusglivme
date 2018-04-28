# cmusglivme
CMus artwork displayer. Displays a slideshow of artwork in folder of track being played by cmus.
This code was written to perform the following tasks:
* Locate attached displays
* Use gliv to display in fullscreen and image maximized the artwork of the Artist directory and artwork in album directory

## Requirements
* xrandr
* gliv

That's all. 

# Usage

`git clone https://github.com/bubonic/cmusglivme`

`cd cmusglivme`

`chmod +x cmusglivme.sh levenstein.pl`

`cp .glivrc ~/ && cp cmusglivme.sh levenstein.pl ~/.cmus`

In cmus type the following:
`:set status_display_program=/home/user/.cmus/cmusglivme.sh`


## Options
You can set the following options in cmusglivme.sh at the beginning of the file:

`FULLSCREEN="No"`

`ARTIST_ART="/media/bubonic/MyWD/Pictures/Artists/"`
 
FULLSCREEN="Yes"
will have the function to display on the primary screen in fullscreen mode. If set to "No" (default) it will use attached displays and display the artwork in fullscreen mode on attached displays. Set "Yes" if you are using something like chromecast or don't have an attached display
 
ARIST_ART="DIR"
is the directory containing art of the artist. The code will use the levenstein.pl fuzzy matching algorithm to come up with a directory of the best match of the artist ID3 tag provided by cmus. 

# discogsartistimgs.py

This little python app will take two argumets: 1) The Artist name in quotes, e.g. "John Digweed" 2) The location where you store your artists images for cmusglivme.sh

`Usage: ./discogsartistimgs.py 'Artist Name' '/directory/of/artist/images/`

It will download all the artist images from discogs for the first artist found in the search term, so be precise. It will create a directory '/directory/of/artist/images/Arist Name` and download all images to that folder. 
Used in conjunction with cmusglivme.sh this will give you all the art you need for your party. 

# Enjoy!
