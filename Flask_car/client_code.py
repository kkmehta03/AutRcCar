# import the necessary package
import time
import cv2
import numpy as np
import pygame
from pygame.locals import *
import socket
import urllib.request


class CollectTrainingData(object):
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('192.168.1.3', 8000))
        self.server_socket.listen(0)

        # accept one client's connection
        self.connection = self.server_socket.accept()[0].makefile('rb')
        self.isReceiving = True

        # get connection with the car
        #############################

        # create labels
        self.k = np.zeros((3, 3), 'float')
        for i in range(3):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 3), 'float')

        pygame.init()
        pygame.display.set_mode((320, 240))
        pygame.key.set_repeat(1, 100)
        # pygame.key.set_repeat(1, 40)
        self.collect_imgdata()

    def collect_imgdata(self):
        saved_frame = 0
        total_frame = 0

        print('start collecting images....')
        image_array = np.zeros((1, 50400))
        label_array = np.zeros((1, 3), 'float')

        # get the video stream from our client(Pi)
        try:
            stream_bytes = bytes()

            while self.isReceiving:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    gray_image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                    # only get the lower half image (cut the row num in half)
                    half_gray = gray_image[120:240, :]

                    # save streamed images
                    #cv2.imwrite('training_images/frame{:>05}.jpg'.format(total_frame), gray_image)

                    # show current frame (show video in big picture)
                    cv2.imshow('view', half_gray)

                    # reshape half_gray from into one row numpy array
                    temp_image_array = half_gray.reshape(1, 50400).astype(np.float32)

                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            keypress = event.key
                            if keypress == pygame.K_LEFT:
                                print('left')
                                urllib.request.urlopen('http://192.168.1.4:8000/left').read()
                                image_array = np.vstack((image_array, temp_image_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                # tell car to go left

                            elif keypress == pygame.K_RIGHT:
                                print ('right')
                                urllib.request.urlopen('http://192.168.1.4:8000/right').read()
                                image_array = np.vstack((image_array, temp_image_array))
                                label_array = np.vstack((label_array, self.k[2]))
                                saved_frame += 1
                                # tell car to go right

                            elif keypress == pygame.K_UP:
                                print ('forward')
                                urllib.request.urlopen('http://192.168.1.4:8000/forward').read()
                                image_array = np.vstack((image_array, temp_image_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                # tell car to go forward

                            elif keypress == pygame.K_ESCAPE:
                                print ('exit')
                                self.isReceiving = False

                                # tell the car to stop
                                ######################

                                break

            # delete first row of zeros
            train = image_array[1:, :]
            train_labels = label_array[1:, :]
            print('Training data shape', train.shape)
            print('Training label shape', train_labels.shape)

            # save training data in numpy file
            np.savez('training_data3/test025.npz', train=train, train_labels=train_labels)

            print('Total frame:', total_frame)
            print('Saved frame', saved_frame)
            print('Dropped frame', total_frame - saved_frame)

        finally:
            # self.server_socket.shutdown(socket.SHUT_RDWR)
            self.connection.close()
            self.server_socket.close()
            print('connection closed')

if __name__ == '__main__':
    CollectTrainingData()
