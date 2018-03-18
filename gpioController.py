import socket
import RPi.GPIO as GPIO
import sys
import picamera
import time
import io
import struct

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(('192.168.1.3',8000))
connection = cs.makefile('wb')
con = cs.makefile('rb')

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
def clean():
    GPIO.cleanup()

try:
    init()
    with picamera.PiCamera() as cam:
        cam.resolution = (320,240)
        cam.framerate = 10
        time.sleep(2)
        start = time.time()
        stream = io.BytesIO()

        for foo in cam.capture_continuous(stream,'jpeg',use_video_port=True):
            connection.write(struct.pack('<L',stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            if time.time() - start > 600:
                break
            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L',0))
    for c in con:
        direction = c.read(1024).decode()
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
