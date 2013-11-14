from flask import Flask, json, jsonify, g, render_template, request, Response

import time
import subprocess

import glob

# configuration
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/_take_pictures')
def take_picture():
    # http://pymotw.com/2/subprocess/
    # subprocess.call('gphoto2 --capture-image-and-download --filename "%n.jpg" --interval 5 --frames 2', shell=True)

    return_code = subprocess.call('open photobooth.app/', shell=True)
    
    #subprocess.call(["open","photobooth.app/"])
    
    if return_code == 0:
        time.sleep(20)
    
    picture_list = glob.glob("static/pictures/*.JPG")
    
    return jsonify(status='1', pictures=picture_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)