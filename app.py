from flask import Flask, json, jsonify, g, render_template, request, Response

import time
import subprocess

import glob

# configuration
DEBUG = True
SECRET_KEY = 'development key'
GPHOTO = True
EOSUTILITY = False

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/_take_pictures')
def take_picture():
    # http://pymotw.com/2/subprocess/
    if GPHOTO:
        return_code = subprocess.call('gphoto2 --capture-image-and-download --filename "static/pictures/%n.JPG" --interval 4 --frames 2', shell=True)
    elif EOSUTILITY:
        return_code = subprocess.call('open photobooth.app/', shell=True)
    
        #subprocess.call(["open","photobooth.app/"])
    else:
        raise Exception("You need to specify a program to automate your camera.")
    
    if return_code == 0:
        time.sleep(20)

    picture_list = glob.glob("static/pictures/*.JPG")
    
    return jsonify(status='0', pictures=picture_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)