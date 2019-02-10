"""
datasvc.py

@author: Jinchi Zhang
@email: jizjiz148148@gmail.com

Services for loading data and pamrameters
"""
import numpy as np
import os

from ml.utils.logger import get_logger
from ml.common.datasvc_abstract import DataSvcAbstract

LOGGER = get_logger(__name__)
PWD = os.path.dirname(os.path.realpath(__file__))


class DataSvc(DataSvcAbstract):
    """
    Class DataSvc for classifier
    """

    def __init__(self, base_path=PWD):
        """
        Constructor of DataSvc

        :param base_path: base path, string
        """
        path = base_path if os.path.isdir(base_path) else PWD
        super().__init__(path)

    def load(self):
        """
        load data for classifiers
        """
        LOGGER.info('Loading data sets ...')
        train_dataset = super().load_dataset('train_catvnoncat', 'h5')
        # print(type(train_dataset))
        train_set_x_orig = np.array(train_dataset['train_set_x'][:])  # your train set features
        train_set_y_orig = np.array(train_dataset['train_set_y'][:])  # your train set labels

        test_dataset = super().load_dataset('test_catvnoncat', 'h5')
        test_set_x_orig = np.array(test_dataset['test_set_x'][:])  # your test set features
        test_set_y_orig = np.array(test_dataset['test_set_y'][:])  # your test set labels

        # classes = np.array(test_dataset['list_classes'][:])  # the list of classes NOT USING

        train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
        test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))

        self.trainings = {
            'x': train_set_x_orig,
            'y': train_set_y_orig,
        }
        self.tests_set = {
            'x': test_set_x_orig,
            'y': test_set_y_orig,
        }
        LOGGER.info('Loading data sets - DONE')
