import RPi.GPIO as GPIO
import io
import socket
import struct
import time
import picamera

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.2', 8000))
connection = client_socket.makefile('wb')

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
try:
with picamera.PiCamera() as camera:
camera.resolution = (320, 240)
camera.framerate = 10
time.sleep(2)
start = time.time()
stream = io.BytesIO()

    for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        stream.seek(0)
        connection.write(stream.read())
        if time.time() - start > 600:
            break
        stream.seek(0)
        stream.truncate()
connection.write(struct.pack('<L', 0))
a = client_socket.recv(1024)
if a == 'w':
    forwardGPIO()
elif a == 'a':
    leftGPIO()
elif a == 's':
    reverseGPIO()
elif a == 'd':
    rightGPIO()
else:
    pass

finally:
connection.close()
client_socket.close()
