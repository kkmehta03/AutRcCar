import socket
import RPi.GPIO as GPIO
import sys
import picamera
import time
import io
import struct

class SendTrainingData(object):
    def __init__(self):
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cs.connect(('192.168.1.3',8000))
        self.connection = self.cs.makefile('wb')
        self.con = self.cs.makefile('rb')
        self.controllerInit()
        self.send_image()
        self.receive_command()
        
    def ControllerInit(self):
        self.GPIO.setmode(GPIO.BOARD)
        self.GPIO.setup(03, GPIO.OUT) #back motor pin
        self.GPIO.setup(05, GPIO.OUT) #back motor pin
        self.GPIO.setup(07, GPIO.OUT) #left pin
        self.GPIO.setup(11, GPIO.OUT) #right pin
    def send_image(self):
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
    def receive_command(self):
        try:
            for c in con:
                direction = self.c.read(1024).decode()
                if direction == 'w':
                    self.forwardGPIO()
                elif direction == 'a':
                    self.leftGPIO()
                elif direction == 's':
                    self.reverseGPIO()
                elif direction == 'd':
                    self.rightGPIO()
                elif direction == 'q':
                    break
                else:
                    pass
    def forwardGPIO(self):
        self.GPIO.output(03,True)
        self.GPIO.output(05,False)
        self.clean()
    def reverseGPIO(self):
        self.GPIO.output(03,False)
        self.GPIO.output(05,True)
        self.clean()
    def rightGPIO(self):
        self.GPIO.output(07,False)
        self.GPIO.output(11,True)
        self.clean()
    def leftGPIO(self):
        self.GPIO.output(07,True)
        self.GPIO.output(11,False)
        self.clean()
    def clean(self):
        self.GPIO.cleanup()
    finally:
        self.connection.close()
        self.con.close()
        self.cs.close()
if __name__ == '__main__':
    sendTrainingData()
