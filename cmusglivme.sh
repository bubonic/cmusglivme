#!/bin/sh

# requires: gliv, xrandr
# make sure you have both of these programs
#
# this will dipslay the art in the folder of currently playing track in a slideshow
# either in full screen mode or on attached display in full screen mode. it will decide for you.
# so make sure you fill your folders with a ton of cool art.
# it will dipslay the slideshow for as long as the duration of the track
#
# if you change the variable FULLSCREEN below to "Yes" this will display the slideshow on the primary
# display only. Good for when you mirror displays or don't have another monitor attached.
# set to 'No' it will display fullscreen on attached dispalys.  
#
# gliv has the nice option that the slideshow will fade pictures in/out.
#
# written by: bubonic
# 2018


#edit to "Yes" or "No" & define ARTIST_ART directory
FULLSCREEN="No"
ARTIST_ART="/media/bubonic/MyWD/Pictures/Artists/"

# creat list of artists from directory for fuzzy-matching
ls -1 "$ARTIST_ART" > /tmp/artists.list

status=$2
file_path=`echo $4 | sed 's/file //' | sed 's:^\(.*\)/.*$:\1:'`/
duration=`cmus-remote -Q | grep "duration" | sed 's/duration //'`
position=`cmus-remote -Q | grep "position" | sed 's/position //'`
TIMER=$((duration-position))
artist=`cmus-remote -Q | grep "tag artist" | sed 's/tag artist //' | sed -e "s/\b\(.\)/\u\1/g"`
album=`cmus-remote -Q | grep "tag album" | sed 's/tag album //' | head -1`
VGADISPLAY=`xrandr | grep "VGA-1" | awk '{print $2}'`
HDMIDISPLAY=`xrandr | grep "HDMI-1" | awk '{print $2}'`
DPDISPLAY=`xrandr | grep "DP-1" | awk '{print $2}'`

AAPATH=`~/.cmus/levenstein.pl "$artist" "/tmp/artists.list"`
ARTIST_ART_PATH="$ARTIST_ART$AAPATH"
#ARTIST_ART_PATH="$ARTIST_ART$artist"

if [ $VGADISPLAY = "connected" ]; then
	DIMENSION=`xrandr | grep "VGA-1" | awk '{print $3}'`

elif [ $HDMIDISPLAY = "connected" ]; then
	DIMENSION=`xrandr | grep "HDMI-1" | awk '{print $3}'`

elif [ $DPDISPLAY = "connected" ]; then
	DIMENSION=`xrandr | grep "DP-1" | awk '{print $3}'`
fi
if [ $status = "playing" ]; then
	#COVER_PHOTO=`ls -as "$file_path" | grep ".jpg\|.jpeg\|.png" | sort -g | tail -1 | awk '{for (i=2; i<NF; i++) printf $i " "; print $NF}'`
	if [ $FULLSCREEN = "Yes" ]; then
		sed -i 's/full-screen.*\=.False/full-screen	\= True/g' ~/.glivrc
		~/.cmus/discogsalbumart.py "$artist" "$album" "$file_path"
		gliv "$file_path" "$ARTIST_ART_PATH" &
	else
		sed -i 's/full-screen.*\=.True/full-screen	\= False/g' ~/.glivrc
		~/.cmus/discogsalbumart.py "$artist" "$album" "$file_path"
		gliv -G=$DIMENSION  "$file_path" "$ARTIST_ART_PATH" &
	fi
	pid=$!
	sleep $TIMER
	kill $pid
else
	pkill gliv
fi

