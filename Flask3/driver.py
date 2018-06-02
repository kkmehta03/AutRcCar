import gpioController as g
import us1
import time

class Drivers():
    def steer(prediction):
      dist = us1.distance()
      print(dist)
      if prediction == 1 and dist > 40:
        print('forward')
        g.forwardGPIO()
      elif dist < 40 and prediction == 1:
        print('too close! waiting for 2 seconds')
        g.stopGPIO()
        time.sleep(2)
        g.reverseGPIO(0.8)
        time.sleep(0.1)

      elif prediction == 0 and dist > 40 :
        print('left')
        g.leftGPIO()
      elif dist < 40 and prediction == 0:
        print('Too close! waiting for 2 seconds')
        g.stopGPIO()
        time.sleep(2)
        g.reverseGPIO(0.8)

      elif prediction == 2 and dist > 40:
        print('right')
        g.rightGPIO()
      elif dist < 40 and prediction == 2:
        print('Too close! waiting for 2 seconds')
        g.stopGPIO()
        time.sleep(2)
        g.reverseGPIO(0.8)
        
      else:
        print('Take care of me please :)')
        g.stopGPIO()
