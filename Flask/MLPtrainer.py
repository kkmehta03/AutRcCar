import cv2
import numpy as np
import glob
import datetime

print('Loading training data...')
e0 = cv2.getTickCount()

# load training data
image_array = np.zeros((1, 115200))
label_array = np.zeros((1, 4), 'float')
training_data = glob.glob('training_data_temp/test20180427-150530.npz')

for single_npz in training_data:
    with np.load(single_npz) as data:
        print (data.files)
        train_temp = data['train']
        train_labels_temp = data['train_labels']
        print (train_temp.shape)
        print (train_labels_temp.shape)
    image_array = np.vstack((image_array, train_temp))
    label_array = np.vstack((label_array, train_labels_temp))

train = image_array[1:371, :]
#print(train)
train_labels = label_array[1:371, :]
print(train_labels)
#validate = image_array[121:158,:]
#validate_labels = label_array[121:158, : ]
#print (validate.shape)
print (train_labels.shape)
#print (validate_labels.shape)

e00 = cv2.getTickCount()
time0 = (e00 - e0)/ cv2.getTickFrequency()
print('Loading image duration:', time0)

# set start time
e1 = cv2.getTickCount()

# create MLP
layer_sizes = np.int32([115200, 32,8,8, 4])
model = cv2.ml.ANN_MLP_create()
model.setLayerSizes(layer_sizes)
model.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 2, 1)
model.setBackpropWeightScale(0.001)

print('Training MLP ...')
num_iter = model.train(np.float32(train), cv2.ml.ROW_SAMPLE, np.float32(train_labels))

# set end time
e2 = cv2.getTickCount()
time = (e2 - e1)/cv2.getTickFrequency()
print('Training duration:', time)

# save param
filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
model.save('mlp_xml/mlp'+ filename1 +'.xml')

#print('Ran for %d iterations' % num_iter)

ret, resp = model.predict(train)
prediction = resp.argmax(-1)
print('Prediction:', prediction)
true_labels = train_labels.argmax(-1)
print('True labels:', true_labels)

print('Testing...')
train_rate = np.mean(prediction == true_labels)
print ('Train rate: %f:' % (train_rate*100))
