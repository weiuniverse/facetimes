import keras
from read_data import read_data
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

image,label = read_data()
image = np.array(image)
# print(image[0])
# print(image[0].shape)
# model = keras.applications.vgg16.VGG16(include_top=True, weights=None, input_tensor=None, input_shape=(64,64,3), pooling=None, classes=4)
# model.fit(image,label)
input_shape = (64,64,3)
model = Sequential()
model.add(Convolution2D(32, kernel_size=(3, 3), activation='relu',padding="same", input_shape=input_shape))
model.add(Convolution2D(64, (3, 3), activation='relu',padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Convolution2D(128, kernel_size=(3, 3), activation='relu',padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Convolution2D(128, kernel_size=(3, 3), activation='relu',padding="same"))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(4))

# model.summary()

# sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
# model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
adam = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(loss='mean_squared_error', optimizer='adam',epochs=30,batch_size=64)
# model.load_weights('model.h5')
model.fit(image,label)
model.save('model.h5')
