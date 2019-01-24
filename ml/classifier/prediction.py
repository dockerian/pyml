"""

"""

import scipy
from scipy import ndimage
from matplotlib import pyplot as plt

from ml.classifier.mathEx import *
from ml.classifier.utils import \
    load_data, \
    load_parameters, \
    print_pypath


def predict(X, y, parameters):
    """

    @param X:
    @param y:
    @param parameters:
    @return:
    """

    m = X.shape[1]
    n = len(parameters) // 2  # number of layers in the neural network
    p = np.zeros((1, m))

    # Forward propagation
    probas, caches = L_model_forward(X, parameters)

    # convert probas to 0/1 predictions
    for i in range(0, probas.shape[1]):
        if probas[0, i] > 0.5:
            p[0, i] = 1
        else:
            p[0, i] = 0

    # print(results)
    # print("predictions: " + str(p))
    # print("true labels: " + str(y))
    print("Accuracy: " + str(np.sum((p == y) / m)))

    return p


def run():
    np.random.seed(1)

    train_x_orig, train_y, test_x_orig, test_y, classes = load_data()
    m_train = train_x_orig.shape[0]
    num_px = train_x_orig.shape[1]
    m_test = test_x_orig.shape[0]
    # Reshape the training and test examples
    train_x_flatten = train_x_orig.reshape(train_x_orig.shape[0], -1).T
    test_x_flatten = test_x_orig.reshape(test_x_orig.shape[0], -1).T

    # Standardize data to have feature values between 0 and 1.
    train_x = train_x_flatten/255.
    test_x = test_x_flatten/255.

    parameters = load_parameters()
    pred_train = predict(train_x, train_y, parameters)
    pred_test = predict(test_x, test_y, parameters)

    my_image = "cat3.jpg"
    my_label_y = [1]

    fname = "images/" + my_image
    image = np.array(ndimage.imread(fname, flatten=False))
    my_image = scipy.misc.imresize(image, size=(num_px, num_px)).reshape((num_px*num_px*3, 1))
    my_image = my_image/255.
    my_predicted_image = predict(my_image, my_label_y, parameters)
    plt.imshow(image)
    print ("y = " + str(np.squeeze(my_predicted_image)) + ", your L-layer model predicts a \"" + classes[int(np.squeeze(my_predicted_image)),].decode("utf-8") +  "\" picture.")
    plt.show(block=False)


if __name__ == '__main__':
    print_pypath()
    run()
