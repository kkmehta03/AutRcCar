__author__ = 'kkm'
''' the car runs at 35.0375 cm/s. Run this file to allow the car to autonomously drive around.'''
import time
import picamera
import numpy as np
import cv2
import gpioController as g
import io
import us1
class neuralnet(object):
  def __init__(self,filepath):
    self.model = cv2.ml.ANN_MLP_load(filepath)
  def predict(self, samples):
    ret, resp = self.model.predict(samples)
    print(ret)
    print(resp)
    print(resp.argmax(-1))
    return resp.argmax(-1)
def steer(prediction):
  dist = us1.distance()
  print(dist)
  if prediction == 1 and dist > 40:
    print('forward')
    g.forwardGPIO()
  elif dist < 40 and prediction == 1:
    print('too close! going away')
    g.reverseGPIO(1.6)
    time.sleep(0.1)
    g.leftGPIO()
  elif prediction == 0 and dist > 40 :
    print('left')
    g.leftGPIO()
  elif dist < 40 and prediction == 0:
    print('nope! going right!')
    g.reverseGPIO(1.6)
    time.sleep(0.1)
    g.rightGPIO()
  elif prediction == 2 and dist > 40:
    print('right')
    g.rightGPIO()
  elif dist < 40 and prediction == 2:
    print('nope! going left')
    g.reverseGPIO(1.6)
    time.slee(0.1)
    g.leftGPIO()
  else:
    print('Take care of me please :)')
    g.stopGPIO()

model = neuralnet('mlp.xml')
with picamera.PiCamera() as cam:
  cam.resolution = (320,240)
  cam.framerate = 10
  start = time.time()
  stream = io.BytesIO()
  for foo in cam.capture_continuous(stream,'jpeg',use_video_port=True):
    stream.seek(0)
    jpg = stream.read()
    color_image = cv2.imdecode(np.fromstring(jpg,dtype=np.uint8),cv2.IMREAD_COLOR)
    roi = color_image[120:240, :]
    image_array = roi.reshape(1,115200).astype(np.float32)
    print(image_array)
    print(image_array.size)
    print(image_array.shape)
    prediction = model.predict(image_array)
    steer(prediction)
    stream.seek(0)
    stream.truncate()
