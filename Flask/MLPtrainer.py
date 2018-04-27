import cv2
import numpy as np
import glob
import datetime
import label_images1 as l

print('Loading training data...')
e0 = cv2.getTickCount()

# load training data
fName, cnt = l.label()
image_array = np.zeros((1, 115200))
label_array = np.zeros((1, 4), 'float')
training_data = glob.glob(fName)

for single_npz in training_data:
    with np.load(single_npz) as data:
        print (data.files)
        train_temp = data['train']
        train_labels_temp = data['train_labels']
        print (train_temp.shape)
        print (train_labels_temp.shape)
    image_array = np.vstack((image_array, train_temp))
    label_array = np.vstack((label_array, train_labels_temp))

#Split training data and test/validation data
#Use 80% data to train and 20% to validate the model

def dataSplitter():
    trainCount = round(0.8 * cnt)
    train = image_array[1:trainCount, :]
    train_labels = label_array[1:trainCount, :]
    trainCount+=1
    validate = image_array[trainCount:cnt,:]
    validate_labels = label_array[trainCount:cnt, : ]
    print (train.shape)
    print (validate.shape)
    print (train_labels.shape)
    print (validate_labels.shape)
    return train, validate, train_labels, validate_labels

train, validate, train_labels, validate_labels = dataSplitter()

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

ret, resp = model.predict(validate)
prediction = resp.argmax(-1)
print('Prediction:', prediction)
true_labels = validate_labels.argmax(-1)
print('True labels:', true_labels)

print('Testing...')
train_rate = np.mean(prediction == true_labels)
print ('Train rate: %f:' % (train_rate*100))
