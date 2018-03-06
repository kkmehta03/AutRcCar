"""Image helpers"""
import time
import cv2

def save_image_with_direction(stream, direction):
    """Save image"""
    stream.seek(0)
    image = cv2.imread(stream)
    image.cv2.imwrite('image%s.jpg' % ("-" + direction + "-"+ str(time.time())), format="JPEG")
