"""

"""
import matplotlib.pyplot as plt
import numpy as np
import os

from ml.common.mathEx import \
    compute_cost_with_l2_regularization, \
    l_model_backward_with_l2, \
    l_model_forward
from ml.classifier.datasvc import DataSvc
from ml.common.parameters import Parameters


PWD = os.path.dirname(os.path.realpath(__file__))
NUM_ITERATIONS = 2000
LAMBD = 0.7
LEARNING_RATE = 0.0075


def l_layer_model(x, y, layers_dims, learning_rate=0.009, num_iterations=2000, print_cost=False, lambd=0.7):
    """

    @param x:
    @param y:
    @param layers_dims:
    @param learning_rate:
    @param num_iterations:
    @param print_cost:
    @return:
    """

    np.random.seed(1)
    costs = []  # keep track of cost

    parameters = Parameters(PWD)
    parameters.initialize_parameters_deep_he(layers_dims)

    for i in range(0, num_iterations):

        # Forward propagation: [LINEAR -> RELU]*(L-1) -> LINEAR -> SIGMOID.
        al, caches = l_model_forward(x, parameters.get())

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
    """
    """
    np.random.seed(1)
    print('Start training ...')

    data_svc = DataSvc()
    data_svc.load()
    train_x_orig, train_y = data_svc.trainings['x'], data_svc.trainings['y']
    # Reshape the training and test examples
    train_x_flatten = train_x_orig.reshape(train_x_orig.shape[0], -1).T

    # Standardize data to have feature values between 0 and 1.
    train_x = train_x_flatten/255.

    # CONSTANTS #
    layers_dims = [12288, 20, 7, 5, 3, 1]  # 5-layer model

    parameters = l_layer_model(
        train_x, train_y, layers_dims,
        learning_rate=LEARNING_RATE, num_iterations=NUM_ITERATIONS, print_cost=True, lambd=LAMBD)
    # print(type(parameters))
    parameters.save()


if __name__ == '__main__':
    run()
