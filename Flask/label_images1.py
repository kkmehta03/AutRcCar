import cv2
import numpy as np
import glob
import time

def label():

    k = np.zeros((4,4), 'float')
    for i in range(4):
        k[i,i] = 1

    temp_label = np.zeros((1,4),'float')
    image_array1 = np.zeros((1,115200),'float')
    label_array1 = np.zeros((1,4),'float')
    count = 0
    for img in glob.glob("left/*.png"):
        image = cv2.imread(img,cv2.IMREAD_COLOR)
        #print(image)
        roi = image[120:240, :, :]
        #img1 = Image.fromstring(img,'RGB')
        #plt.imshow(image,interpolation = 'nearest')
        #plt.show()
        #img1.show()
        temp_array1 = roi.reshape(1,115200).astype(np.float32)
        #plt.imshow(temp_array1,interpolation = 'nearest')
        #plt.show()
        image_array1 = np.vstack((image_array1, temp_array1))
        label_array1 = np.vstack((label_array1, k[0]))
        count+=1
    print('left done')
    print(count)

    for img in glob.glob("right/*.png"):
        image = cv2.imread(img,cv2.IMREAD_COLOR)
        #cv2.imshow('img',image)
        roi = image[120:240, :, :]
        temp_array1 = roi.reshape(1,115200).astype(np.float32)
        image_array1 = np.vstack((image_array1, temp_array1))
        label_array1 = np.vstack((label_array1, k[2]))
        count+=1
    print('right done')
    print(count)

    for img in glob.glob("forward/*.png"):
        image = cv2.imread(img,cv2.IMREAD_COLOR)
        #cv2.imshow('img',image)
        roi = image[120:240, :, :]
        temp_array1 = roi.reshape(1,115200).astype(np.float32)
        image_array1 = np.vstack((image_array1, temp_array1))
        label_array1 = np.vstack((label_array1, k[1]))
        count+=1
    print('forward done')
    print(count)

    for img in glob.glob("reverse/*.png"):
        if not img:
            break
        else:
            image = cv2.imread(img,cv2.IMREAD_COLOR)
            #cv2.imshow('img',image)
            roi = image[120:240, :, :]
            temp_array1 = roi.reshape(1,115200).astype(np.float32)
            image_array1 = np.vstack((image_array1, temp_array1))
            label_array1 = np.vstack((label_array1, k[3]))
            count+=1
    print('reverse done')
    print(count)

    train = image_array1[1:, :]
    train_labels = label_array1[1:, :]
    # save training data as a numpy file
    npzNames = 'training_data_temp/test'+time.strftime("%Y%m%d-%H%M%S")+'.npz'
    np.savez(npzNames,train=train, train_labels=train_labels)
    print('npz file saved!')
    return npzNames, count
