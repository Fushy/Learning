# check https://github.com/chouhbik/Kaggle-Dogs-vs-cats/blob/master/Dogs%20vs%20cats.ipynb
import os
import shutil

from keras import backend as K, layers, models
from keras.applications import VGG16
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import array_to_img, img_to_array, load_img
import numpy as np
from Files import get_files_from_path
from Image import display_images
from Introspection import get_current_file_path, get_project_path
from Paths import SEP, join
from rng import rng_int

import util

v_extract_features = {}

# pas de caractere utf-8 utilisant d'accents sous windows, de preference un path de forme A-Z
# Faire attention a ce que toutes les images soient correcte, pas de taille de 0 octet.
file_path = get_current_file_path()
project_path = get_project_path()
dataset_dir = join(project_path, r"datasets" + SEP + "PetImages")
cat_dataset_dir = join(dataset_dir, "Cat")
dog_dataset_dir = join(dataset_dir, "Dog")
base_dir = join(project_path, "cats_and_dogs_data_process")
models_dir = join(base_dir, r"models")
train_dir = join(base_dir, "train")
train_cats_dir = join(train_dir, "cats")
train_dogs_dir = join(train_dir, "dogs")
validation_dir = join(base_dir, "validation")
validation_cats_dir = join(validation_dir, "cats")
validation_dogs_dir = join(validation_dir, "dogs")
test_dir = join(base_dir, "test")
test_cats_dir = join(test_dir, "cats")
test_dogs_dir = join(test_dir, "dogs")

model_path_save = join(models_dir, "model.h5")
history_path_save = join(models_dir, "history.plk")

conv_base = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))


def gen_model():
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dense(1, activation='softmax'))
    return model


def create_dirs():
    dirs = [base_dir, train_dir, validation_dir, test_dir, train_cats_dir, train_dogs_dir, validation_cats_dir,
            validation_dogs_dir, test_cats_dir, test_dogs_dir, models_dir]
    list(map(lambda d: os.makedirs(d, exist_ok=True), dirs))
    for file_name in ["{}.jpg".format(i) for i in range(1000)]:
        src = join(cat_dataset_dir, file_name)
        dst = join(train_cats_dir, file_name)
        shutil.copyfile(src, dst)
    for file_name in ["{}.jpg".format(i) for i in range(1000, 1500)]:
        src = join(cat_dataset_dir, file_name)
        dst = join(validation_cats_dir, file_name)
        shutil.copyfile(src, dst)
    for file_name in ["{}.jpg".format(i) for i in range(1500, 2000)]:
        src = join(cat_dataset_dir, file_name)
        dst = join(test_cats_dir, file_name)
        shutil.copyfile(src, dst)
    for file_name in ["{}.jpg".format(i) for i in range(1000)]:
        src = join(dog_dataset_dir, file_name)
        dst = join(train_dogs_dir, file_name)
        shutil.copyfile(src, dst)
    for file_name in ["{}.jpg".format(i) for i in range(1000, 1500)]:
        src = join(dog_dataset_dir, file_name)
        dst = join(validation_dogs_dir, file_name)
        shutil.copyfile(src, dst)
    for file_name in ["{}.jpg".format(i) for i in range(1500, 2000)]:
        src = join(dog_dataset_dir, file_name)
        dst = join(test_dogs_dir, file_name)
        shutil.copyfile(src, dst)


def get_rand_img_tensor():
    fnames = get_files_from_path(train_cats_dir)
    image = load_img(fnames[rng_int(0, len(fnames))], target_size=(150, 150))
    image_array = img_to_array(image)  # Converts it to a Numpy array with shape (150, 150, 3) #Reshapes it to (1, 150, 150, 3)
    return image, image_array


def check_datagen_effects():
    datagen = ImageDataGenerator(rotation_range=40, width_shift_range=0.2, height_shift_range=0.2, shear_range=0.2,
                                 zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')
    image, img_tensor = get_rand_img_tensor()
    x = img_tensor.reshape(
        (1,) + img_tensor.shape)  # Converts it to a Numpy array with shape (150, 150, 3) Reshapes it to (1, 150, 150, 3)
    images, i = [image], 0
    for batch in datagen.flow(x, batch_size=1):
        # Generates batches of randomly transformed images. Loops indefinitely
        images.append(array_to_img(batch[0]))
        i += 1
        if i % 100 == 0:
            break
    display_images(images, to_rgb=True)


def extract_features(directory, sample_count):
    if "datagen" not in v_extract_features:
        v_extract_features["datagen"] = ImageDataGenerator(rescale=1. / 255)
    conv_base = v_extract_features["conv_base"]
    datagen = v_extract_features["datagen"]
    batch_size = 20
    features = np.zeros(shape=(sample_count, 4, 4, 512))
    labels = np.zeros(shape=sample_count)
    generator = datagen.flow_from_directory(directory, target_size=(150, 150), batch_size=batch_size, class_mode='binary')
    i = 0
    for inputs_batch, labels_batch in generator:
        features_batch = conv_base.predict(inputs_batch)
        features[i * batch_size: (i + 1) * batch_size] = features_batch
        labels[i * batch_size: (i + 1) * batch_size] = labels_batch
        i += 1
        if i * batch_size >= sample_count:
            break
    return features, labels


def scratch_data_augmentation():
    test_datagen = ImageDataGenerator(rescale=1. / 255)  # The validation data shouldn’t be augmented
    train_datagen = ImageDataGenerator(rescale=1. / 255, rotation_range=40, width_shift_range=0.2, height_shift_range=0.2,
                                       shear_range=0.2, zoom_range=0.2, horizontal_flip=True)

    train_generator = train_datagen.flow_from_directory(train_dir, target_size=(150, 150), batch_size=20, class_mode='binary')
    validation_generator = test_datagen.flow_from_directory(validation_dir, target_size=(150, 150), batch_size=20,
                                                            class_mode='binary')
    data_batch, labels_batch = train_generator[0]
    print('data batch shape:', data_batch.shape)
    print('labels batch shape:', labels_batch.shape)
    return train_generator, test_datagen, validation_generator


def pretrained_data():
    train_features, train_labels = extract_features(train_dir, 2000)
    validation_features, validation_labels = extract_features(validation_dir, 1000)
    test_features, test_labels = extract_features(test_dir, 1000)
    train_features = np.reshape(train_features, (2000, 4 * 4 * 512))
    validation_features = np.reshape(validation_features, (1000, 4 * 4 * 512))
    test_features = np.reshape(test_features, (1000, 4 * 4 * 512))
    return train_features, train_labels, validation_features, validation_labels, test_features, test_labels


def pretrained_data_augmentation():
    train_datagen = ImageDataGenerator(rescale=1. / 255, rotation_range=40, width_shift_range=0.2, height_shift_range=0.2,
                                       shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    train_generator = train_datagen.flow_from_directory(train_dir, target_size=(150, 150), batch_size=20, class_mode='binary')
    validation_generator = test_datagen.flow_from_directory(validation_dir, target_size=(150, 150), batch_size=20,
                                                            class_mode='binary')
    return train_generator, test_datagen, validation_generator


def densely_connected_classifier():
    model = models.Sequential()
    model.add(layers.Dense(256, activation='relu', input_dim=4 * 4 * 512))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1, activation='sigmoid'))
    return model


def conv_n_densely_connected_classifier():
    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    print('This is the number of trainable weights ' 'before freezing the conv base:', len(model.trainable_weights))
    conv_base.trainable = False
    print('This is the number of trainable weights ' 'after freezing the conv base:', len(model.trainable_weights))
    return model


def show_all_channels_activation(model):
    layer_outputs_gen_model = [layer.output for layer in model.layers[:8]]
    activation_model_gen_model = models.Model(inputs=model.input, outputs=layer_outputs_gen_model)
    _, img_tensor = get_rand_img_tensor()
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    # Returns a list of five Numpy arrays one array per layer activation
    activations = activation_model_gen_model.predict(img_tensor)
    first_layer_activation = activations[0]
    plt.imshow(img_tensor[0])
    plt.matshow(first_layer_activation[0, :, :, 4], cmap='viridis')
    plt.show()
    layer_names = []
    for layer in model.layers[:8]:
        layer_names.append(layer.name)
    images_per_row = 16
    for layer_name, layer_activation in zip(layer_names, activations):
        n_features = layer_activation.shape[-1]
        size = layer_activation.shape[1]
        n_cols = n_features // images_per_row
        display_grid = np.zeros((size * n_cols, images_per_row * size))
        for col in range(n_cols):
            for row in range(images_per_row):
                channel_image = layer_activation[0, :, :, col * images_per_row + row]
                channel_image -= channel_image.mean()
                channel_image /= channel_image.std()
                channel_image *= 64
                channel_image += 128
                channel_image = np.clip(channel_image, 0, 255).astype('uint8')
                display_grid[col * size: (col + 1) * size, row * size: (row + 1) * size] = channel_image
        scale = 1. / size
        plt.figure(figsize=(scale * display_grid.shape[1], scale * display_grid.shape[0]))
        plt.title(layer_name)
        plt.grid(False)
        plt.imshow(display_grid, aspect='auto', cmap='viridis')
    plt.show()


def generate_pattern(layer_name, filter_index, size=150):
    def deprocess_image(x):
        x -= x.mean()
        x /= (x.std() + 1e-5)
        x *= 0.1
        x += 0.5
        x = np.clip(x, 0, 1)
        x *= 255
        x = np.clip(x, 0, 255).astype('uint8')
        return x

    model = VGG16(weights='imagenet', include_top=False)
    layer_output = model.get_layer(layer_name).output
    loss = K.mean(layer_output[:, :, :, filter_index])
    grads = K.gradients(loss, model.input)[0]
    grads /= (K.sqrt(K.mean(K.square(grads))) + 1e-5)
    iterate = K.function([model.input], [loss, grads])
    # loss_value, grads_value = iterate([np.zeros((1, 150, 150, 3))])
    input_img_data = np.random.random((1, size, size, 3)) * 20 + 128.  # Starts from a gray image with some noise
    step = 1.
    for i in range(40):
        loss_value, grads_value = iterate([input_img_data])  # Computes the loss value and gradient value
        input_img_data += grads_value * step  # Adjusts the input image in the direction that maximizes the loss
    return deprocess_image(input_img_data[0])


def all_filter_response_patterns():
    layer_name = 'block1_conv1'
    size = 64
    margin = 5
    results = np.zeros((8 * size + 7 * margin, 8 * size + 7 * margin, 3))
    for i in range(8):
        for j in range(8):
            filter_img = generate_pattern(layer_name, i + (j * 8), size=size)
            horizontal_start = i * size + i * margin
            horizontal_end = horizontal_start + size
            vertical_start = j * size + j * margin
            vertical_end = vertical_start + size
            results[horizontal_start: horizontal_end,
            vertical_start: vertical_end, :] = filter_img
    plt.figure(figsize=(20, 20))
    plt.imshow(results)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # create_dirs()
    # check_datagen_effects()

    train_datas, test_datas, validation_datas = scratch_data_augmentation()
    train_features, train_labels, validation_features, validation_labels, test_features, test_labels = pretrained_data()
    train_datas, test_datas, validation_datas = pretrained_data_augmentation()
    model = gen_model()
    model = densely_connected_classifier()
    model = conv_n_densely_connected_classifier()
    model.compile(optimizer=RMSprop(lr=1e-4), loss='binary_crossentropy', metrics=['accuracy'])
    model.compile(optimizer=RMSprop(lr=2e-5), loss='binary_crossentropy', metrics=['acc'])
    # model = load_model(model_path_save)
    model.summary()

    # show_all_channels_activation(model)
    # plt.imshow(generate_pattern('block3_conv1', 0))
    history = util.train_n_save(model, train_datas, validation_datas, epochs=30, steps_per_epoch=50)
    # history = train_n_save(model, (train_features, train_labels), (validation_features, validation_labels))
    # history = util.get_history(history_path_save)
    util.show_history_charts(history)
