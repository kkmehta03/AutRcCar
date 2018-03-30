from flask import Flask
from time import sleep
import Rpi.GPIO as GPIO
import server_code

app = Flask(__name__)

server_code.stream_client()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(03,GPIO.OUT)
GPIO.setup(05,GPIO.OUT)
GPIO.setup(07,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

pwm1 = GPIO.PWM(13,100)
pwm2 = GPIO.PWM(15,100)
@app.route('/forward')
def fwd():
    pwm1.start(0)
    pwm2.start(0)
    GPIO.output(03,True)
    GPIO.output(05,False)
    GPIO.output(07,True)
    GPIO.output(11,False)
    sleep(0.8)
    pwm1.stop()
    pwm2.stop()
    return "Forward"

@app.route('/left')
def left_turn():
    pwm2.start(0)
    pwm2.ChangeDutyCycle(60)
    GPIO.output(07,True)
    GPIO.output(11,False)
    sleep(0.8)
    pwm2.stop()
    return "Turn Left"

@app.route('/right')
def right_turn():
    pwm1.start(0)
    pwm1.ChangeDutyCycle(60)
    GPIO.output(03,True)
    GPIO.output(05,False)
    sleep(0.8)
    pwm1.stop()
    return "Turn Right"
@app.route('/reverse')
def rvs():
    pwm1.start(0)
    pwm2.start(0)
    GPIO.output(03,False)
    GPIO.output(05,True)
    GPIO.output(07,False)
    GPIO.output(11,True)
    sleep(0.8)
    pwm1.stop()
    pwm2.stop()
@app.route('/stop')
def stp():
    pwm1.stop()
    pwm2.stop()
@app.route('/clean')
def cl():
    GPIO.cleanup()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
