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

    def update(self, grads, learning_rate):
        """
        update parameters with gradients.

        @param grads: gradients, dictionaries
        @param learning_rate: hyper-parameter alpha for deep learning, floats
        """

        L = len(self._parameters) // 2  # number of layers in the neural network

        # Update rule for each parameter. Use a for loop.
        for l in range(L):
            self._parameters["W" + str(l + 1)] = \
                self._parameters["W" + str(l + 1)] - learning_rate * grads["dW" + str(l + 1)]
            self._parameters["b" + str(l + 1)] = \
                self._parameters["b" + str(l + 1)] - learning_rate * grads["db" + str(l + 1)]

    def initialize_parameters_deep_he(self, layer_dims):
        """
        initialization for deep learning with HE random algorithm to prevent fading & exploding gradients.

        @param layer_dims: dimensions of layers, lists
        @return: initialized parameters
        """

        np.random.seed(1)
        parameters = {}
        l = len(layer_dims)  # number of layers in the network

        for l in range(1, l):
            # initialized W with random and HE term
            parameters['W' + str(l)] = np.random.randn(layer_dims[l], layer_dims[l - 1]) * np.sqrt(
                2 / layer_dims[l - 1])

            parameters['b' + str(l)] = np.zeros((layer_dims[l], 1))

            assert (parameters['W' + str(l)].shape == (layer_dims[l], layer_dims[l - 1]))
            assert (parameters['b' + str(l)].shape == (layer_dims[l], 1))

        self._parameters = parameters
