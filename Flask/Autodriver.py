__author__ = 'kkm'
''' the car runs at 35.0375 cm/s'''
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
  #def create(self):
    #layer_size = np.int32([38400,4,2,8,8,4])
    #self.model.create(layer_size)
    #self.model.load('mlp_xml/mlp.xml')
  def predict(self, samples):
    ret, resp = self.model.predict(samples)
    #print(ret)
    print('Predicting : ',resp.argmax(-1))
    return resp.argmax(-1)

#model = cv2.ANN_MLP()
#layer_size = ([38400,32,4])
#model.create(layer_size)
#model.load('/autrccar/Flask/mlp_xml/mlp.xml')

#def predictor(samples):
  #ret, resp = model.predict(samples)
  #print(ret.argmax(-1))
  #return (ret.argmax(-1))

def steer(prediction):
  dist = us1.distance()
  print(dist)
  
  elif prediction == 1 and dist > 40:
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
    time.sleep(0.1)
    g.leftGPIO()
  
  else:
    print('Take care of me please :)')
    g.stopGPIO()
    
model = neuralnet('mlp1.xml')
with picamera.PiCamera() as cam:
  cam.resolution = (320,240)
  cam.framerate = 10
  start = time.time()
  stream = io.BytesIO()
  for foo in cam.capture_continuous(stream,'jpeg',use_video_port=True):
    stream.seek(0)
    jpg = stream.read()
    image = cv2.imdecode(np.fromstring(jpg,dtype=np.uint8),cv2.IMREAD_COLOR)
    #roi = gray[120:240, :]
    #cv2.imshow('image',roi)
    image_array = image.reshape(1,115200).astype(np.float32)
    print(image_array)
    #print(type(image_array))
    #print(image_array.size)
    #print(image_array.shape)
    #prediction = predictor(image_array)
    prediction = model.predict(image_array)
    steer(prediction)
    stream.seek(0)
    stream.truncate()
