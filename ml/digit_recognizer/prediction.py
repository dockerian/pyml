"""
Prediction.py
predict training set and calculate accuracy
"""
import os
import numpy as np

from ml.common.mathEx import one_vs_all_prediction, l_model_forward
from ml.digit_recognizer.datasvc import DataSvc
from ml.common.parameters import Parameters

PWD = os.path.dirname(os.path.realpath(__file__))


def predict(x, y, parameters):
    """
    prediction over a dataset

    @param x: input X
    @param y: output Y
    @param parameters: parameters got from training
    @return: array of prediction
    """
    # m = x.shape[1]
    # n = len(parameters) // 2  # number of layers in the neural network

    # Forward propagation
    probas, caches = l_model_forward(x, parameters)

    # changing probabilities to predictions using one vs. all method
    prediction = one_vs_all_prediction(probas)

    # print (results)
    # print ("predictions: " + str(prediction))
    # print ("true labels: " + str(y))
    # print("Accuracy: " + str(np.sum((prediction == y) / m)))

    return prediction


def run():
    np.random.seed(1)

    # load data
    data_svc = DataSvc()
    data_svc.load()
    train_x_orig, train_y_orig = data_svc.trainings['x'], data_svc.trainings['y']
    test_x_orig, test_y_orig = data_svc.tests_set['x'], data_svc.tests_set['y']
    m_train = train_x_orig.shape[1]
    m_test = test_x_orig.shape[1]

    # standardization
    train_x = train_x_orig / 255.
    test_x = test_x_orig / 255.

    # load parameters
    parameters = Parameters(PWD)
    parameters.load()

    # predict on training set and test set
    pred_train = predict(train_x, train_y_orig, parameters.get())
    pred_test = predict(test_x, test_y_orig, parameters.get())
    print('Accuracy on training set: ', str(np.sum((pred_train == train_y_orig) / m_train)))
    print('Accuracy on test set: ', str(np.sum((pred_test == test_y_orig) / m_test)))


if __name__ == '__main__':
    run()
