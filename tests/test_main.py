"""
# test_main
"""
import logging
import unittest


class MainTester(unittest.TestCase):
    """
    MainTester includes all unit tests for main module
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

    def test_main(self):
        import runpy
        result = runpy.run_module('ml.main', run_name='__main__')
        self.assertEqual(result['__name__'], '__main__')
        # print('main result:', result)
        pass
