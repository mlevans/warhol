from flask import Flask, json, jsonify, g, render_template, request, Response
import time
import subprocess
import glob
import os
import shutil

# Create the app
app = Flask(__name__)

# Handle Configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'configuration.py')

#config_path = os.path.abspath(os.environ.get('PHOTOBOOTH_CONFIGURATION', CONFIG_PATH))
config_path = os.path.abspath(CONFIG_PATH)

if os.path.isfile(config_path):
    app.config.from_pyfile(config_path)
else:
    print 'You need a configuration file.'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/_take_pictures')
def take_pictures():
    # http://pymotw.com/2/subprocess/
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

            # Take the photos
            # Might want to add a delay, but not until we figure out a way to make it faster.
            time.sleep(2)
            for i in range(app.config['NUMBER_OF_PHOTOS']):
                subprocess.call('kill -USR1 ' + GPHOTO2_PID, shell=True)
                time.sleep(app.config['INTERVAL_TIME'])
        except subprocess.CalledProcessError, e:
            print 'Is gPhoto2 running?'
            print e.output

    elif app.config['USE_EOSUTILITY']:
        # Add a slight delay so that people can adjust themselves for the photos.
        time.sleep(2)
        subprocess.call('open photobooth.app/', shell=True)
        # Wait for the photos to finish
        time.sleep(app.config['SHOOT_DURATION'])
    
        #subprocess.call(["open","photobooth.app/"])
    else:
        raise Exception("You need to specify a program to automate your camera.")
    
    # Create a timestamp
    timestamp = str(int(time.time()))

    # Create a unique directory for the photos.
    try:
        os.makedirs("static/pictures/sets/" + timestamp)
        # os.chmod("static/pictures/sets/" + timestamp, 0777)
    except OSError as e:
        print e

    # Get the latest pictures
    picture_list = glob.glob("static/pictures/*.JPG")

    # Move the photos
    for i, picture_path in enumerate(picture_list):
        if EOSUTILITY or picture_path != "static/pictures/1.JPG":
            shutil.move(picture_list[i], "static/pictures/sets/" + timestamp)
    
    new_picture_list = glob.glob("static/pictures/sets/" + timestamp + "/*.JPG")

    # Add a timestamp to each image
    if new_picture_list:
        for i, picture_path in enumerate(new_picture_list):
            new_picture_list[i] = new_picture_list[i] + '?timestamp=' + timestamp
    else:
        raise Exception("No photos with that naming scheme were found!")
    
    return jsonify(status='0', pictures=new_picture_list)

if __name__ == '__main__':
    port = app.config.get('PORT') or 5000
    app.run(host='0.0.0.0', port=port)