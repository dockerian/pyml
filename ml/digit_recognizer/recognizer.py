"""
recognizer.py
@author: Jinchi Zhang, Yunhan Li
@email: jizjiz148148@gmail.com, kpr.sajuuk@gmail.com

Predict on single pictures of digits for experiments.
"""

import os
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from ml.digit_recognizer.prediction import predict
from ml.digit_recognizer.utils import \
    load_parameters, \
    print_pypath

IMAGE_SIZE = 28
IMAGE_NAME = '3.jpg'
TRUE_ANSWER = 3
IMAGE_TYPE = 1  # 1 as white based, 2 as black based
PWD = os.path.dirname(os.path.realpath(__file__))


def predict_image(image_name, my_label_y, image_type):
    """
    predict images using one step of forward propagation.

    @param image_name: name of the image, strings
    @param my_label_y: actual answer y, numbers or numpy arrays
    @param image_type: 1: white based, 2: black based, ints
    """

    # load parameters
    parameters = load_parameters()

    fname = os.path.join(PWD, 'images', image_name)

    my_image = Image.open(fname).convert('L').resize((IMAGE_SIZE, IMAGE_SIZE))
    my_image_x = np.array(my_image).reshape([IMAGE_SIZE*IMAGE_SIZE, 1])

    # standardization with type
    if image_type == 1:
        my_image_x = 1 - my_image_x / 255.
    else:
        my_image_x = my_image_x / 255.

    my_predicted_image = predict(my_image_x, my_label_y, parameters)
    plt.imshow(my_image)
    plt.show(block=True)
    print('My model predicted this images as: ' + str(my_predicted_image) + '\nThis image is actually: ' + str(my_label_y))


def run():
    predict_image(IMAGE_NAME, TRUE_ANSWER, IMAGE_TYPE)


if __name__ == '__main__':
    print_pypath()
    run()
