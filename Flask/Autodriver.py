import time
import picamera
import numpy as np
import cv2
import gpioController

model = cv2.ANN_MLP()

layer_size = np.int32([38400,8,4,4,2,4])
model.create(layer_size)
model.load('mlp_xml/mlp.xml')

def predict(samples):
  

with picamera.PiCamera() as camera:
camera.resolution = (320, 240)
    camera.framerate = 24
    time.sleep(2)
    image = np.empty((240 * 320 * 3,), dtype=np.uint8)
    camera.capture(image, 'gray')
    image = image.reshape((240, 320, 3))
    cv2.imshow('image',image)
    
    image_array = half_grey.reshape(1,38400).astype(np.float32)
    
    prediction = model.predict(image_array)
    
