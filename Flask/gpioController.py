import RPi.GPIO as GPIO
def ControllerInit():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(03, GPIO.OUT) #back motor pin
    GPIO.setup(05, GPIO.OUT) #back motor pin
    GPIO.setup(07, GPIO.OUT) #left pin
    GPIO.setup(11, GPIO.OUT) #right pin

def forwardGPIO():
    ControllerInit()
    GPIO.output(03,True)
    GPIO.output(05,False)
    
def reverseGPIO():
    ControllerInit()
    GPIO.output(03,False)
    GPIO.output(05,True)
    
def rightGPIO():
    ControllerInit()
    GPIO.output(07,False)
    GPIO.output(11,True)
    
def leftGPIO():
    ControllerInit()
    GPIO.output(07,True)
    GPIO.output(11,False)
def stopGPIO():
    GPIO.output(03,False)
    GPIO.output(05,False)
    GPIO.output(07,False)
    GPIO.output(11,False)
    
def clean():
    GPIO.cleanup()
clean()

