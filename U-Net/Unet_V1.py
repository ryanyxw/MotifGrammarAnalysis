
#dabnut
from stringprep import c7_set
import tensorflow as tf

import numpy as np
 
IMG_WIDTH = 128
IMG_HEIGHT = 1
IMG_CHANNELS = 4


model_path = "Model/motif-finder"


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
model.summary()



#################################
#loads the data

xTrain = np.load('NumpyArr/xTrain.npy')
yTrain = np.load('NumpyArr/yTrain.npy')

print(xTrain.shape)
print(yTrain.shape)

#################################
#Model checkpoint
#verbose = 1 means that we want to print the status of the model on the screen


checkpointer = tf.keras.callbacks.ModelCheckpoint(model_path, verbose = 1, save_best_only = True)

callbacks = [
    tf.keras.callbacks.EarlyStopping(patience = 2, monitor = 'val_loss'),
    tf.keras.callbacks.TensorBoard(log_dir='logs'), 
    checkpointer
]

results = model.fit(xTrain, yTrain,  validation_split=0.1, batch_size=50, epochs=1, callbacks=callbacks)

