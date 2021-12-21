# This file contains functions to help writing code for deep learning.
# You can copy the functions or just use them.
# Created by Caleb Roelens
# 09-2021


import enum
import matplotlib.pyplot as plt
import sklearn.utils
from sklearn.datasets import make_blobs
import numpy as np
from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sns
from tensorflow.keras.callbacks import EarlyStopping
from skimage.io import imread, imshow
import random


class ModelLoss(enum):
    """Class made so you don't have to remember the correct string.\n Contains the possible loss for the compiler.\n"""
    CATEGORICAL_CROSSENTROPY = "categorical_crossentropy"
    BINARY_CROSSENTROPY = "binary_crossentropy"


class ModelActivation(enum):
    """
    Contains all possible model activation functions.\n
    """
    RELU = 'relu'
    SIGMOID = 'sigmoid'
    SOFTMAX = 'softmax'
    SOFTPLUS = 'softplus'
    SOFTSIGN = 'softsign'
    TAHN = 'tahn'
    SELU = 'selu'
    ELU = 'elu'
    EXPONENTIAL = 'exponential'


class ModelInitializers(enum):
    """
    Class with all initializers.\n
    """
    RANDOM_NORMAL = 'RandomNormal'
    RANDOM_UNIFORM = 'RandomUniform'
    TRUNCATED_NORMAL = 'TruncatedNormal'
    ZEROS = 'Zeros'
    ONES = 'Ones'
    GLOROT_NORMAL = 'GlorotNormal'
    GLOROT_UNIFORM = 'GlorotUniform'
    HE_NORMAL = 'HeNormal'
    IDENTITY = 'Identity'
    ORTHOGONAL = 'Orthogonal'
    CONSTANT = 'Constant'
    VARIANCE_SCALING = 'VarianceScaling'


# Generate random data
def generate_random_cluster_data(sample_count, class_count, random_state=0, cluster_std=1):
    """
    Generate blob data using the sklearn.dataset.make_blobs function.\n
    Originally from task 1.\n
    :param cluster_std: The cluster std
    :param random_state: The random state
    :param class_count: The amount of classes
    :param sample_count: The amount of sample to return
    """

    X, y = make_blobs(n_samples=sample_count, centers=class_count,
                      center_box=[-10, 10], random_state=random_state, cluster_std=cluster_std)
    return X, y


def get_input_shape(dataset):
    """
    Get the input shape to use for a neural network
    :param dataset: The X_train dataframe or array
    :return: The input dimension
    """
    return dataset.shape[1]


def create_model_accuracy_plot(history, legend=None):
    """
    Plots two accuracy plots.\n
    :param history: history param of your model
    :param legend: the legend to use. If None, defaults to 'train' and 'test'.
    :return: None, Shows a plot
    """
    if legend is None:
        legend = ['train', 'test']
    plt.plot(history.history['accuracy'], 'r')
    plt.plot(history.history['val_accuracy'], 'b')
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(legend, loc='upper left')
    plt.show()
    # Loss
    plt.plot(history.history['loss'], 'r')
    plt.plot(history.history['val_loss'], 'b')

    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(legend, loc='upper left')
    plt.show()


def print_accuracy_score(y_test, y_pred):
    """
    Print the accuracy score in %\n
    :param y_test: y_test
    :param y_pred: y_pred
    :return: No return, a print action
    """
    from sklearn.metrics import accuracy_score
    print(accuracy_score(y_test, y_pred) * 100, "%")


def range_f(start_value, stop_value, step_value, numpy_return=False):
    """
    Extended range function. Allows for the use of floats.\n
    :param start_value: The start value
    :param stop_value: The stop value
    :param step_value: The step value
    :return:
    """
    if numpy_return:
        return np.arange(start=start_value, stop=stop_value, step=step_value)
    else:
        return np.arange(start=start_value, stop=stop_value, step=step_value).tolist()


def print_confusion_matrix(y_test, y_pred):
    """
    Creates a clear readable confusion matrix
    :param y_test: y_test
    :param y_pred: y_pred 
    :return: a dataframe that visualises a confusion matrix
    """
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    cf_index = ["Actual 1", "Actual 0"]
    cf_data = {"Pred 1": [tp, fp], "Pred 0": [fn, tn]}
    confusion_matrix_visual = pd.DataFrame(cf_data, index=cf_index)
    return confusion_matrix_visual


def create_count_plot(label, dataset):
    """
    Create a count plot.\n
    :param label: The label to count.
    :param dataset: The dataset to use.
    :return: Shows a count plot.
    """
    sns.countplot(x=label, data=dataset)


def has_column(dataset, columns) -> bool:
    """
    Check if column has certain column id.\n
    :param dataset: dataset to look for column
    :param columns: the columns name
    :return: True or False
    """
    return columns in dataset.columns


def clean_shape_print(dataset):
    """
    Print the shape cleanly. Only for two dimensional ones. \n
    :param dataset: the dataset
    :return: a print statement
    """
    dataset_shape = dataset.shape
    print(f"{dataset_shape[0]} rows, {dataset_shape[1]} columns")


def create_early_stopping(monitor='loss', verbose=1, patience=5) -> EarlyStopping:
    """
    Create an early stopping object.\n
    :param monitor: default to balanced
    :param verbose: verbose
    :param patience: the patience of the es
    :return: EarlyStopping
    """
    return EarlyStopping(monitor=monitor, verbose=verbose, patience=patience)


def display_image_from_data(data, shape,  cmap='gray'):
    """
    Display an image. Format has to be one line. For example 784 values for shape 28x28 image.\n
    :return: Shows the image
    """
    imshow(data.reshape(shape), cmap=cmap)


def get_predictions(x_test, model):
    """
    Get the argmax prediction.\n
    :param x_test: X_test set
    :param model: The model
    :return: The prediction(s)
    """
    return np.argmax(model.predict(x_test), axis=-1)


def display_image_from_x_test(x_test, index):
    """
    Display an image from a x_test dataset
    :param x_test: the dataset
    :param index: the index of the image to show
    :return:
    """
    imshow(x_test[index])


def safe_shuffle(data1, data2, random_state):
    """
    Shuffle list in unison.\n
    :param data1: The first list
    :param data2: The second list
    :param random_state: The random state to use
    :return: The arrays
    """
    return sklearn.utils.shuffle(data1, data2, random_state=random_state)


def draw_square_on_image(square_shape, image_shape, image):
    """
    Draw a square on an image.\n
    :param square_shape: Shape of the square. Tuple
    :param image_shape: Shape of the image. Tuple
    :param image: The image to draw on.
    :return:
    """
    cover_points = np.random.randint(0, image_shape[0] - square_shape[0], size=2)
    x, y = cover_points
    cover_image = image.copy()
    cover_image[x:x + square_shape[0], y:y + square_shape[1]] = 1
    return cover_image


def add_ranged_column(value1, value2, column_label, dataset):
    """
    Add column that contains if certain column is between values.\n
    :return: The data
    """
    return np.where(dataset[column_label] <= value2, value1, 0)

