import numpy as np
def saveToCsv(filename = ''):
    data = np.load('training_data_temp/'+filename+'.npz')
    for key, value in data.items():
        np.savetxt("CSVFiles/npzToCsv - " + filename + key + ".csv", value)
