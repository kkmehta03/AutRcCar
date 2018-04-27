from importlib import import_module
import os
from flask import Flask, render_template, Response, make_response, url_for, redirect
import gpioController as g

# import camera driver
'''if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_pi import Camera
'''
app = Flask(__name__,template_folder='Templates')

@app.route('/')
def index():
    """Raspberry Pi Car Controller. Make sure you've installed RPi_Cam_Web_interface and ppen https://your-pi-address:80 to stream picamera data"""
    return render_template('index.html')

'''
def gen(Camera):
    """Video streaming generator function."""
    while True:
        frame = Camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    '''
@app.route('/<changepin>', methods=['POST'])
def reroute(changepin):
    changePin = int(changepin)
    
    if changePin == 1:
        g.leftGPIO()
    elif changePin == 2:
        g.forwardGPIO()
    elif changePin == 3:
        g.rightGPIO()
    elif changePin == 4:
        g.reverseGPIO()
    else:
        g.stopGPIO()
        g.clean()
    response = make_response(redirect(url_for('index')))
    return(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
