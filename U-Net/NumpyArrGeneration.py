#This file reads the output from TrainingDataPrep.py (the two txt files) and generates numpy arrays for training

from stringprep import c7_set
import numpy as np
 
from tqdm import tqdm 


IMG_WIDTH = 128
IMG_HEIGHT = 1
IMG_CHANNELS = 4


PWMFile = open("PWMOut.txt", 'r')
labelFile = open("labelOut.txt", 'r')

#How many training data
numTrain = eval(PWMFile.readline().strip())

#Prepares the xTrain and yTrain inputs
xTrain = np.zeros((numTrain, IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS), dtype = np.float64)
yTrain = np.zeros((numTrain, IMG_WIDTH, IMG_HEIGHT, 1), dtype = np.bool)

for i in tqdm(range(0, numTrain), desc = "Preparing Training Data"):
    xArr = []
    yArr = []
    isError = False
    for c in range(IMG_WIDTH):
        if (isError):
            break
        pwmInput = PWMFile.readline()
        labelInput = (labelFile.readline().strip()) == "1"
        try:
            xArr += [list(map(lambda x: eval(x), pwmInput.strip().split(" ")))]
            
            yArr += [labelInput]
        except:
            print("pwmInput = " + str(pwmInput))
            print("labelInput = " + str(labelInput))
            print("xArr = " + str(xArr))
            print("yArr = " + str(yArr))
            print(xTrain[i - 1])
            isError = True
    #print(xArr)
    #print(yArr)
    PWMFile.readline()
    labelFile.readline()
    #print(np.array(yArr)[:, np.newaxis, np.newaxis].shape)
    xTrain[i] = (np.array(xArr))[:, np.newaxis, :]
    yTrain[i] = (np.array(yArr))[:, np.newaxis, np.newaxis]
    #print(xTrain[i])
    #print(yTrain[i])    

#print(xTrain)
np.save('NumpyArr/xTrain.npy', xTrain)
np.save("NumpyArr/yTrain.npy", yTrain)
#print(xTrain[79])
