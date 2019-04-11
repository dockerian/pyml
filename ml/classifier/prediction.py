"""

"""

import scipy
from scipy import ndimage
from matplotlib import pyplot as plt
import os
import numpy as np

from ml.common.mathEx import l_model_forward
from ml.classifier.datasvc import DataSvc
from ml.common.parameters import Parameters


PWD = os.path.dirname(os.path.realpath(__file__))
SHOW_IMAGE = True


def predict(x, y, parameters):
    m = x.shape[1]
    # n = len(parameters) // 2  # number of layers in the neural network
    p = np.zeros((1, m))

    # Forward propagation
    probas, caches = l_model_forward(x, parameters)

    # convert probas to 0/1 predictions
    for i in range(0, probas.shape[1]):
        if probas[0, i] > 0.5:
            p[0, i] = 1
        else:
            p[0, i] = 0

    # print(results)
    # print("predictions: " + str(p))
    # print("true labels: " + str(y))
    # print("Accuracy: " + str(np.sum((p == y) / m)))

    return p


def run():
    np.random.seed(1)

    data_svc = DataSvc()
    data_svc.load()
    train_x_orig, train_y = data_svc.trainings['x'], data_svc.trainings['y']
    test_x_orig, test_y = data_svc.tests_set['x'], data_svc.tests_set['y']
    m_train = train_x_orig.shape[0]
    num_px = train_x_orig.shape[1]
    m_test = test_x_orig.shape[0]

    # Reshape the training and test examples
    train_x_flatten = train_x_orig.reshape(train_x_orig.shape[0], -1).T
    test_x_flatten = test_x_orig.reshape(test_x_orig.shape[0], -1).T

    # Standardize data to have feature values between 0 and 1.
    train_x = train_x_flatten/255.
    test_x = test_x_flatten/255.

    parameters = Parameters(PWD)
    parameters.load()
    pred_train = predict(train_x, train_y, parameters.get())
    pred_test = predict(test_x, test_y, parameters.get())
    print('Accuracy on training set: ', str(np.sum((pred_train == train_y) / m_train)))
    print('Accuracy on test set: ', str(np.sum((pred_test == test_y) / m_test)))

    my_image = "cat3.jpg"
    my_label_y = [1]
    fname = "images/" + my_image
    image = np.array(ndimage.imread(fname, flatten=False))
    my_image = scipy.misc.imresize(image, size=(num_px, num_px)).reshape((num_px*num_px*3, 1))
    my_image = my_image/255.
    my_predicted_image = predict(my_image, my_label_y, parameters.get())
    plt.imshow(image)
    print("1 if is the object, 0 if not: " + str(np.squeeze(my_predicted_image)))
    plt.show(block=SHOW_IMAGE)


if __name__ == '__main__':
    run()
