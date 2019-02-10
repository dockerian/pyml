"""
common.datasvc_abstract.py
"""
import abc
import h5py
import inspect
import numpy as np
import os

from ml.utils.logger import get_logger
from ml.utils.logger import raise_ni

LOGGER = get_logger(__name__)
PWD = os.path.dirname(os.path.realpath(__file__))


class DataSvcAbstract:
    """
    DataSvcAbstract class provides abstract interfaces to any data service.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, base_path=PWD):
        self.base_path = base_path if os.path.isdir(base_path) else PWD
        self.trainings = {"x": None, "y": None}  # x, y should be numpy arrays
        self.tests_set = {"x": None, "y": None}  # x, y should be numpy arrays

    def load(self):
        """
        Abstract method to load data
        """
        name = inspect.currentframe().f_code.co_name
        raise_ni(name)

    def load_dataset(self, data_name, data_type='csv'):
        """
        load data from os, datasets folder

        @param data_name: data name, string
        @param data_type: data type, string
        @return: data, numpy array
        """
        data = None
        data_file = '{}.{}'.format(data_name, data_type)
        data_path = os.path.join(self.base_path, 'datasets', data_file)
        if data_type == 'csv':
            data = np.genfromtxt(data_path, delimiter=',')
        elif data_type == 'h5':
            data = h5py.File(data_path, 'r')

        return data
