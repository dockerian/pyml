"""
common.parameters.py
"""

import numpy as np
import os

from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)
PWD = os.path.dirname(os.path.realpath(__file__))


class Parameters:
    """
    DataSvcAbstract class provides abstract interfaces to any data service.
    """

    def __init__(self, base_path=PWD, file_name="saved_parameters.npy"):
        self.base_path = base_path if os.path.isdir(base_path) else PWD
        self._param_file = os.path.join(self.base_path, 'datasets', file_name)
        self._parameters = None

    def load(self):
        """
        load parameters saved from datasets. file name: saved_parameters.npy
        @return: loaded parameters
        """
        LOGGER.info('loading saved parameters: {}'.format(self._param_file))
        self._parameters = np.load(self._param_file).item()
        return self._parameters

    def save(self, parameters):
        """
        save parameters from calculation to saved_parameters.npy
        @param parameters: parameters from calculation, dictionaries
        """
        LOGGER.info('saving parameters: {} ...'.format(self._param_file))
        np.save(self._param_file, parameters, allow_pickle=True, fix_imports=True)
