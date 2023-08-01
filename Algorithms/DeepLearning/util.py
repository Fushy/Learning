from pathlib import Path
import pickle
import statistics

import numpy as np

from Introspection import frameinfo
from Util import reverse_dict


def timeseries_dataset_from_array_hand(data, lookback, delay, min_index, max_index, shuffle=False, batch_size=128, step=6):
    """
    data: The original array of floating-point data, which you normalized in listing.
    lookback: How many timesteps back the input data should go.
    delay: How many timesteps in the future the target should be.
    min_index and max_index: Indices in the data array that delimit which timesteps to draw from. This is useful for keeping a
    segment of the data for validation and another for testing.
    shuffle: Whether to shuffle the samples or draw them in chronological order.
    batch_size: The number of samples per batch.
    step: The period, in timesteps, at which you sample data. You’ll set it to 6 in order to draw one data point every hour.
    The goal is from samples, expect targets
    """
    # from keras.utils import timeseries_dataset_from_array
    # return timeseries_dataset_from_array(data, lookback, delay, min_index, max_index, shuffle=shuffle, batch_size=batch_size, sampling_rate=step)
    if max_index is None:
        max_index = len(data) - delay - 1
    i = min_index + lookback
    while True:
        if shuffle:
            rows = np.random.randint(min_index + lookback, max_index, size=batch_size)
        else:
            if i + batch_size >= max_index:
                i = min_index + lookback
            rows = np.arange(i, min(i + batch_size, max_index))
            i += len(rows)
        samples = np.zeros((len(rows), lookback // step, data.shape[-1]))
        targets = np.zeros((len(rows),))
        for j, row in enumerate(rows):
            indices = range(rows[j] - lookback, rows[j], step)
            samples[j] = data[indices]
            targets[j] = data[rows[j] + delay][1]
        yield samples, targets


def train_n_save(model, history_path_save, model_path_save, train_data, validation_data, steps_per_epoch=100, epochs=100,
                 validation_steps=50):
    if type(train_data) is tuple:
        train_feature, train_label = train_data
        history = model.fit(train_feature, train_label, steps_per_epoch=steps_per_epoch, epochs=epochs,
                            validation_data=validation_data, validation_steps=validation_steps)
    else:
        history = model.fit(train_data, steps_per_epoch=steps_per_epoch, epochs=epochs, validation_data=validation_data,
                            validation_steps=validation_steps)
    save_history(history, history_path_save)
    model.save(model_path_save)
    return history.history


def save_history(history: dict, path):
    assert path.suffix == ".plk"  # .plk file
    with open(path, 'wb') as file:
        pickle.dump(history, file)


def get_history(path):
    assert path.suffix == ".plk"
    with open(path, 'rb') as file:
        return pickle.load(file)


def list_to_sentence(data, indice, library) -> str:
    num_word = reverse_dict(library.get_word_index())
    return " ".join([num_word[nums] for nums in data[indice]])


def lists2d_to_pad_tensor(data):
    """ pad the sequences with zeros to ensure uniform length """
    max_length = max([len(nums) for nums in data])
    results = np.zeros((len(data), max_length), dtype=int)
    for i, sequence in enumerate(data):
        results[i, :len(sequence)] = sequence
    return results
    # return [nums + [0] * (max_length - len(nums)) for nums in data]


def lists2d_to_onehot_tensor(data, dimension=None):
    """ converting the data into a one-hot encoding representation """
    results = np.zeros((len(data), dimension))
    for i, sequence in enumerate(data):
        results[i, sequence] = 1.
    return results


def show_history_charts(history: dict):
    if type(history) is not dict:
        history = history.history
    save_history(history, Path(frameinfo(2)["pathname"] + "last_show_history.plk"))
    import matplotlib.pyplot as plt
    epochs = range(1, len(history['loss']) + 1)
    print("history keys:", list(history))
    plt.rcParams['figure.figsize'] = (6, 6)
    plt.rcParams["keymap.zoom"].append("a")
    plt.rcParams["keymap.back"].append("²")
    names = [word for word in history if ("_" not in word or ("acc" in word and "val" not in word)) and "loss" not in word]
    names += ["loss"]
    fig, axs = plt.subplots(len(names))
    for i, name in enumerate(names):
        axs[i].set_title(name)
    validation_datas_present = False
    for k, v in history.items():
        i = next(i for (i, name) in enumerate(names) if name in k)
        if "loss" in k:
            if 'val' in k:
                axs[i].plot(epochs, v, color='blue', label='Validation loss')
                last_5_average = statistics.mean(v[int(len(v) * 0.9):])
                axs[i].axhline(y=last_5_average, color="blue", linestyle="-.",
                               label="Average model loss {:.2f}".format(last_5_average))
            else:
                axs[i].plot(epochs, v, color='blue', label='Training loss', linestyle='', marker='o')
        else:
            if 'val' in k:
                validation_datas_present = True
                axs[i].plot(epochs, v, color='green', label="Validation " + names[i])
                last_5_average = statistics.mean(v[int(len(v) * 0.9):])
                axs[i].axhline(y=last_5_average, color="green", linestyle="-.",
                               label="Average model val {:.2f}".format(last_5_average))
            else:
                axs[i].plot(epochs, v, color='green', label='Training ' + names[i], linestyle='', marker='o')
    for i, name in enumerate(names):
        axs[i].legend()
    plt.xlabel('Epochs'), plt.ylabel('Loss'), plt.tight_layout()
    plt.gcf().canvas.manager.set_window_title("Statistics on training{} datas".format(
        "/validation" if validation_datas_present else ""))
    plt.show()
    # while plt.isinteractive():
    #     plt.pause(1)


def featurewise_normalization(data) -> np.array:
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    normalized_data = (data - mean) / std
    return normalized_data, mean, std


def interpretable_featurewise_normalization(normalized_data, std) -> np.array:
    return normalized_data * std


def reverse_featurewise_normalization(normalized_data, mean, std) -> np.array:
    return interpretable_featurewise_normalization(normalized_data, std) + mean
