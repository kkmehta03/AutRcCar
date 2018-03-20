import socket
import sys
import picamera
import time
import io
import struct
import gpioController as g

class SendTrainingData(object):
    def __init__(self):
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cs.connect(('192.168.1.3',8000))
        self.connection = self.cs.makefile('wb')
        self.con = self.cs.makefile('rb')
        g.ControllerInit()
        g.receive_command()
        g.send_image()


    def receive_command():
        direction = self.c.read(1024).decode()
        if direction == 'w':
            g.forwardGPIO()
        elif direction == 'a':
            g.leftGPIO()
        elif direction == 's':
            g.reverseGPIO()
        elif direction == 'd':
            g.rightGPIO()
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
                    receive_command()
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
