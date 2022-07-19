
#Every run is 3 epochs
from re import L
from stringprep import c7_set
from regex import S
import tensorflow as tf
import numpy as np


IMG_WIDTH = 128
IMG_HEIGHT = 1
IMG_CHANNELS = 4

model_path = "Model/motif-finder"
input_path = "../Tomtom/CompleteProgram/filtered.chen"
labelled_path = "../Tomtom/CompleteProgram/labelled.txt"
output_path = "testingOut.txt"

seed = 42
np.random.seed(seed)

#Building the model

#Defining the input layer
s = tf.keras.layers.Input((IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS))


####################### First set of convolution + max pooling #######################
#We call this convolution layer on "inputs"
c1 = tf.keras.layers.Conv2D(16, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(s)
#Dropout 10% of data points from c1
c1 = tf.keras.layers.Dropout(0.05)(c1)
#We call convolution again
c1 = tf.keras.layers.Conv2D(16, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
#Max Pooling layer
p1 = tf.keras.layers.MaxPooling2D((2, 1))(c1)
####################### First set end #######################

####################### Second set of convolution + max pooling #######################
#We call this convolution layer on "inputs"
c2 = tf.keras.layers.Conv2D(32, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(p1)
#Dropout 10% of data points from c1
c2 = tf.keras.layers.Dropout(0.05)(c2)
#We call convolution again
c2 = tf.keras.layers.Conv2D(32, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
#Max Pooling layer
p2 = tf.keras.layers.MaxPooling2D((2, 1))(c2)
####################### Second set end #######################

####################### Third set of convolution + max pooling #######################
#We call this convolution layer on "inputs"
c3 = tf.keras.layers.Conv2D(64, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(p2)
#Dropout 10% of data points from c1
c3 = tf.keras.layers.Dropout(0.05)(c3)
#We call convolution again
c3 = tf.keras.layers.Conv2D(64, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(c3)
#Max Pooling layer
p3 = tf.keras.layers.MaxPooling2D((2, 1))(c3)
####################### Third set end #######################

####################### Fourth set of convolution + max pooling #######################
#We call this convolution layer on "inputs"
c4 = tf.keras.layers.Conv2D(128, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(p3)
#Dropout 10% of data points from c1
c4 = tf.keras.layers.Dropout(0.05)(c4)
#We call convolution again
c4 = tf.keras.layers.Conv2D(128, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(c4)
#Max Pooling layer
p4 = tf.keras.layers.MaxPooling2D((2, 1))(c4)
####################### Fourth set end #######################
###############################################################################################################################################################################################################


#END OF ENCODER/CONTRACTOR PATH


###############################################################################################################################################################################################################
####################### Valley Set #######################
#We call this convolution layer on "inputs"
c5 = tf.keras.layers.Conv2D(256, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(p4)
#Dropout 10% of data points from c1
c5 = tf.keras.layers.Dropout(0.05)(c5)
#We call convolution again
c5 = tf.keras.layers.Conv2D(256, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(c5)
####################### Valley Set end #######################
###############################################################################################################################################################################################################


#Start of Expansive Set


###############################################################################################################################################################################################################
####################### First Upsample Set #######################
u6 = tf.keras.layers.Conv2DTranspose(128, (2, 1), strides=(2, 1), padding='same')(c5)
u6 = tf.keras.layers.concatenate([u6, c4])
c6 = tf.keras.layers.Conv2D(128, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(u6)
c6 = tf.keras.layers.Dropout(0.1)(c6)
c6 = tf.keras.layers.Conv2D(128, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(c6)
####################### First Upsample Set End#######################

####################### Second Upsample Set #######################
u7 = tf.keras.layers.Conv2DTranspose(64, (2, 1), strides=(2, 1), padding='same')(c6)
u7 = tf.keras.layers.concatenate([u7, c3])
c7 = tf.keras.layers.Conv2D(64, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(u7)
c7 = tf.keras.layers.Dropout(0.1)(c7)
c7 = tf.keras.layers.Conv2D(64, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(c7)
####################### Second Upsample Set End#######################

####################### Third Upsample Set #######################
u8 = tf.keras.layers.Conv2DTranspose(32, (2, 1), strides=(2, 1), padding='same')(c7)
u8 = tf.keras.layers.concatenate([u8, c2])
c8 = tf.keras.layers.Conv2D(32, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(u8)
c8 = tf.keras.layers.Dropout(0.05)(c8)
c8 = tf.keras.layers.Conv2D(32, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(c8)
####################### Third Upsample Set End#######################

####################### Fourth Upsample Set #######################
u9 = tf.keras.layers.Conv2DTranspose(16, (2, 1), strides=(2, 1), padding='same')(c8)
u9 = tf.keras.layers.concatenate([u9, c1], axis = 3)
c9 = tf.keras.layers.Conv2D(16, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(u9)
c9 = tf.keras.layers.Dropout(0.05)(c9)
c9 = tf.keras.layers.Conv2D(16, (3, 1), activation='relu', kernel_initializer='he_normal', padding='same')(c9)
####################### Fourth Upsample Set End#######################

#Get final output of depth of 1
outputs = tf.keras.layers.Conv2D(1, (1, 1), activation='sigmoid')(c9)

#Run the model
model = tf.keras.Model(inputs=[s], outputs=[outputs])
#Choose the optimizer with algorithms used for back propagation
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#Printout summary
# model.summary()


#################################

#Loads the previously trained motif finder
model.load_weights(model_path)


#################################

#Prepares the data extracted from filtered.chen


#Randomly gets probabilities for 4 positions
def getProbabilities():
    x = np.random.rand(4)
    x = x / (sum(x))
    return x

#Converts a single sequence from filtered.chen to a 128 length sequence
#Returns false if the sequence itself is longer than 128 length, true otherwise
def processSingleSequence(inputFile, outputFile, labelledFile, model):

    #Gets rid of the name of the motif
    name = inputFile.readline()
    if (name == "\n" or name == ""):
        return False
    name2 = labelledFile.readline()
    if (name[1:] != name2): #If we realize that the names of the sequences we are comparing are wrong
        print(name)
        print(name2)
        print("ERROR")
        return False
    outputFile.write(name) #Writes the name into the output file
    name = name[1:-1].split("_")
    length = eval(name[-1]) - eval(name[-2]) + 1

    #returns false if our sequence length is longer than IMG_WIDTH
    if (length > IMG_WIDTH):
        return False

    testSeq = []
    outSeq = []#Records what the actual expected results are
    

    #We have IMG_WIDTH - length positions left to fill, so we choose a random number to represent new additions to the beginning and end
    pivotPoint = np.random.randint(0, IMG_WIDTH - length)
    print(pivotPoint)

    #Positions leading up to the testing sequence (padded with random probabilities)
    for i in range(pivotPoint):
        #Adds in a random set of probabiltiies
        testSeq += [getProbabilities()]
        #Writes a 0 to the expected output
        outSeq += ['0']

    outSeq[-1] += '\nStart Now: -----------------'#The actual sequence starts from here

    line = inputFile.readline()
    for i in range(length):
        #Reads in the PWM for the corresponding sequence
        line = list(map(lambda x: eval(x), line.strip().split("\t")))
        totSum = sum(line)
        line = list(map(lambda x: x / totSum, line))
        testSeq += [line]
        line = inputFile.readline()

        #Writes the corresponding expected output into outputFile
        outSeq += [labelledFile.readline().strip()]
    
    labelledFile.readline() #Burn the last empty row

    outSeq[-1] += '\nEnd now: -----------------'#The actual sequence ended the previous line before
    for i in range(IMG_WIDTH - length - pivotPoint):
        testSeq += [getProbabilities()]
        outSeq += ['0']
    
    testSeq = np.array(testSeq)[np.newaxis, :, np.newaxis, :]
    print(testSeq.shape)

    prediction = model.predict(testSeq, verbose = 1)
    prediction = (prediction > 1e-2)[0]#ROC

    for i in range(len(prediction)):
        outputFile.write(str(prediction[i][0][0]) +  '\t' + str(outSeq[i]) + '\n')

    outputFile.write('\n')
    # print(prediction.shape)
    # print(prediction > 1e-4)
    return True



def processFile(model):
    inputFile = open(input_path, 'r')
    outputFile = open(output_path, 'w')
    labelledFile = open(labelled_path, 'r')
    #while(processSingleSequence(inputFile, outputFile, labelledFile, model)):
    #    continue
    processSingleSequence(inputFile, outputFile, labelledFile, model)

processFile(model)

#preds_train = model.predict(X_train[:int(X_train.shape[0]*0.9)], verbose=1)