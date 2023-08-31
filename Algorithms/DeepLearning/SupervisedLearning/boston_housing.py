from keras import layers, models
from keras.datasets import boston_housing
from matplotlib import pyplot as plt
from numpy import ndarray, uint8
import numpy as np

import util

train_data: ndarray[uint8, list[int]]
train_labels: ndarray[uint8, int]
test_data: ndarray[uint8, list[int]]
test_labels: ndarray[uint8, int]

training_set, test_set = boston_housing.load_data()
train_data, train_labels = training_set
test_data, test_labels = test_set
print("x_train_data shape", train_data.shape, "y_train_labels shape", train_labels.shape)
print("x_test_data shape", test_data.shape, "y_test_labels shape", test_labels.shape)

print(train_data[0])
util.featurewise_normalization(train_data, test_data)
print(train_data[0])


def build_model():
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu', input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model

k = 4
num_val_samples = len(train_data) // k
num_epochs = 100
all_mae_scores = []
all_mae_histories = []
for i in range(k):
    print('processing fold #k-' + str(i),
          "train([:{0}]+[{1}:]) val([{0}:{1}])".format(i * num_val_samples, (i + 1) * num_val_samples))
    partial_train_data = np.concatenate([train_data[:i * num_val_samples], train_data[(i + 1) * num_val_samples:]], axis=0)
    partial_train_targets = np.concatenate([train_labels[:i * num_val_samples], train_labels[(i + 1) * num_val_samples:]], axis=0)
    val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
    val_targets = train_labels[i * num_val_samples: (i + 1) * num_val_samples]
    model = build_model()
    # history = model.fit(partial_train_data, partial_train_targets, epochs=num_epochs, batch_size=1, verbose=0)
    # val_mse, val_mae = model.evaluate(val_data, val_targets, verbose=0)
    # all_mae_scores.append(val_mae)
    history = model.fit(partial_train_data, partial_train_targets, epochs=num_epochs, batch_size=16, verbose=0,
                        validation_data=(val_data, val_targets))
    all_mae_histories.append(history.history["val_mae"])
network = build_model()
network.fit(train_data, train_labels, epochs=100, batch_size=16)
print("mae: {1:.4f}\tloss: {0:.4f}".format(*network.evaluate(test_data, test_labels)))

# print(all_mae_scores, np.mean(all_scores))
average_mae_history = [np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]
print(average_mae_history)
plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()

