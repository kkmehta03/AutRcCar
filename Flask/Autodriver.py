import time
import picamera
import numpy as np
import cv2
import gpioController as g

model = cv2.ANN_MLP()
g.stopGPIO()
layer_size = np.int32([38400,4,2,8,8,4])
model.create(layer_size)
model.load('mlp_xml/mlp.xml')

def predict(samples):
  ret, resp = model.predict(samples)
  return resp.argmax(-1)

def steer(prediction):
  if prediction == 2:
    g.forwardGPIO()
  elif prediction == 0:
    g.leftGPIO()
  elif prediction == 1:
    g.rightGPIO()
  else:
    g.stopGPIO()
  

with picamera.PiCamera() as camera:
  camera.resolution = (320, 240)
  camera.framerate = 24
  time.sleep(2)
  image = np.empty((240 * 320 * 3,), dtype=np.uint8)
  camera.capture(image, 'gray')
  image = image.reshape((240, 320, 3))
  stream = io.BytesIO()
  for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
    stream.seek(0)
    cv2.imshow('image',image)
    image_array = half_grey.reshape(1,38400).astype(np.float32)
    prediction = model.predict(image_array)
    steer(prediction)  
