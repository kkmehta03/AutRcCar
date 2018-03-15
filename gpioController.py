import socket
import RPi.GPIO as GPIO
import sys
import picamera
import time
import io

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(('192.168.1.3',8000))
connection = cs.makefile('wb')

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(03, GPIO.OUT) #back motor pin
    GPIO.setup(05, GPIO.OUT) #back motor pin
    GPIO.setup(07, GPIO.OUT) #left pin
    GPIO.setup(11, GPIO.OUT) #right pin
def forwardGPIO():
    GPIO.output(03,True)
    GPIO.output(05,False)
    clean()
def reverseGPIO():
    GPIO.output(03,False)
    GPIO.output(05,True)
    clean()
def rightGPIO():
    GPIO.output(07,False)
    GPIO.output(11,True)
    clean()
def leftGPIO():
    GPIO.output(07,True)
    GPIO.output(11,False)
    clean()
def forwardLeftGPIO():
    forwardGPIO()
    leftGPIO()
    clean()
def forwardRightGPIo():
    forwardGPIO()
    rightGPIO()
    clean()
def reverseLeftGPIO():
    reverseGPIO()
    leftGPIO()
    clean()
def reverseRightGPIO():
    reverseGPIO()
    rightGPIO()
    clean()
def clean():
    GPIO.cleanup()

#def key_in(event):
    init()
    key_press = event.char
    sleep_time = 0.030

    if key_press.lower() == 'w':
        forwardGPIO()
    elif key_press.lower() == 'a':
        leftGPIO()
    elif key_press.lower() == 's':
        reverseGPIO()
    elif key_press.lower() == 'd':
        rightGPIO()
    elif key_press.lower() == 'w' && 'a':
        forwardLeftGPIO()
    elif key_press.lower() == 'w' && 'd':
        forwardRightGPIo()
    elif key_press.lower() == 's' && 'a':
        reverseLeftGPIO()
    elif key_press.lower() == 's' && 'd':
        reverseRightGPIO()
    else:
        clean()
try:
    init()
    with picamera.PiCamera() as cam:
        cam.resolution = (320,240)
        cam.framerate = 10
        time.sleep(2)
        start = time.time()
        stream = io.BytesIO()

        for foo in camera.capture_continuous(stream,'jpeg',use_video_port =True):
            connection.write(struct.pack('<L',stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            if time.time() - start > 600:
                break
            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L',0))
    direction = cs.recv(1024).decode()
    if direction == 'w':
        forwardGPIO()
    elif direction == 'a':
        leftGPIO()
    elif direction == 's':
        reverseGPIO()
    elif direction == 'd':
        rightGPIO()
    else:
        clean()
finally:
    connection.close()
    cs.close()
