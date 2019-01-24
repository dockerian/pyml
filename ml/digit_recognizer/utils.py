"""
@author: Jinchi Zhang, Jason Zhu
@email: jizjiz148148@gmail.com, jzhu@infoblox.com

Utilities functions.
"""
import os
import numpy as np

PWD = os.path.dirname(os.path.realpath(__file__))


def load_datas():
    """
    load datas from os
    for training, 39,998 pictures as train data, 2000 as test data

    @return: train and tests sets for training and analyzing, numpy arrays
    """
    print('\nLoading data sets')
    data = load_dataset('train.csv')
    data_modified = data[1:, :]
    train_set_x_orig = data_modified[1:39999, 1:]
    train_set_y_orig = data_modified[1:39999, 0]
    test_set_x_orig = data_modified[40000:, 1:]
    test_set_y_orig = data_modified[40000:, 0]

    # turning Xs to transpose for convention
    train_set_x_orig = train_set_x_orig.T
    test_set_x_orig = test_set_x_orig.T

    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))
    print('\nFinished loading data sets')
    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig


def load_dataset(data_name):
    """
    load data from os, datasets folder

    @param data_name: data name, string
    @return: data, numpy array
    """

    data_csv = os.path.join(PWD, 'datasets', data_name)
    data = np.genfromtxt(data_csv, delimiter=',')
    return data


def load_parameters():
    """
    load parameters saved from datasets. file name: saved_parameters.npy
    @return: loaded parameters
    """
    data_dir = os.path.dirname(os.path.realpath(__file__))
    saved_parameters = os.path.join(data_dir, 'datasets', 'saved_parameters.npy')
    print('\nloading saved parameters: {}'.format(saved_parameters))
    parameters = np.load(saved_parameters).item()

    return parameters


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
    save parameters from calculation to saved_parameters.npy
    @param parameters: parameters from calculation, dictionaries
    """
    data_dir = os.path.dirname(os.path.realpath(__file__))
    saved_parameters = os.path.join(data_dir, 'datasets', 'saved_parameters.npy')
    print('\nsaving parameters: {} ...'.format(saved_parameters))
    np.save(saved_parameters, parameters, allow_pickle=True, fix_imports=True)
