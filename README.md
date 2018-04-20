# cmusglivme
CMus artwork displayer. Displays a slideshow of artwork in folder of track being played by cmus.
This code was written to perform the following tasks:
* Locate attached displays
* Use gliv to display in fullscreen and image maximized the artwork of the Artist directory and artwork in album directory

# Usage

`git clone https://github.com/bubonic/cmusglivme`
`cd cmusglivme`
`cd .glivrc ~ && cp cmusglivme.sh ~/.cmus`

In cmus type the following:
`:set status_display_program=/home/user/.cmus/cmusglivme.sh`

## Options
You can set the following options in cmusglivme.sh at the beginning of the file:
`FULLSCREEN="No"
ARTIST_ART="/media/bubonic/MyWD/Pictures/Artists/"`
 
FULLSCREEN="Yes"
will have the function to display on the primary screen in fullscreen mode. If set to "No" (default) it will use attached displays and display the artwork in fullscreen mode on attached displays. Set "Yes" if you are using something like chromecast or don't have an attached display
 
 ARIST_ART="DIR"
is the directory containing art of the artist. The code will format the artist information provided by cmus in first letter uppercases. E.g., Kevin Saunderson. So make sure your directory name is in that format. I will be adding functionaly to fuzzy match the artist name with a given directory in the ARTIST_ART directory. 

#Enjoy!
