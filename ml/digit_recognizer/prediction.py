"""
Prediction.py
predict training set and calculate accuracy
"""

from ml.digit_recognizer.mathEx import *
from ml.digit_recognizer.utils import \
    load_datas, \
    load_parameters, \
    print_pypath


def predict(x, y, parameters):
    """
    prediction over a dataset

    @param x: input X
    @param y: output Y
    @param parameters: parameters got from training
    @return: array of prediction
    """
    m = x.shape[1]
    n = len(parameters) // 2  # number of layers in the neural network

    # Forward propagation
    probas, caches = L_model_forward(x, parameters)

    # changing probabilities to predictions using one vs. all method
    prediction = one_vs_all_prediction(probas)

    # print (results)
    # print ("predictions: " + str(prediction))
    # print ("true labels: " + str(y))
    print("Accuracy: " + str(np.sum((prediction == y) / m)))

    return prediction


def run():
    np.random.seed(1)

    # load data
    train_x_orig, train_y_orig, test_x_orig, test_y_orig = load_datas()

    # standardization
    train_x = train_x_orig / 255.
    test_x = test_x_orig / 255.

    # load parameters
    parameters = load_parameters()

    # predict on training set and test set
    pred_train = predict(train_x, train_y_orig, parameters)
    pred_test = predict(test_x, test_y_orig, parameters)


if __name__ == '__main__':
    print_pypath()
    run()
