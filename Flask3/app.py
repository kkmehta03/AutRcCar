from importlib import import_module
import os
from flask import Flask, render_template, Response, make_response, url_for, redirect
import gpioController as g
from camera_pi import Camera
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen(Camera):
    """Video streaming generator function."""
    while True:
        frame = Camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        color_image = cv2.imdecode(np.fromstring(frame,dtype=np.uint8),cv2.IMREAD_COLOR)
        roi = color_image[120:240, :]
        image_array = roi.reshape(1,115200).astype(np.float32)

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
