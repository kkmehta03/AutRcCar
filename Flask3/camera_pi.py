import picamera
class Camera():
    def get_frame():
        with picamera.PiCamera() as cam:
          cam.resolution = (320,240)
          cam.framerate = 10
          start = time.time()
          stream = io.BytesIO()
          for foo in cam.capture_continuous(stream,'jpeg',use_video_port=True):
            stream.seek(0)
            yield stream.read()

            stream.seek(0)
            stream.truncate()
