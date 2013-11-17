# Run from root directory
INITIAL_PICTURE=static/pictures/1.JPG

if [ -f $INITIAL_PICTURE ];
then
	rm $INITIAL_PICTURE
fi

gphoto2 --capture-image-and-download --filename "static/pictures/%n.JPG" -F 100000 -I -1
