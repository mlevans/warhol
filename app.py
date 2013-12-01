#!/usr/bin/env python

from flask import Flask, jsonify, render_template, request
import time
import subprocess
import glob
import sys
import os
import shutil

# Create the app
app = Flask(__name__)

"""
# Default Configuration so things work if there's no configuration.py
DEBUG = True
SECRET_KEY = 'Change this'
PORT = 5000
USE_GPHOTO = False
USE_EOSUTILITY = True
INTERVAL_TIME = 5 # in seconds
NUMBER_OF_PHOTOS = 4 # Number of photos per shoot
SHOOT_DURATION = INTERVAL_TIME * NUMBER_OF_PHOTOS

app.config.from_object(__name__)
"""

# Now for the custom configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'configuration.py')

#config_path = os.path.abspath(os.environ.get('PHOTOBOOTH_CONFIGURATION', CONFIG_PATH))
config_path = os.path.abspath(CONFIG_PATH)

if os.path.isfile(config_path):
    app.config.from_pyfile(config_path)
else:
    print 'You should add a configuration file.'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/handle_photo_list')
def handle_photo_list():
    timestamp = request.args.get('timestamp')

    # Get the latest pictures
    picture_list = glob.glob("static/pictures/*.JPG")

    if len(picture_list) > 3:
        # Move the photos
        for i, picture_path in enumerate(picture_list):
            if (app.config['USE_EOSUTILITY'] and not app.config['USE_GPHOTO']) or picture_path != "static/pictures/1.JPG":
                shutil.move(picture_list[i], "static/pictures/sets/" + timestamp)
    else:
        return jsonify(status='1')
        #raise Exception("No photos with that naming scheme were found!")

    # Get a list of the pictures that have been moved
    new_picture_list = glob.glob("static/pictures/sets/" + timestamp + "/*.JPG")

    # Add a timestamp to each image
    if new_picture_list:
        for i, picture_path in enumerate(new_picture_list):
            new_picture_list[i] = new_picture_list[i] + '?timestamp=' + timestamp
        return jsonify(status='0', pictures=new_picture_list)
    else:
        #return None
        raise Exception("No photos with that naming scheme were found!")

@app.route('/_take_pictures')
def take_pictures():
    ###
    # TODO: Find previous pictures if any and delete them
    ###
    if app.config['USE_GPHOTO']:
        # FIRST METHOD
        # For capture with 6 second delay
        # return_code = subprocess.call('gphoto2 --capture-image-and-download --filename "static/pictures/%n.JPG" --interval 4 --frames 2', shell=True)
        
        # SECOND METHOD
        # For instantaneous capture
        # Get PID
        try:
            pids = subprocess.check_output(["pgrep","gphoto2"])

            split_pids = pids.split('\n')

            if len(split_pids) == 2 and not split_pids[1]:
                GPHOTO2_PID = split_pids[0]
            else:
                raise Exception("It seems like there are multiple gphoto processes happening.")
        except subprocess.CalledProcessError, e:
            print 'Is gPhoto2 running?', e.output
            sys.exit(1)

        # Take the photos

        # Add a slight delay so that people can adjust themselves for the photos.
        time.sleep(2)
        
        for i in range(app.config['NUMBER_OF_PHOTOS']):
            #subprocess.call('kill -USR1 ' + GPHOTO2_PID, shell=True)
            gphoto_proc = subprocess.Popen(["kill", "-USR1", GPHOTO2_PID],stdout=subprocess.PIPE)

            stdoutdata, stderrdata = gphoto_proc.communicate()

            print 'stdout: ',stdoutdata, 'stderr: ', stderrdata

            # Wait for the photos to finish
            # time.sleep(app.config['INTERVAL_TIME'])
    elif app.config['USE_EOSUTILITY']:
        #time.sleep(60)
        # Add a slight delay so that people can adjust themselves for the photos.
        time.sleep(2)
        
        # Open the photobooth app
        # subprocess.call('open photobooth.app/', shell=True)
        # subprocess.call(["open","photobooth.app/"])
        photobooth_proc = subprocess.Popen(["open", "photobooth.app"],stdout=subprocess.PIPE)
        stdoutdata, stderrdata = photobooth_proc.communicate()
        print 'stdout: ',stdoutdata, 'stderr: ', stderrdata

        # Wait for the photos to finish
        # time.sleep(app.config['SHOOT_DURATION'])
    else:
        raise Exception("You need to specify a program to automate your camera.")
    
    # Create a timestamp
    timestamp = str(int(time.time()))
    #g.timestamp = timestamp

    #print 'g timestamp', g.timestamp

    # Create a unique directory for the photos.
    try:
        os.makedirs("static/pictures/sets/" + timestamp)
        # os.chmod("static/pictures/sets/" + timestamp, 0777)
    except OSError as e:
        print e
    
    return jsonify(status='0', timestamp=timestamp)

if __name__ == '__main__':
    port = app.config.get('PORT') or 5000
    app.run(host='0.0.0.0', port=port)