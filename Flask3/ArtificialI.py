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
    return resp.argmax(-1)
