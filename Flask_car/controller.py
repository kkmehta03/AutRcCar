from flask import Flask
from car import *
import Rpi.GPIO as GPIO

app = Flask(__name__)
stream_client()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(03,GPIO.OUT) #back motor pin
GPIO.setup(05,GPIO.OUT) #back motor pin
GPIO.setup(07,GPIO.OUT) #left pin
GPIO.setup(11,GPIO.OUT) #right pin
@app.route('/forward')
def fwd():
    GPIO.output(03,True)
    GPIO.output(05,False)
    return "Forward"

@app.route('/left')
def left_turn():
    left()
    return "Turn Left"

@app.route('/right')
def right_turn():
    right()
    return "Turn Right"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
