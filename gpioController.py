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
        controllerInit()
        send_image()
        receive_command()

    def ControllerInit():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(03, GPIO.OUT) #back motor pin
        GPIO.setup(05, GPIO.OUT) #back motor pin
        GPIO.setup(07, GPIO.OUT) #left pin
        GPIO.setup(11, GPIO.OUT) #right pin

    def forwardGPIO():
        GPIO.output(03,True)
        GPIO.output(05,False)
        self.clean()

    def reverseGPIO():
        GPIO.output(03,False)
        GPIO.output(05,True)
        self.clean()

    def rightGPIO():
        GPIO.output(07,False)
        GPIO.output(11,True)
        self.clean()

    def leftGPIO():
        GPIO.output(07,True)
        GPIO.output(11,False)
        self.clean()

    def clean():
        GPIO.cleanup()

    def receive_command():
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
            exit
        else:
            pass

    def send_image(self):
        try:
            with picamera.PiCamera() as cam:
                cam.resolution = (320,240)
                cam.framerate = 10
                time.sleep(2)
                start = time.time()
                stream = io.BytesIO()

                for foo in cam.capture_continuous(stream,'jpeg',use_video_port=True):
                    self.connection.write(struct.pack('<L',stream.tell()))
                    self.connection.flush()
                    stream.seek(0)
                    self.connection.write(stream.read())
                    if time.time() - start > 600:
                        break
                    stream.seek(0)
                    stream.truncate()
            self.connection.write(struct.pack('<L',0))

        finally:
            self.connection.close()
            self.con.close()
            self.cs.close()
if __name__ == '__main__':
    SendTrainingData()
