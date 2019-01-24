"""

"""
import h5py
import numpy as np
import os
from matplotlib import pyplot as plt


PWD = os.path.dirname(os.path.realpath(__file__))


def load_data():
    """
    """
    train_dataset = load_train_datasets()
    # print(type(train_dataset))
    train_set_x_orig = np.array(train_dataset['train_set_x'][:])  # your train set features
    train_set_y_orig = np.array(train_dataset['train_set_y'][:])  # your train set labels

    test_dataset = load_test_datasets()
    test_set_x_orig = np.array(test_dataset['test_set_x'][:])  # your test set features
    test_set_y_orig = np.array(test_dataset['test_set_y'][:])  # your test set labels

    classes = np.array(test_dataset['list_classes'][:])  # the list of classes

    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes


def load_train_datasets():
    """
    """
    data_train_h5 = os.path.join(PWD, 'datasets', 'train_catvnoncat.h5')
    train_dataset = h5py.File(data_train_h5, 'r')
    return train_dataset


def load_test_datasets():
    """
    """
    data_tests_h5 = os.path.join(PWD, 'datasets', 'test_catvnoncat.h5')
    test_dataset = h5py.File(data_tests_h5, 'r')
    return test_dataset


def load_parameters():
    """
    """
    data_dir = os.path.dirname(os.path.realpath(__file__))
    saved_parameters = os.path.join(data_dir, 'datasets', 'saved_parameters.npy')
    print('\nloading saved parameters: {}'.format(saved_parameters))
    parameters = np.load(saved_parameters).item()

    return parameters


def print_mislabeled_images(classes, X, y, p):
    """
    """
    a = p + y
    mislabeled_indices = np.asarray(np.where(a == 1))
    plt.rcParams['figure.figsize'] = (40.0, 40.0)  # set default size of plots
    num_images = len(mislabeled_indices[0])
    for i in range(num_images):
        index = mislabeled_indices[1][i]

        plt.subplot(2, num_images, i + 1)
        plt.imshow(X[:, index].reshape(64, 64, 3), interpolation='nearest')
        plt.axis('off')
        plt.title(
            "Prediction: " + classes[int(p[0, index])].decode("utf-8") + " \n Class: " + classes[y[0, index]].decode(
                "utf-8"))


def print_pypath():
    """
    Print out Python path.
    """
    import sys
    print('\nPYTHONPATH')
    print('.'*80)
    for p in sys.path:
        print(p)
    print('.' * 80)


def save_parameters(parameters):
    """
    """
    data_dir = os.path.dirname(os.path.realpath(__file__))
    saved_parameters = os.path.join(data_dir, 'datasets', 'saved_parameters.npy')
    print('\nsaving parameters: {} ...'.format(saved_parameters))
    np.save(saved_parameters, parameters, allow_pickle=True, fix_imports=True)
