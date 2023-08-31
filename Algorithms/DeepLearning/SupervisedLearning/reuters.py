from keras import layers, models
from keras.datasets import reuters
from keras.losses import categorical_crossentropy, sparse_categorical_crossentropy
from keras.optimizers import RMSprop
from keras.utils import to_categorical
from numpy import ndarray, uint8
import numpy as np

import util

x_train_data: ndarray[uint8, list[int]]
y_train_labels: ndarray[uint8, int]
x_test_data: ndarray[uint8, list[int]]
y_test_labels: ndarray[uint8, int]

max_words = 10000
training_set, test_set = reuters.load_data(num_words=max_words)
x_train_data, y_train_labels = training_set
x_test_data, y_test_labels = test_set
print("x_train_data shape", x_train_data.shape, "y_train_labels shape", y_train_labels.shape)
print("x_test_data shape", x_test_data.shape, "y_test_labels shape", y_test_labels.shape)
# print(util.list_to_sentence(x_train_data, 1, reuters))
data_to_tensor = util.lists2d_to_onehot_tensor
x_train_tensor = data_to_tensor(x_train_data, max_words)
x_test_tensor = data_to_tensor(x_test_data, max_words)

network = models.Sequential()
network.add(layers.Dense(64, activation='relu', input_shape=(max_words,)))
network.add(layers.Dense(64, activation='relu', input_shape=(max_words,)))
network.add(layers.Dense(46, activation='softmax'))
y_train_labels = to_categorical(y_train_labels)
y_test_labels = to_categorical(y_test_labels)
network.compile(optimizer=RMSprop(lr=0.001), loss=categorical_crossentropy, metrics=['accuracy'])
# network.compile(optimizer=RMSprop(lr=0.001), loss=sparse_categorical_crossentropy, metrics=['accuracy'])

x_train_tensor_1 = x_train_tensor[:1000]
x_train_tensor_2 = x_train_tensor[1000:]
y_train_labels_1 = y_train_labels[:1000]
y_train_labels_2 = y_train_labels[1000:]

history = network.fit(x_train_tensor_2, y_train_labels_2, epochs=20, batch_size=512,
                      validation_data=(x_train_tensor_1, y_train_labels_1))
# history = network.fit(x_train_tensor_1, train_labels_1, epochs=20, batch_size=512, validation_data=(x_train_tensor_2,
# train_labels_2)) print(history.history)
# history = network.fit(x_train_tensor, y_train_labels, epochs=20, batch_size=512)

print("acc: {1:.4f}\tloss: {0:.4f}".format(*network.evaluate(x_test_tensor, y_test_labels)))

predictions = network.predict(x_test_tensor)
# print("For the first sentence, the class with the lowest probability is", np.argmin(predictions[0]))
# print("For the first sentence, the class with the highest probability is", np.argmax(predictions[0]))

util.show_history_charts(history)
