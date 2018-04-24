import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
pwm1 = GPIO.PWM(13,100)
pwm2 = GPIO.PWM(15,100)

def forwardGPIO():
    pwm1.start(0)
    pwm1.ChangeDutyCycle(100)
    pwm2.start(0)
    pwm2.ChangeDutyCycle(100)
    GPIO.output(3,True)
    GPIO.output(5,False)
    GPIO.output(7,True)
    GPIO.output(11,False)
    sleep(0.8)
    pwm1.stop()
    pwm2.stop()

def reverseGPIO(t):
    pwm1.start(0)
    pwm1.ChangeDutyCycle(100)
    pwm2.start(0)
    pwm2.ChangeDutyCycle(100)
    GPIO.output(3,False)
    GPIO.output(5,True)
    GPIO.output(7,False)
    GPIO.output(11,True)
    sleep(t)
    pwm1.stop()
    pwm2.stop()

def rightGPIO():
    pwm1.start(0)
    pwm2.start(0)
    pwm1.ChangeDutyCycle(80)
    pwm2.ChangeDutyCycle(80)
    GPIO.output(3,True)
    GPIO.output(5,False)
    GPIO.output(7,False)
    GPIO.output(11,True)
    sleep(0.8)
    pwm1.stop()
    pwm2.stop()

def leftGPIO():
    pwm2.start(0)
    pwm1.start(0)
    pwm2.ChangeDutyCycle(80)
    pwm1.ChangeDutyCycle(80)
    GPIO.output(7,True)
    GPIO.output(11,False)
    GPIO.output(3,False)
    GPIO.output(5,True)
    sleep(0.8)
    pwm2.stop()
    pwm1.stop()

def stopGPIO():
    pwm1.stop()
    pwm2.stop()

def clean():
    GPIO.cleanup()
