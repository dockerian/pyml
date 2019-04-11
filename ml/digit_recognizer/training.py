"""
training.py
@author: Jinchi Zhang, Jason Zhu, Yunhan Li
@email: jizjiz148148@gmail.com, jzhu@infoblox.com, kpr.sajuuk@gmail.com

Training using gradient decent.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

from ml.digit_recognizer.datasvc import DataSvc
from ml.common.mathEx import \
    change_to_multi_class, \
    compute_cost_with_l2_regularization, \
    l_model_backward_with_l2, \
    l_model_forward
from ml.common.parameters import Parameters

# hyper-parameters
PWD = os.path.dirname(os.path.realpath(__file__))
LAYERS_DIMENSIONS = [784, 50, 35, 20, 15, 10]  # 5-layer model
NUMBER_OF_LABELS = 10
LEARNING_RATE = 0.009
NUMBER_OF_ITERATIONS = 8000
LAMBDA = 0.9


def l_layer_model(
    x, y, layers_dims,
    learning_rate=0.009, num_iterations=2000,
        print_cost=False, lambd=0.7):
    """
    training using gradient decent

    @param x: input X, numpy arrays
    @param y: actual answers Y, numpy arrays
    @param layers_dims: dimensions of layers, lists
    @param learning_rate: hyper-parameter alpha, floats
    @param num_iterations: hyper-parameter number of iterations, ints
    @param print_cost: whether print cost to system, booleans
    @param lambd: regularization hyper-parameter lambda, floats
    @return: trained parameters, dictionaries
    """

    costs = []  # keep track of cost

    parameters = Parameters(PWD)
    parameters.initialize_parameters_deep_he(layers_dims)

    for i in range(0, num_iterations):

        # Forward propagation: [LINEAR -> RELU]*(L-1) -> LINEAR -> SIGMOID.
        al, caches = l_model_forward(x, parameters.get())
        # print(AL)
        # print(y)
        # Compute costs
        cost = compute_cost_with_l2_regularization(al, y, parameters.get(), lambd)

        # Backward propagation.
        grads = l_model_backward_with_l2(al, y, caches, lambd)

        # Update parameters.
        parameters.update(grads, learning_rate)

        # Print the cost every 100 training example
        if print_cost and i % 100 == 0:
            print("Cost after iteration %i: %f" % (i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)

    # plot the cost
    plt.plot(np.squeeze(costs))
    plt.ylabel('cost')
    plt.xlabel('iterations (per tens)')
    plt.title("Learning rate =" + str(learning_rate))
    # plt.show()

    return parameters


def run():

    print('Start training ...')
    np.random.seed(1)
    data_svc = DataSvc()
    data_svc.load()
    train_x_orig, train_y_orig, = data_svc.trainings['x'], data_svc.trainings['y']

    # make multi-class ys
    train_y = change_to_multi_class(train_y_orig)

    # standardization
    train_x = train_x_orig/255.

    layers_dims = LAYERS_DIMENSIONS

    # train parameters
    parameters = l_layer_model(
        train_x, train_y, layers_dims,
        learning_rate=LEARNING_RATE, num_iterations=NUMBER_OF_ITERATIONS, print_cost=True, lambd=LAMBDA)

    # save parameters
    parameters.save()


if __name__ == '__main__':
        run()
