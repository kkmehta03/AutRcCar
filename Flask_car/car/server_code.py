import io
import socket
import struct
import time
import picamera

def stream_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.3', 8000))
    connection = client_socket.makefile('wb')

    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (420,240)
            camera.framerate = 10
            time.sleep(2)
            start = time.time()
            stream = io.BytesIO()

            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                stream.seek(0)
                connection.write(stream.read())

                if time.time() - start > 90:
                    break
                stream.seek(0)
                stream.truncate()

        connection.write(struct.pack('<L', 0))
    except socket.error, e:
        print e
    finally:
        connection.close()
        client_socket.close()
