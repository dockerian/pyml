"""
mathEX.py
@author: Jinchi Zhang
@email: jizjiz148148@gmail.com

Math-related functions, extensions.
"""
import numpy as np


def change_to_multi_class(y, num_of_labels):
    """
    change the input prediction y to array-wise multi_class classifiers.

    @param y:input prediction y, numpy arrays
    @param num_of_labels: number of class we want to classify, ints
    @return: array-wise multi_class classifiers
    """

    m = y.shape[1]
    multi_class_y = np.zeros([num_of_labels, m])

    for i in range(m):
        label = y[0, i]
        multi_class_y[int(label), i] = 1

    return multi_class_y


def compute_cost(aL, y):
    """
    compute costs between output results and actual results y. NEEDS TO BE MODIFIED.

    @param aL: output results, numpy arrays
    @param y: actual result, numpy arrays
    @return: cost, floats
    """

    m = y.shape[1]

    # Compute loss from aL and y.
    cost = sum(sum((1. / m) * (-np.dot(y, np.log(aL).T) - np.dot(1 - y, np.log(1 - aL).T))))

    cost = np.squeeze(cost)

    assert (cost.shape == ())

    return cost


def compute_cost_with_l2_regularization(aL, y, parameters, lambd):
    """
    compute costs with L2 regularization, uses the original cost function.

    @param aL: results AL, numpy arrays
    @param y: actual results y, numpy arrays
    @param parameters: parameters got from forward propagation, dictionaries
    @param lambd: lambda for regularization, floats
    @return: cost, floats
    """
    m = y.shape[1]
    num_of_parameters = len(parameters) // 2
    w_square_sum = 0

    # adding up Ws
    for i in range(num_of_parameters):
        w_square_sum += np.sum(np.square(parameters['W'+str(i+1)]))

    # compute regular costs
    cross_entropy_cost = compute_cost(aL, y)

    # combine regular costs and regularization term
    l2_regularization_cost = (lambd / (2 * m)) * w_square_sum

    cost = cross_entropy_cost + l2_regularization_cost

    return cost


def initialize_parameters_deep_he(layer_dims):
    """
    initialization for deep learning with HE random algorithm to prevent fading & exploding gradients.

    @param layer_dims: dimensions of layers, lists
    @return: initialized parameters
    """

    np.random.seed(1)
    parameters = {}
    L = len(layer_dims)  # number of layers in the network

    for l in range(1, L):

        # initialized W with random and HE term
        parameters['W' + str(l)] = np.random.randn(layer_dims[l], layer_dims[l - 1]) * np.sqrt(2 / layer_dims[l - 1])

        parameters['b' + str(l)] = np.zeros((layer_dims[l], 1))

        assert (parameters['W' + str(l)].shape == (layer_dims[l], layer_dims[l - 1]))
        assert (parameters['b' + str(l)].shape == (layer_dims[l], 1))

    return parameters


"""
def initialize_parameters_deep(layer_dims):

    np.random.seed(1)
    parameters = {}
    L = len(layer_dims)  # number of layers in the network

    for l in range(1, L):
        parameters['W' + str(l)] = np.random.randn(layer_dims[l], layer_dims[l - 1])
        parameters['b' + str(l)] = np.zeros((layer_dims[l], 1))

        assert (parameters['W' + str(l)].shape == (layer_dims[l], layer_dims[l - 1]))
        assert (parameters['b' + str(l)].shape == (layer_dims[l], 1))

    return parameters
"""


def L_model_forward(x, parameters):
    """
    Forward propagation of deep learning.

    @param x: input x, numpy arrays
    @param parameters:
    @return: output aL and caches for following calculations, numpy arrays and indexes
    """

    caches = []
    a = x
    L = len(parameters) // 2  # number of layers in the neural network

    # Implement [LINEAR -> RELU]*(L-1). Add "cache" to the "caches" list.
    for l in range(1, L):
        a_prev = a

        # use relu or leaky relu in hiden layers
        a, cache = linear_activation_forward(a_prev, parameters['W' + str(l)], parameters['b' + str(l)],
                                             activation="leaky_relu") #was relu
        caches.append(cache)

    # Implement LINEAR -> SIGMOID. Add "cache" to the "caches" list.

    # output layer with sigmoid activation
    aL, cache = linear_activation_forward(a, parameters['W' + str(L)], parameters['b' + str(L)], activation="sigmoid")

    caches.append(cache)

    assert (aL.shape == (10, x.shape[1])) # shape[0] should be same with shape[0] of output layer

    return aL, caches


def L_model_backward_with_l2(aL, y, caches, lambd):
    """
    Backward propagation for deep learning with L2 regularization.

    @param aL: output AL, numpy arrays
    @param y: actual answers y, numpy arrays
    @param caches: caches from forward propagation, dictionaries
    @param lambd: regularization parameter lambda, floats
    @return: gradients for gradient decent, dictionaries
    """
    grads = {}
    L = len(caches)  # the number of layers
    m = aL.shape[1]
    y = y.reshape(aL.shape)  # after this line, Y is the same shape as AL

    # Initializing the back propagation
    dAL = - (np.divide(y, aL) - np.divide(1 - y, 1 - aL))

    # Lth layer Inputs: "AL, Y, caches". Outputs: "grads["dAL"], grads["dWL"], grads["dbL"]
    current_cache = caches[L - 1]
    grads["dA" + str(L - 1)], grads["dW" + str(L)], grads["db" + str(L)] = linear_activation_backward_with_l2(dAL, current_cache, lambd, activation="sigmoid")

    for l in reversed(range(L - 1)):
        # lth layer: (RELU -> LINEAR) gradients.
        current_cache = caches[l]

        # use relu or leaky relu for hiden layers
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward_with_l2(grads["dA" + str(l + 1)], current_cache,
                                                                                     lambd, activation="leaky_relu")
        grads["dA" + str(l)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp
        grads["db" + str(l + 1)] = db_temp

    return grads


def linear_activation_backward_with_l2(da, cache, lambd, activation):
    """
    activation step for backward propagation with multiple choices of activation function.

    @param da: dA from last step of backward propagation, numpy arrays
    @param cache: caches in deep learning, dictionaries
    @param lambd: regularization parameter lambda, floats
    @param activation: choice of activation, strings
    @return: last dA, dW, db, numpy arrays
    """

    linear_cache, activation_cache = cache

    if activation == "relu":
        dZ = relu_backward(da, activation_cache)
        dA_prev, dW, db = linear_backward_with_l2(dZ, linear_cache, lambd)

    elif activation == "sigmoid":
        dZ = sigmoid_backward(da, activation_cache)
        dA_prev, dW, db = linear_backward_with_l2(dZ, linear_cache, lambd)

    elif activation == "leaky_relu":
        dZ = leaky_relu_backward(da, activation_cache)
        dA_prev, dW, db = linear_backward_with_l2(dZ, linear_cache, lambd)

    return dA_prev, dW, db


def linear_activation_forward(a_prev, w, b, activation):
    """
    activation step for forward propagation with multiple choices of activation function.

    @param a_prev: previous A from last step of forward propagation, numpy arrays
    @param w: parameter W in current layer, numpy arrays
    @param b: parameter b in current layer, numpy arrays
    @param activation: choice of activation, strings
    @return: current A and cache for following calculation
    """

    if activation == "sigmoid":
        # Inputs: "A_prev, W, b". Outputs: "A, activation_cache".
        Z, linear_cache = linear_forward(a_prev, w, b)
        A, activation_cache = sigmoid(Z)

    elif activation == "relu":
        # Inputs: "A_prev, W, b". Outputs: "A, activation_cache".
        Z, linear_cache = linear_forward(a_prev, w, b)
        A, activation_cache = relu(Z)

    elif activation == "leaky_relu":
        # Inputs: "A_prev, W, b". Outputs: "A, activation_cache".
        Z, linear_cache = linear_forward(a_prev, w, b)
        A, activation_cache = leaky_relu(Z)

    assert (A.shape == (w.shape[0], a_prev.shape[1]))
    cache = (linear_cache, activation_cache)
    return A, cache


def linear_backward_with_l2(dz, cache, lambd):
    """
    linear step in backward propagation.

    @param dz: current dZ, numpy arrays
    @param cache: caches from previous calculation, dictionaries
    @param lambd: regularization parameter lambda, floats
    @return: previous dA, current dW, db, numpy arrays
    """

    a_prev, w, b = cache
    m = a_prev.shape[1]
    dW = 1. / m * np.dot(dz, a_prev.T) + (lambd / m) * w
    db = 1. / m * np.sum(dz, axis=1, keepdims=True)
    dA_prev = np.dot(w.T, dz)

    # dA_prev = dropouts_backward(dA_prev, D, keep_prob)

    assert (dA_prev.shape == a_prev.shape)
    assert (dW.shape == w.shape)
    assert (db.shape == b.shape)

    return dA_prev, dW, db


def linear_forward(a, w, b):
    """
    linear step for forward propagation
    @param a: current A, numpy arrays
    @param w: current parameter W, numpy arrays
    @param b: current parameter b, numpy arrays
    @return: current z, and caches for following calculations, numpy arrays and dictionaries
    """

    z = w.dot(a) + b

    assert (z.shape == (w.shape[0], a.shape[1]))
    cache = (a, w, b)

    return z, cache


def one_vs_all_prediction(prob_matrix):
    """
    Compare every probability, get the maximum and output the index.

    @param prob_matrix: probability matrix, numpy arrays
    @return: prediction generated from probability matrix, numpy arrays
    """
    m = prob_matrix.shape[1]

    prediction = np.argmax(prob_matrix, axis=0)
    prediction = np.array([prediction])  # keep dimensions

    assert (prediction.shape == (1, m))

    return prediction


def relu(z):
    """
    relu function

    @param z: input A, numpy arrays or numbers
    @return: output A, numpy arrays or numbers
    """

    a = np.maximum(0, z)

    assert (a.shape == z.shape)

    cache = z
    return a, cache


def relu_backward(da, cache):
    """
    compute gradient of relu function.

    @param da: input dA, numpy arrays or numbers
    @param cache: caches with Z, dictionaries
    @return: result dZ, numpy arrays or numbers
    """

    z = cache
    dz = np.array(da, copy=True)  # just converting dz to a correct object.

    # When z <= 0s you should set dz to 0 as well.
    dz[z <= 0] = 0

    assert (dz.shape == z.shape)

    return dz


def leaky_relu(z):
    """
    leaky relu function

    @param z: input Z, numpy arrays or numbers
    @return: result A and caches for following calculation
    """

    a = np.maximum(0.01 * z, z)

    assert (a.shape == z.shape)

    cache = z
    return a, cache


def leaky_relu_backward(da, cache):
    """
    compute gradients of leaky relu function.

    @param da: input dA, numpy arrays or numbers
    @param cache: cache with Z, dictionaries
    @return: result dZ, numpy arrays or numbers
    """

    z = cache
    dz = np.array(da, copy=True)  # just converting dz to a correct object.

    # When z < 0, you should set dz to 0.01  as well.
    #temp = np.ones(Z.shape)
    #temp[Z <= 0] = 0.01
    #dZ = dZ*temp


    #Z[Z > 0] = 1
    #Z[Z != 1] = 0.01
    #dZ = dZ*Z

    temp = np.ones_like(z)
    temp[z < 0] = 0.01
    dz = dz*temp

    assert (dz.shape == z.shape)

    return dz


def sigmoid(z):
    """
    sigmoid function.

    @param z: input Z, numpy arrays or numbers
    @return: result A, caches for following calculations, numpy arrays or numbers, dictionaries
    """

    a = 1 / (1 + np.exp(-z))
    cache = z

    return a, cache


def sigmoid_backward(da, cache):
    """
    compute gradients of sigmoid function.

    @param da: input dA, numpy arrays or numbers
    @param cache: caches with Z, dictionaries
    @return: result dZ, numpy arrays or numbers
    """

    z = cache

    s = 1 / (1 + np.exp(-z))
    dz = da * s * (1 - s)

    assert (dz.shape == z.shape)

    return dz


"""
unused dropout functions
def dropouts_forward(A,  activation_cache, keep_prob):
    D = np.random.rand(A.shape[0], A.shape[1])
    D = D < keep_prob
    A = A * D
    A = A / keep_prob
    cache = (activation_cache, D)
    return A, cache


def dropouts_backward(dA, D, keep_prob):
    dA = dA*D
    dA = dA/keep_prob
    return dA
"""


def update_parameters(parameters, grads, learning_rate):
    """
    update parameters with gradients.

    @param parameters: input parameters, dictionaries
    @param grads: gradients, dictionaries
    @param learning_rate: hyper-parameter alpha for deep learning, floats
    @return: updated parameters, dictionaries
    """

    L = len(parameters) // 2  # number of layers in the neural network

    # Update rule for each parameter. Use a for loop.
    for l in range(L):
        parameters["W" + str(l + 1)] = parameters["W" + str(l + 1)] - learning_rate * grads["dW" + str(l + 1)]
        parameters["b" + str(l + 1)] = parameters["b" + str(l + 1)] - learning_rate * grads["db" + str(l + 1)]

    return parameters




