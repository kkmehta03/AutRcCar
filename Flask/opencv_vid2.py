import cv2
import numpy as np

vidcap = cv2.VideoCapture('media/vi_0007_20180425_162905.mp4')
count = 0
success = True
while success:
    vidcap.set(cv2.CAP_PROP_POS_MSEC,(count * 100))
    success,image = vidcap.read()

    ## Stop when last frame is identified
    image_last = cv2.imread("frame{}.png".format(count-1))
    if np.array_equal(image,image_last):
        break
    im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("TrainingData/ right%d.png" % count, im_gray)     # save frame as PNG file
    print('{}.sec reading a new frame: {} '.format(count,success))
    count += 1
