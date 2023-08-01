import os
from pathlib import Path

from keras import layers
from keras.models import Sequential
from keras.optimizers import RMSprop
from keras.saving.saving_api import load_model
from keras.utils import timeseries_dataset_from_array
import numpy as np

from util import featurewise_normalization, get_history, show_history_charts

climate_dir = r"B:\_Documents\Livres\Deep_Learning_with_Python_-_Francois_Chollet\datasets\jena_climate"
fname = os.path.join(climate_dir, 'jena_climate_2009_2016.csv')
f = open(fname)
data = f.read()
f.close()
lines = data.split('\n')
header = lines[0].split(',')
lines = lines[1:]
print(header)
print(len(lines))

temperature_recorded = np.zeros((len(lines),))
data_recorded = np.zeros((len(lines), len(header) - 1))
for i, line in enumerate(lines):
    values = [float(x) for x in line.split(',')[1:]]
    temperature_recorded[i] = values[1]
    data_recorded[i, :] = values

data_recorded, mean, std = featurewise_normalization(data_recorded)

# plt.plot(range(1440), temperature_recorded[:1440])
# plt.plot(range(len(temperature_recorded)), temperature_recorded)
# plt.show()

# lookback = 1440 * 2

# def evaluate_naive_method():
#     batch_maes = []
#     for step in range(val_steps):
#         samples, targets = next(val_gen)
#         preds = samples[:, -1, 1]
#         mae = np.mean(np.abs(preds - targets))
#         batch_maes.append(mae)
#     print(np.mean(batch_maes))
#     celsius_mae = interpretable_featurewise_normalization(np.mean(batch_maes), std[1])
#     print(celsius_mae)

# evaluate_naive_method()

num_train_samples = int(0.5 * len(data_recorded))
num_val_samples = int(0.25 * len(data_recorded))
num_test_samples = len(data_recorded) - num_train_samples - num_val_samples
sequence_length = 120
sampling_rate = 6
delay = 144
batch_size = 128
train_dataset = timeseries_dataset_from_array(data_recorded[:-delay], targets=temperature_recorded[delay:],
                                              sampling_rate=sampling_rate, sequence_length=sequence_length, shuffle=True,
                                              batch_size=batch_size, start_index=0, end_index=num_train_samples)
val_dataset = timeseries_dataset_from_array(data_recorded[:-delay], targets=temperature_recorded[delay:],
                                            sampling_rate=sampling_rate, sequence_length=sequence_length, shuffle=True,
                                            batch_size=batch_size, start_index=num_train_samples,
                                            end_index=num_train_samples + num_val_samples)
test_dataset = timeseries_dataset_from_array(data_recorded[:-delay], targets=temperature_recorded[delay:],
                                             sampling_rate=sampling_rate, sequence_length=sequence_length, shuffle=True,
                                             batch_size=batch_size, start_index=num_train_samples + num_val_samples)


model = Sequential()
# model.add(layers.Conv1D(32, 5, activation='relu', input_shape=(None, data_recorded.shape[-1])))
# model.add(layers.MaxPooling1D(3))
# model.add(layers.Conv1D(32, 5, activation='relu'))
model.add(layers.GRU(32, dropout=0.1, recurrent_dropout=0.5, return_sequences=True, input_shape=(None, data_recorded.shape[-1])))
model.add(layers.GRU(64, activation='relu', dropout=0.1, recurrent_dropout=0.5))
model.add(layers.Dense(1))
model.compile(optimizer=RMSprop(), loss='mse', metrics=['mae'])
history = model.fit(train_dataset, epochs=40, validation_data=val_dataset)
# history = get_history(Path(r"B:\_Documents\Livres\Deep_Learning_with_Python_-_Francois_Chollet\last_show_history.plk"))
show_history_charts(history)
