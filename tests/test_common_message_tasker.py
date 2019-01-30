"""
# test_common_message_tasker
"""
import logging
import unittest

from ml.common.message_tasker import MessageTasker


class MessageTaskerTester(unittest.TestCase):
    """
    MessageTaskerTester includes all unit tests for common.message_tasker module
    """

    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def _func_task_1(self, message, **kwargs):
        message['step 1'] = 'init'
        return kwargs.update({'data 1': 'updated'})

    def _func_task_2(self, message, **kwargs):
        message['step 2'] = 'done'
        return kwargs.update({'data 2': 'updated'})

    def _func_task_2_1(self, message, **kwargs):
        message['step 2.1'] = 'done'
        message['step 1'] = 'overwritten by step 2.1'
        return kwargs.update({'data 2.1': 'updated'})

    def _func_task_2_1_1(self, message, **kwargs):
        message['step 2.1.1'] = 'done'
        message['step 1'] = 'overwritten by step 2.1.1'
        return kwargs.update({'data 2.1.1': 'updated'})

    def _func_task_2_1_1_1(self, message, **kwargs):
        message['step 2.1.1.1'] = 'done'
        message['step 1'] = 'overwritten by step 2.1.1.1'
        return kwargs.update({'data 2.1.1.1': 'updated'})

    def _func_task_2_1_1_1_1(self, message, **kwargs):
        message.update(kwargs)
        message['step 2.1.1.1.1'] = 'done'
        message['step 1'] = 'overwritten by step 2.1.1.1.1'
        return kwargs.update({'data 2.1.1.1.1': 'updated'})

    def _func_task_2_2(self, message, **kwargs):
        message['step 2.2'] = 'done'
        return kwargs.update({'data 2.2': 'updated'})

    def _func_task_3(self, message, **kwargs):
        message['step 3'] = 'done'
        return kwargs.update({'data 3': 'updated'})

    def setUp(self):
        """
        setup for tests.
        """
        self.tasks = [{
            "_name": "task_1",
            "_func": self._func_task_1,
            "tasks": []
        }, {
            "_name": "task_2",
            "_func": self._func_task_2,
            "tasks": [{
                "_name": "task_2.1",
                "_func": self._func_task_2_1,
                "tasks": [{
                    "_name": "task_2.1.1",
                    "_func": self._func_task_2_1_1,
                    "tasks": [{
                        "_name": "task_2.1.1.1",
                        "_func": self._func_task_2_1_1_1,
                        "tasks": [{
                            "_name": "task_2.1.1.1.1",
                            "_func": self._func_task_2_1_1_1_1,
                        }]
                    }]
                }]
            }, {
                "_name": "task_2.2",
                "_func": self._func_task_2_2,
            }]
        }, {
            "_name": "task_3",
            "_func": self._func_task_3,
        }]

        self.tasks_results = [{
            'step 1': 'init',
            'step 2': 'done',
            'step 3': 'done',
        }, {
            'step 1': 'overwritten by step 2.1',
            'step 2': 'done',
            'step 2.1': 'done',
            'step 2.2': 'done',
            'step 3': 'done',
        }, {
            'step 1': 'overwritten by step 2.1.1',
            'step 2': 'done',
            'step 2.1': 'done',
            'step 2.1.1': 'done',
            'step 2.2': 'done',
            'step 3': 'done',
        }, {
            'step 1': 'overwritten by step 2.1.1.1',
            'step 2': 'done',
            'step 2.1': 'done',
            'step 2.1.1': 'done',
            'step 2.1.1.1': 'done',
            'step 2.2': 'done',
            'step 3': 'done',
        }]
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    def test_start_all_levels(self):
        """
        Test all levels for MessageTaker.
        """
        for n in range(0, 4):
            expected = {}
            expected.update(self.tasks_results[n])
            self.tasker = MessageTasker(self.tasks, max_level=n)
            result = self.tasker.start(None, **{'step x': 'no effect'})
            self.assertDictEqual(result, expected)

    def test_start(self):
        """
        Test ml.common.message_tasker.MessageTasker::start
        """
        tests = [{
            "msg": {'test 0': 'message for test 0'},
        }, {
            "msg": {'step 2': 'done'},
        }, {
            "msg": {},
        }]
        tasks_result = {}
        tasks_result.update(self.tasks_results[3])
        self.tasker = MessageTasker(self.tasks, max_level=-3)

        for test in tests:
            expected = {}
            expected.update(test['msg'])
            expected.update(tasks_result)
            message = {}
            message.update(test['msg'])
            result1 = self.tasker.start(message)
            self.assertDictEqual(result1, expected)
            result2 = self.tasker.start(None)
            self.assertDictEqual(result2, expected)
        pass
