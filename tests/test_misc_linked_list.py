"""
# test_misc_link_list.py

"""
import logging
import os
import unittest

from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class LinkedListTests(unittest.TestCase):
    """
    LinkedListTests includes all unit tests for ml.misc.linked_list module
    """
    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def setUp(self):
        """setup for test"""
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.repo_path = os.path.dirname(self.test_path)
        self.proj_path = os.path.join(self.repo_path, "ml")
        self.base_path = os.path.join(self.repo_path, "ml", "misc")
        self.data_path = os.path.join(self.repo_path, "ml", "misc", "datasets")
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    def build_linked_list(self, items):
        head, next = None, None
        for item in items:
            item['next'] = None
            if next is None:
                head = item
            else:
                next['next'] = item
            next = item
        return head, next

    def test__init__(self):
        """
        test ml.misc.linked_list :: LinkedList :: __init__
        :return:
        """
        from ml.misc.linked_list import LinkedList
        tests = [{
            "head": {'data': 9, 'next': {'data': 88.5, 'next': {'data': -773, 'next': None}}},
            "my_list": [9, 88.5, -773],
        }, {
            "head": {'data': -9, 'next': {'data': 3.1415926, 'next': {'data': 'string', 'next': None}}},
            "my_list": [-9, 3.1415926, 'string'],
        }, {
            "head": {'data': None, 'next': {'data': {'launch': 'bread'}, 'next': {'data': 'string', 'next': None}}},
            "my_list": [None, {'launch': 'bread'}, 'string'],
        }, {
            "head": {'data': 7, 'next': None},
            "my_list": [7],
        }, {
            "head": None,
            "my_list": [],
        }, {
            "head": None,
            "my_list": None,
        }, {
            "head": None,
            "my_list": 5,
        }]
        for test in tests:
            my_list = test['my_list']
            expected = test['head']
            obj = LinkedList(my_list)
            if isinstance(expected, dict):
                self.assertDictEqual(obj.head, expected)
            else:
                self.assertIsNone(obj.head)

    def test_add(self):
        """
        test ml.misc.linked_list :: LinkedList :: add
        :return:
        """
        from ml.misc.linked_list import LinkedList
        tests = [{
            "result": {'data': 'add', 'next': {'data': 'string', 'next': None}},
            "head": {'data': 3.14, 'next': {'data': 'add', 'next': {'data': 'string', 'next': None}}},
            "my_list": [3.14, 'string'],
            "item": 'add',
            "position": 1,
        }, {
            "result": {'data': -87.345, 'next': {'data': -3.14, 'next': {'data': ['data', 'next'], 'next': None}}},
            "head": {'data': -87.345, 'next': {'data': -3.14, 'next': {'data': ['data', 'next'], 'next': None}}},
            "my_list": [-3.14, ['data', 'next']],
            "item": -87.345,
            "position": 0,
        }, {
            "result": {'data': {0}, 'next': None},
            "head": {'data': -3.14, 'next': {'data': {'data': 9, 'next': None}, 'next': {'data': {0}, 'next': None}}},
            "my_list": [-3.14, {'data': 9, "next": None}],
            "item": {0},
            "position": 9999,
        }, {
            "result": {'data': None, 'next': {'data': 9, 'next': None}},
            "head": {'data': None, 'next': {'data': 9, 'next': None}},
            "my_list": [9],
            "item": None,
            "position": -6,
        }, {
            "result": {'data': [1, 2, 99, 'only list'], 'next': None},
            "head": {'data': [1, 2, 99, 'only list'], 'next': None},
            "my_list": 18,
            "item": [1, 2, 99, 'only list'],
            "position": -99,
        }, {
            "result": {'data': [], 'next': None},
            "head": {'data': [], 'next': None},
            "my_list": None,
            "item": [],
            "position": 365,
        }, {
            "result": None,
            "head": {'data': 3.14, 'next': {'data': 'string', 'next': None}},
            "my_list": [3.14, 'string'],
            "item": 'add',
            "position": 9.93,
        }, {
            "result": None,
            "head": {'data': 3.14, 'next': {'data': 'string', 'next': None}},
            "my_list": [3.14, 'string'],
            "item": 'add',
            "position": int,
        }, {
            "result": None,
            "head": {'data': 3.14, 'next': {'data': 'string', 'next': None}},
            "my_list": [3.14, 'string'],
            "item": 'add',
            "position": 'string',
        }, {
            "result": None,
            "head": {'data': 3.14, 'next': {'data': 'string', 'next': None}},
            "my_list": [3.14, 'string'],
            "item": 'add',
            "position": [1, 2, 5, 9],
        }, {
            "result": None,
            "head": {'data': 3.14, 'next': {'data': 'string', 'next': None}},
            "my_list": [3.14, 'string'],
            "item": 'add',
            "position": {'2': 2, '3': 3},
        }]
        for test in tests:
            my_list = test['my_list']
            expected_head = test['head']
            input_item = test['item']
            position = test['position']
            expected = test['result']
            obj = LinkedList(my_list)
            result = obj.add(input_item, position)
            self.assertDictEqual(obj.head, expected_head)
            self.assertEqual(result, expected)

    def test_append(self):
        """
        test ml.misc.linked_list :: LinkedList :: append
        :return:
        """
        from ml.misc.linked_list import LinkedList
        tests = [{
            "head": {'data': 9, 'next': {'data': 88.5, 'next': {'data': -773, 'next': {'data': -39.9, 'next': None}}}},
            "my_list": [9, 88.5, -773],
            "append_item": -39.9,
        }, {
            "head": {'data': 3.1415926, 'next': {'data': 'string', 'next': {'data': 'string2', 'next': None}}},
            "my_list": [3.1415926, 'string'],
            "append_item": 'string2',
        }, {
            "head": {'data': {'launch': 'bread'}, 'next': {'data': None, 'next': {'data': [1, 2, 3, 4], 'next': None}}},
            "my_list": [{'launch': 'bread'}, None],
            "append_item": [1, 2, 3, 4],
        }, {
            "head": {'data': 7, 'next': {'data': [], 'next': None}},
            "my_list": [7],
            "append_item": [],
        }, {
            "head": {'data': 7.77, 'next': None},
            "my_list": [],
            "append_item": 7.77
        }, {
            "head": {'data': None, 'next': None},
            "my_list": None,
            "append_item": None,
        }, {
            "head": {'data': 'string', 'next': None},
            "my_list": 5,
            "append_item": 'string'
        }, {
            "head": {'data': {'data': None, 'next': None}, 'next': None},
            "my_list": None,
            "append_item": {'data': None, 'next': None},
        }]
        for test in tests:
            my_list = test['my_list']
            expected = test['head']
            input_item = test['append_item']
            obj = LinkedList(my_list)
            obj.append(input_item)
            if isinstance(expected, dict):
                self.assertDictEqual(obj.head, expected)
            else:
                self.assertIsNone(obj.head)

    def test_check_circular_link(self):
        """
        test ml.misc.linked_list :: LinkedList :: check_circular_link
        :return:
        """
        from ml.misc.linked_list import LinkedList

        # test True
        a = {'data': 99, 'next': None}
        b = {'data': 'string', 'next': None}
        c = {'data': [], 'next': a}
        a['next'] = b
        b['next'] = c
        d = {'data': 1, 'next': {'data': None, 'next': None}}
        e = {'data': 'pie', 'next': d}
        d['next']['next'] = e
        tests_true = [{
            "my_linked": a,
        }, {
            "my_linked": b,
        }, {
            "my_linked": c,
        }, {
            "my_linked": d,
        }, {
            "my_linked": e,
        }]
        for test in tests_true:
            my_linked = test["my_linked"]
            obj = LinkedList([])
            obj.head = my_linked
            result = obj.check_circular_link()
            self.assertTrue(result)

        # test False
        tests = [{
            "my_list": [9, 88.5, -773],
        }, {
            "my_list": [-9, 3.1415926, 'string'],
        }, {
            "my_list": [None, {'launch': 'bread'}, 'string'],
        }, {
            "my_list": [7],
        }]
        for test in tests:
            my_list = test['my_list']
            obj = LinkedList(my_list)
            result = obj.check_circular_link()
            self.assertFalse(result)
        # exception check
        tests_ex = [{
            "my_list": 9.93,
        }, {
            "my_list": int,
        }, {
            "my_list": '35',
        }, {
            "my_list": [],
        }]
        for test in tests_ex:
            my_list = test['my_list']
            obj = LinkedList(my_list)
            result = obj.check_circular_link()
            self.assertIsNone(result)

    def test_delete(self):
        """
        test ml.misc.linked_list :: linkedLists :: delete
        :return:
        """
        from ml.misc.linked_list import LinkedList
        tests = [{
            "head": {'data': 3.14, 'next': {'data': 1001, 'next': None}},
            "my_list": [3.14, 1001, 'string'],
            "position": 2,
            "result": {'data': 'string', 'next': None},
        }, {
            "head": {'data': ['data', 'next'], 'next': None},
            "my_list": [-3.14, ['data', 'next']],
            "position": 0,
            "result": {'data': -3.14, 'next': None},
        }, {
            "head": {'data': -3.14, 'next': None},
            "my_list": [-3.14, {'data': 9, "next": None}],
            "position": 9999,
            "result": {'data': {'data': 9, "next": None}, 'next': None},
        }, {
            "head": None,
            "my_list": [9],
            "position": -6,
            "result": {'data': 9, 'next': None},
        }, {
            "head": None,
            "my_list": 18,
            "position": -99,
            "result": None,
        }, {
            "head": None,
            "my_list": None,
            "position": 365,
            "result": None,
        }]
        for test in tests:
            my_list = test['my_list']
            print(my_list)
            expected = test['head']
            position = test['position']
            expected_return = test['result']
            obj = LinkedList(my_list)
            return_result = obj.delete(position)
            if isinstance(expected, dict):
                self.assertDictEqual(obj.head, expected)
            else:
                self.assertIsNone(obj.head)
            if isinstance(expected_return, dict):
                self.assertDictEqual(return_result, expected_return)
            else:
                self.assertIsNone(return_result)

        # exception check
        tests_ex = [{
            "position": 9.93,
        }, {
            "position": int,
        }, {
            "position": '35',
        }, {
            "position": [1, 8, 17],
        }]
        for test in tests_ex:
            my_list = [1, 2, 3, 4]
            position = test['position']
            obj = LinkedList(my_list)
            with self.assertRaises(TypeError):
                obj.delete(position)

    def test_find_middle_item(self):
        """
        test ml.misc.linked_list :: LinkedList :: find_middle_item
        :return:
        """
        from ml.misc.linked_list import LinkedList
        tests = [{
            "result": {'data': 1001, 'next': {'data': 'string', 'next': None}},
            "my_list": [3.14, 1001, 'string'],
        }, {
            "result": {'data': ['data', 'next'], 'next': None},
            "my_list": [-3.14, ['data', 'next']],
        }, {
            "result": {'data': {'data': 9, 'next': None}, 'next': None},
            "my_list": [-3.14, {'data': 9, "next": None}],
        }, {
            "result": {'data': -564,
                       'next': {'data': 'string',
                                'next': {'data': ['list', '2'], 'next': {'data': {'data': 2}, 'next': None}}}},
            "my_list": [None, 0, 839842, 1995, -564, 'string', ['list', '2'], {'data': 2}]
        }, {
            "result": {'data': 9, 'next': None},
            "my_list": [9],
        }, {
            "result": None,
            "my_list": 18,
        }, {
            "result": None,
            "my_list": None,
        }, {
            "result": None,
            "my_list": []
        }]
        for test in tests:
            my_list = test['my_list']
            expected = test['result']
            obj = LinkedList(my_list)
            result = obj.find_middle_item()
            if expected is None:
                self.assertIsNone(result)
            else:
                self.assertDictEqual(result, expected)

    def test_fix(self):
        """
        test ml.misc.linked_list :: LinkedList :: fix
        @return:
        """
        from ml.misc.linked_list import LinkedList
        # circular a
        a = {'data': 'string', 'next': None}
        b = {'data': 0, 'next': None}
        c = {'data': 987, 'next': a}
        a['next'] = b
        b['next'] = c

        # circular d
        d = {'data': ['just list', 's'], 'next': None}
        e = {'data': 3.1415926, 'next': d}
        d['next'] = e

        tests = [{
            "head": {'data': 'string', 'next': {'data': 0, 'next': {'data': 987, 'next': None}}},
            "link": a,
        }, {
            "head": {'data': ['just list', 's'], 'next':{'data': 3.1415926, 'next': None}},
            "link": d,
        }, {
            "head": {'data': 0, "next": {'data': None, 'next': {'data': {"data": 'fake link'}, 'next': None}}},
            "link": {'data': 0, "next": {'data': None, 'next': {'data': {"data": 'fake link'}, 'next': None}}}
        }, {
            "head": {'data': 'only one ', 'next': None},
            "link": {'data': 'only one ', 'next': None},
        }, {
            "head": {'data': -1, 'next': {'data': [1, 1995, -15], 'next': None}},
            "link": {'data': -1, 'next': {'data': [1, 1995, -15], 'next': None}},
        }, {
            "head": None,
            "link": None,
        }]
        for test in tests:
            my_link = test["link"]
            expected_head = test["head"]
            obj = LinkedList([])
            obj.head = my_link
            obj.fix_circular_link()
            if expected_head is None:
                self.assertIsNone(obj.head)
            else:
                self.assertDictEqual(obj.head, expected_head)

    def test_get_circular_link_item(self):
        """
        test ml.misc.linked_list :: linkedList :: get_circular_link_item
        @return:
        """
        from ml.misc.linked_list import LinkedList

        # circular a
        a = {'data': 'string', 'next': None}
        b = {'data': 0, 'next': None}
        c = {'data': 987, 'next': a}
        a['next'] = b
        b['next'] = c

        # circular d
        d = {'data': ['just list', 's'], 'next': None}
        e = {'data': 3.1415926, 'next': d}
        d['next'] = e

        tests = [{
            "result": c,
            "link": a,
        }, {
            "result": e,
            "link": d,
        }, {
            "result": None,
            "link": {'data': 0, "next": {'data': None, 'next': {'data': {"data": 'fake link'}, 'next': None}}}
        }, {
            "result": None,
            "link": {'data': 'only one ', 'next': None},
        }, {
            "result": None,
            "link": {'data': -1, 'next': {'data': [1, 1995, -15], 'next': None}},
        }, {
            "result": None,
            "link": None,
        }]
        for test in tests:
            my_link = test['link']
            expected = test['result']
            obj = LinkedList([])
            obj.head = my_link
            result = obj.get_circular_link_item()
            if expected is None:
                self.assertIsNone(result)
            else:
                self.assertEqual(result, expected)

    def test_get_circular_link_item_more(self):
        from ml.misc.linked_list import LinkedList
        a = {'data': 'AAA'}
        b = {'data': 'BBBB'}
        c = {'data': 'c3'}
        d = {'data': 'ddddddd'}
        e = {'data': 'e'}

        tests = [{
            'items': [a, b, c], 'cyclic_to': b
        }, {
            'items': [a, b, c, d], 'cyclic_to': a
        }, {
            'items': [a, b, c, d, e], 'cyclic_to': c
        }, {
            'items': [a, b, c, d, e], 'cyclic_to': e
        }]

        for test in tests:
            items = test.get('items')
            cyclic_to = test.get('cyclic_to')
            head, tail = self.build_linked_list(items)
            tail['next'] = cyclic_to
            a = LinkedList()
            a.head = head
            result = a.get_circular_link_item()
            v1 = result['data'] if result else None
            v2 = tail['data'] if tail else None
            msg = 'result.data = {}\n  tail.data = {}'.format(v1, v2)
            self.assertEqual(result, tail, msg)

    def test_reverse(self):
        """
        test ml.misc.LinkedList :: LinkedList :: reverse
        :return:
        """
        from ml.misc.linked_list import LinkedList
        tests = [{
            "head": {'data': -773, 'next': {'data': 88.5, 'next': {'data': 9, 'next': None}}},
            "my_list": [9, 88.5, -773],
        }, {
            "head": {'data': 'string', 'next': {'data': 3.1415926, 'next': {'data': -9, 'next': None}}},
            "my_list": [-9, 3.1415926, 'string'],
        }, {
            "head": {'data': 'string', 'next': {'data': {'launch': 'bread'}, 'next': {'data': None, 'next': None}}},
            "my_list": [None, {'launch': 'bread'}, 'string'],
        }, {
            "head": {'data': 7, 'next': None},
            "my_list": [7],
        }, {
            "head": None,
            "my_list": [],
        }, {
            "head": None,
            "my_list": None,
        }, {
            "head": None,
            "my_list": 5,
        }]
        for test in tests:
            my_list = test['my_list']
            expected = test['head']
            obj = LinkedList(my_list)
            obj.reverse()
            if isinstance(expected, dict):
                self.assertDictEqual(obj.head, expected)
            else:
                self.assertIsNone(obj.head)

    def test_to_list(self):
        """
        test ml.misc.linked_list :: LinkedList :: to_list
        :return:
        """
        from ml.misc.linked_list import LinkedList
        tests = [{
            "result": [9, 88.5, -773],
            "my_list": [9, 88.5, -773],
        }, {
            "result": [-9, 3.1415926, 'string'],
            "my_list": [-9, 3.1415926, 'string'],
        }, {
            "result": [None, {'launch': 'bread'}, 'string'],
            "my_list": [None, {'launch': 'bread'}, 'string'],
        }, {
            "result": [7],
            "my_list": [7],
        }, {
            "result": None,
            "my_list": [],
        }, {
            "result": None,
            "my_list": None,
        }, {
            "result": None,
            "my_list": 5,
        }]
        for test in tests:
            my_list = test['my_list']
            expected = test['result']
            obj = LinkedList(my_list)
            result = obj.to_list()
            if isinstance(expected, list):
                self.assertListEqual(result, expected)
            else:
                self.assertIsNone(result)
