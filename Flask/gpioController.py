import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(03, GPIO.OUT) 
GPIO.setup(05, GPIO.OUT)     
GPIO.setup(07, GPIO.OUT) 
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
    GPIO.output(03,True)
    GPIO.output(05,False)
    GPIO.output(07,True)
    GPIO.output(11,False)
    sleep(0.8)
    pwm1.stop()
    pwm2.stop()
    
def reverseGPIO():
    pwm1.start(0)
    pwm1.ChangeDutyCycle(100)
    pwm2.start(0)
    pwm2.ChangeDutyCycle(100)
    GPIO.output(03,False)
    GPIO.output(05,True)
    GPIO.output(07,False)
    GPIO.output(11,True)
    sleep(0.8)
    pwm1.stop()
    pwm2.stop()
    
def rightGPIO():
    pwm1.start(0)
    pwm1.ChangeDutyCycle(60)
    GPIO.output(03,False)
    GPIO.output(05,True)
    sleep(0.8)
    pwm1.stop()
    
def leftGPIO():
    pwm2.start(0)
    pwm2.ChangeDutyCycle(60)
    GPIO.output(07,True)
    GPIO.output(11,False)
    sleep(0.8)
    pwm2.stop()
    
def stopGPIO():
    pwm1.stop()
    pwm2.stop()
    
def clean():
    GPIO.cleanup()


