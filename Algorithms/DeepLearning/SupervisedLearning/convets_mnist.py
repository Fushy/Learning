from keras.layers import Dropout

import util
from Colors import printc
from keras import layers, models
from keras.datasets import mnist
from keras.utils import to_categorical
from numpy import float32

training_set, test_set = mnist.load_data()
x_train_images, y_train_labels = training_set
x_test_images, y_test_labels = test_set
x_train_4d_tensor = x_train_images.reshape((60000, 28, 28, 1)).astype(float32) / 255  # (batch, width, height, channels)
x_test_4d_tensor = x_test_images.reshape((10000, 28, 28, 1)).astype(float32) / 255  # 1 channel because gray image input
y_train_labels_matrix = to_categorical(y_train_labels)
y_test_labels_matrix = to_categorical(y_test_labels)
print("x_train_images shape", x_train_images.shape, "y_train_labels shape", y_train_labels.shape)
print("x_train_images_2d shape", x_train_4d_tensor.shape, "y_train_labels_matrix shape", y_train_labels_matrix.shape)

from keras.optimizers import RMSprop

model = models.Sequential()

# Convolutional layers
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))  # increase the number of filters
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))  # increase the number of filters
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))  # increase the number of filters

# Flattening and Fully connected layers
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))  # increase the number of units
model.add(layers.Dense(10, activation='softmax'))

# Changing learning rate with a learning rate schedule
optimizer = RMSprop(learning_rate=0.001)  # You can tune this value as required

model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

history = model.fit(x_train_4d_tensor, y_train_labels_matrix, epochs=10, batch_size=64)
printc("Result on test set\nAccuracy: {1:.4f}\tLoss: {0:.4f}\n".format(*model.evaluate(x_test_4d_tensor, y_test_labels_matrix)))
util.show_history_charts(history)
