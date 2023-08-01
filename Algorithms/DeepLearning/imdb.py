from keras import layers, models
from keras.datasets import imdb
from keras.losses import binary_crossentropy
from keras.metrics import binary_accuracy
from keras.optimizers import RMSprop
from numpy import float32, ndarray, uint8
import numpy as np
import util

x_train_data: ndarray[uint8, list[int]]
y_train_labels: ndarray[uint8, int]
x_test_data: ndarray[uint8, list[int]]
y_test_labels: ndarray[uint8, int]

max_words = 10000
training_set, test_set = imdb.load_data(num_words=max_words)
x_train_data, y_train_labels = training_set
x_test_data, y_test_labels = test_set
print("x_train_data shape", x_train_data.shape, "y_train_labels shape", y_train_labels.shape)
print("x_test_data shape", x_test_data.shape, "y_test_labels shape", y_test_labels.shape)

# util.list_to_sentence(x_train_data, 1, imdb)
data_to_tensor = util.lists2d_to_onehot_tensor
# data_to_tensor = util.lists2d_to_pad_tensor
x_train_tensor = data_to_tensor(x_train_data, max_words)
x_test_tensor = data_to_tensor(x_test_data, max_words)
y_train_labels = np.asarray(y_train_labels).astype(float32)
y_test_labels = np.asarray(y_test_labels).astype(float32)

x_validation = x_train_tensor[:10000]
x_train = x_train_tensor[10000:]
y_validation = y_train_labels[:10000]
y_train = y_train_labels[10000:]

network = models.Sequential()
network.add(layers.Dense(16, activation='relu', input_shape=(max_words,)))
network.add(layers.Dropout(0.5))
network.add(layers.Dense(16, activation='relu'))
network.add(layers.Dropout(0.5))
network.add(layers.Dense(1, activation='sigmoid'))
network.compile(optimizer=RMSprop(lr=0.001), loss=binary_crossentropy, metrics=[binary_accuracy])
history = network.fit(x_train, y_train, epochs=20, batch_size=512, validation_data=(x_validation, y_validation))
# history = network.fit(x_train_tensor_1, train_labels_1, epochs=20, batch_size=512, validation_data=(x_train_tensor_2,
# train_labels_2)) history = network.fit(x_train_tensor, y_train_labels, epochs=20, batch_size=512)

# print(history.history)
print("acc: {1:.4f}\tloss: {0:.4f}".format(*network.evaluate(x_test_tensor, y_test_labels)))
# print(network.predict(x_test_tensor))
util.show_history_charts(history)
a = 1
