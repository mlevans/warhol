from flask import Flask, json, jsonify, g, render_template, request, Response

import subprocess

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
    subprocess.call('gphoto2 --capture-image-and-download --filename "%n.jpg" --interval 5 --frames 2', shell=True)

    return jsonify(status='1')

if __name__ == '__main__':
    app.run()