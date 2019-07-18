"""
test_misc_image_rect.py
"""
import logging
import unittest

from ml.misc.image_rect import \
    find_rectangle, find_rects
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class ImageRectTests(unittest.TestCase):
    """
    ImageRectangleTests includes all unit tests for ml.misc.image_rect module
    """
    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def setUp(self):
        """setup for test"""
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    def test_find_rectangle(self):
        tests = [{
            "image": [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 1],
                [1, 1, 1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ],
            "expected": [[2, 3], [3, 5]],
        }, {
            "image": [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 0],
            ],
            "expected": [[4, 6], [4, 6]],
        }, {
            "image": [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 0],
                [1, 1, 1, 1, 1, 0, 0],
            ],
            "expected": [[3, 5], [4, 6]],
        }, {
            "image": [
                [0, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ],
            "expected": [[0, 0], [0, 0]],
        }, {
            "image": [[0]],
            "expected": [[0, 0], [0, 0]],
        }]
        for idx, test in enumerate(tests):
            image = test['image']
            expected = test['expected']
            result = find_rectangle(image)
            msg = "Test %02d:\n%s\nexpect to find\n%s in\n%s" % (
                idx, result, expected, image)
            LOGGER.info(msg)
            self.assertListEqual(result, expected, msg)
        pass

    def test_find_rects(self):
        tests = [{
            "image": [
              [0, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 0, 0, 0, 1],
              [1, 0, 1, 0, 0, 0, 1],
              [1, 0, 1, 1, 1, 1, 1],
              [1, 0, 1, 0, 0, 1, 1],
              [1, 1, 1, 0, 0, 1, 1],
              [1, 1, 1, 1, 1, 1, 0],
            ],
            "rects": [
                [[0, 0], [0, 0]],
                [[2, 3], [3, 5]],
                [[3, 1], [5, 1]],
                [[5, 3], [6, 4]],
                [[7, 6], [7, 6]],
            ],
        }, {
            "image": [
              [0, 1, 1, 1, 1, 1, 1],
              [1, 1, 0, 0, 1, 1, 1],
              [1, 1, 1, 0, 0, 0, 1],
              [1, 0, 1, 0, 0, 0, 1],
              [1, 0, 1, 1, 1, 1, 1],
              [1, 0, 1, 0, 0, 1, 1],
              [1, 1, 1, 0, 0, 1, 1],
              [1, 1, 1, 1, 1, 1, 0],
            ],
            "rects": [
                [[0, 0], [0, 0]],
                [[1, 2], [1, 3]],
                [[2, 3], [3, 5]],
                [[3, 1], [5, 1]],
                [[5, 3], [6, 4]],
                [[7, 6], [7, 6]],
            ],
        }, {
            "image": [
              [0, 1, 1, 1, 0, 0, 0],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 0, 0, 0, 1],
              [1, 0, 1, 0, 0, 0, 1],
              [1, 0, 1, 1, 1, 1, 1],
              [1, 0, 1, 0, 0, 1, 1],
              [1, 1, 1, 0, 0, 1, 1],
              [1, 1, 1, 1, 1, 1, 0],
            ],
            "rects": [
                [[0, 0], [0, 0]],
                [[0, 4], [0, 6]],
                [[2, 3], [3, 5]],
                [[3, 1], [5, 1]],
                [[5, 3], [6, 4]],
                [[7, 6], [7, 6]],
            ],
        }, {
            "image": [
                [0],
            ],
            "rects": [
                [[0, 0], [0, 0]],
            ],
        }, {
            "image": [
                [1],
            ],
            "rects": []
        }]
        for idx, test in enumerate(tests):
            image = test['image']
            rects = test['rects']
            result = find_rects(image)
            msg = "Test %02d:\n%s\nexpect to find\n%s in\n%s" % (
                idx, result, rects, image)
            LOGGER.info(msg)
            self.assertListEqual(result, rects, msg)
        pass
