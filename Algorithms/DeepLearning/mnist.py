from functools import reduce
from operator import mul

from keras import layers, models
from keras.datasets import mnist
from keras.utils import to_categorical
from numpy import float32, ndarray, uint8

import util

x_train_images: ndarray[uint8, list[list[list[int]]]]
x_train_2d_tensor: ndarray[float32, list[list[float]]]
x_test_images: ndarray[uint8, list[list[list[int]]]]
x_test_2d_tensor: ndarray[float32, list[list[float]]]
y_train_labels: ndarray[uint8, int]
y_test_labels: ndarray[uint8, int]
y_train_labels_matrix: ndarray[float32, list[list[float]]]
y_test_labels_matrix: ndarray[float32, list[list[float]]]

training_set, test_set = mnist.load_data()
x_train_images, y_train_labels = training_set
x_test_images, y_test_labels = test_set
flatten_shape = reduce(mul, x_train_images.shape[1:], 1)    # 28 * 28 * 1
x_train_2d_tensor = x_train_images.reshape((len(x_train_images), flatten_shape)).astype(float32) / 255
x_test_2d_tensor = x_test_images.reshape((len(x_test_images), flatten_shape)).astype(float32) / 255
y_train_labels_matrix = to_categorical(y_train_labels)
y_test_labels_matrix = to_categorical(y_test_labels)
print("x_train_images shape", x_train_images.shape, "y_train_labels shape", y_train_labels.shape)
print("x_train_images_2d shape", x_train_2d_tensor.shape, "y_train_labels_matrix shape", y_train_labels_matrix.shape)

model = models.Sequential()
model.add(layers.Dense(512, activation='relu', input_shape=(flatten_shape,)))
model.add(layers.Dense(10, activation='softmax'))
model.summary()
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(x=x_train_2d_tensor, y=y_train_labels_matrix, epochs=10, batch_size=128, validation_split=0.2)
print(history.history)
print(model.predict(x_test_2d_tensor))
print("Accuracy: {1:.4f}\tLoss: {0:.4f}".format(*model.evaluate(x=x_test_2d_tensor, y=y_test_labels_matrix)))
util.show_history_charts(history)
