from keras import Sequential
from keras.optimizers import RMSprop
import numpy as np

from keras.datasets import imdb
from keras.utils import pad_sequences
from keras.layers import Bidirectional, Dense, Embedding, GRU, LSTM, SimpleRNN
from keras import layers

import util


def basic_rnn_demo():
    timesteps = 100  # Number of timesteps in the input sequence
    input_features = 32  # Dimensionality of the input feature space
    output_features = 64  # Dimensionality of the output feature space
    inputs = np.random.random((timesteps, input_features))  # Input data: random noise for the sake of the example
    state_t = np.zeros((output_features,))  # Initial state: an all-zero vector
    W = np.random.random((output_features, input_features))  # Random weight matrices
    U = np.random.random((output_features, output_features))  # Random weight matrices
    b = np.random.random((output_features,))  # Random weight matrices
    successive_outputs = []
    for input_t in inputs:
        output_t = np.tanh(np.dot(W, input_t) + np.dot(U, state_t) + b)
        successive_outputs.append(output_t)
        state_t = output_t
        print(output_t[:5])
    final_output_sequence = np.concatenate(successive_outputs, axis=0)
    print(final_output_sequence)


basic_rnn_demo()


def chose_rnn_layer(n):
    match n:
        case 1:
            return SimpleRNN(32)  # 82% 26s/epoch
        case 2:
            return LSTM(32)  # 88% 52s/epoch
        case 3:
            return GRU(32)  # 83% 46s/epoch
        case 4:
            return Bidirectional(SimpleRNN(32))  # 82% 36s/epoch
        case 5:
            return Bidirectional(LSTM(32))  # 88% 161s/epoch
        case 6:
            return Bidirectional(GRU(32))  # 86% 67/epoch
        case 7:  # 87% 14/epoch
            m = Sequential()
            m.add(layers.Conv1D(32, 7, activation='relu'))
            m.add(layers.MaxPooling1D(5))
            m.add(layers.Conv1D(32, 7, activation='relu'))
            m.add(layers.GlobalMaxPooling1D())
            return m


max_features = 10000
maxlen = 500
(input_train, y_train), (input_test, y_test) = imdb.load_data(num_words=max_features)
input_train = pad_sequences(input_train, maxlen=maxlen)
input_test = pad_sequences(input_test, maxlen=maxlen)
print('input_train shape:', input_train.shape)
print('input_test shape:', input_test.shape)

model = Sequential()
model.add(Embedding(max_features, 128))
model.add(chose_rnn_layer(7))
model.add(Dense(1, activation='sigmoid'))
model.summary()
model.compile(optimizer=RMSprop(), loss='mae')
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
history = model.fit(input_train, y_train, epochs=20, batch_size=128, validation_split=0.2)
print("Accuracy: {1:.4f}\tLoss: {0:.4f}".format(*model.evaluate(input_test, y_test)))
util.show_history_charts(history.history)
