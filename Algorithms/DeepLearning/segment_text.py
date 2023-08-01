from keras.layers import Dropout, Embedding, Flatten, Dense
from keras.utils import pad_sequences

from Introspection import get_current_file_name, get_current_file_path, get_current_path, get_project_path
from Paths import join
import util

# samples = ['The cat sat on the mat.', 'The dog ate my homework.']
# tokenizer = Tokenizer(num_words=1000)
# tokenizer.fit_on_texts(samples)
# sequences = tokenizer.texts_to_sequences(samples)
# one_hot_results = tokenizer.texts_to_matrix(samples, mode='binary')
# word_index = tokenizer.word_index
# print('Found %s unique tokens.' % len(word_index))

# samples = ['The cat sat on the mat.', 'The dog ate my homework.']
# dimensionality = 20
# max_length = 10
# results = np.zeros((len(samples), max_length, dimensionality))
# for i, sample in enumerate(samples):
#     for j, word in list(enumerate(sample.split()))[:max_length]:
#         index = abs(hash(word)) % dimensionality
#         results[i, j, index] = 1.
# results[0]

import os

from keras import Sequential
from keras.datasets import imdb
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
import numpy as np


def imdb_data_to_ml_sets(maxlen=100, training_samples=20000, validation_samples=10000, max_words=10000):
    imdb_dir = r"B:\_Documents\Livres\Deep_Learning_with_Python_-_Francois_Chollet\datasets\aclImdb"
    train_dir = os.path.join(imdb_dir, "train")
    labels = []
    texts = []
    for label_type in ["neg", "pos"]:
        dir_name = os.path.join(train_dir, label_type)
        for fname in os.listdir(dir_name):
            if fname[-4:] == ".txt":
                with open(os.path.join(dir_name, fname), encoding="utf-8") as f:
                    texts.append(f.read())
                if label_type == "neg":
                    labels.append(0)
                else:
                    labels.append(1)

    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    word_index = {k: v for (k, v) in tokenizer.word_index.items() if v < max_words}
    # word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))
    data = pad_sequences(sequences, maxlen=maxlen)
    labels = np.asarray(labels)
    print('Shape of data tensor:', data.shape)
    print('Shape of label tensor:', labels.shape)
    indices = np.arange(data.shape[0])
    np.random.shuffle(indices)
    data = data[indices]
    labels = labels[indices]
    x_train, y_train = data[:training_samples], labels[:training_samples]
    x_val = data[training_samples: training_samples + validation_samples]
    y_val = labels[training_samples: training_samples + validation_samples]
    return x_train, y_train, x_val, y_val, word_index


def word_to_embedding_matrix(word_index):
    glove_dir = r"B:\_Documents\Livres\Deep_Learning_with_Python_-_Francois_Chollet\datasets\glove.6B"
    embeddings_index = {}
    with open(os.path.join(glove_dir, 'glove.6B.100d.txt'), encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
    print('Found %s word vectors.' % len(embeddings_index))
    embedding_dim = 100
    max_words = len(word_index) + 1
    embedding_matrix = np.zeros((max_words, embedding_dim))
    for word, i in word_index.items():
        if word in embeddings_index:
            embedding_vector = embeddings_index[word]
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector
    return embedding_matrix

max_features = 10000  # max words taken into account
maxlen = 100  # Cuts off reviews after 100 words
# (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)
# x_train = pad_sequences(x_train, maxlen=maxlen)
# x_test = pad_sequences(x_test, maxlen=maxlen)

x_train, y_train, x_val, y_val, word_index = imdb_data_to_ml_sets(maxlen=maxlen, max_words=max_features,
                                                                  training_samples=200, validation_samples=10000)
embedding_matrix = word_to_embedding_matrix(word_index)

model = Sequential()
model.add(Embedding(max_features, 100, input_length=maxlen))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))
model.layers[0].set_weights([embedding_matrix])
model.layers[0].trainable = False

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
model.summary()
# history = model.fit(x_train, y_train, epochs=20, batch_size=32, validation_split=0.2)
history = model.fit(x_train, y_train, epochs=20, batch_size=32, validation_data=(x_val, y_val))


util.save_history(history, join(get_current_path(), get_current_file_name() + ".plk"))
model.save(join(get_current_path(), get_current_file_name() + ".h5"))

util.show_history_charts(history.history)
