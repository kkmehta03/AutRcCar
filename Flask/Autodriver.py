import time
import picamera
import numpy as np
import cv2
import gpioController as g
import io

model = cv2.ANN_MLP()
g.stopGPIO()
layer_size = np.int32([38400,4,2,8,8,4])
model.create(layer_size)
model.load('autrccar/Flask/mlp_xml/mlp.xml')

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
    
with picamera.PiCamera() as cam:
  cam.resolution = (320,240)
  cam.framerate = 10
  cam.start_preview()
  time.sleep(2)
  stream = io.BytesIO()
  for foo in cam.capture_continuous(stream,'jpeg',use_video_port=True):
      jpg=np.empty((240*320*3),dtype=np.uint8)
      print(type(jpg))
      cam.capture(jpg,'bgr')
      image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
      roi = image[120:240,:]
      cv2.imshow('image',image)
      image_array = roi.reshape(1,38400).astype(np.float32)
      prediction = model.predict(image_array)
      steer(prediction)
      
      
      
    
