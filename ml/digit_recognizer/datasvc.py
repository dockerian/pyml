"""
datasvc.py

@author: Jinchi Zhang
@email: jizjiz148148@gmail.com

Services for loading data and pamrameters
"""

import os

from ml.utils.logger import get_logger
from ml.common.datasvc_abstract import DataSvcAbstract

LOGGER = get_logger(__name__)
PWD = os.path.dirname(os.path.realpath(__file__))


class DataSvc(DataSvcAbstract):
    """
    Class DataSvc for digit-recogonizer
    """

    def __init__(self, base_path=PWD):
        """
        Constructor of DataSvc

        :param base_path: base path, string
        """
        path = base_path if os.path.isdir(base_path) else PWD
        super().__init__(path)

    def load(self, data_name='train'):
        """
        load datas from os
        for training, 39,998 pictures as train data, 2000 as test data

        @return: train and tests sets for training and analyzing, numpy arrays
        """
        LOGGER.info('Loading data sets ...')
        data = super().load_dataset(data_name)
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
        self.trainings = {
            'x': train_set_x_orig,
            'y': train_set_y_orig,
        }
        self.tests_set = {
            'x': test_set_x_orig,
            'y': test_set_y_orig,
        }
        LOGGER.info('Loading data sets - DONE')
