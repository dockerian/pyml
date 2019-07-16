"""
# test_misc_graph_nodes.py

"""
import logging
import unittest

from ml.misc.graph_nodes import GraphNodes
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class GraphNodesTests(unittest.TestCase):
    """
    GraphNodesTests includes all unit tests for ml.misc.graph_nodes module
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

    def test_has_common_ancestor(self):
        graph_1 = GraphNodes([
            (1, 3), (2, 3), (3, 6), (5, 6),
            (5, 7), (4, 5), (4, 8), (8, 10)
        ])
        graph_2 = GraphNodes([
            (10, 2), (10, 5), (1, 3), (2, 3),
            (3, 4), (5, 6), (5, 7), (7, 8)
        ])
        tests = [{
            "graph": graph_1, "node1": 3, "node2": 8, "result": False,
        }, {
            "graph": graph_1, "node1": 5, "node2": 8, "result": True,
        }, {
            "graph": graph_1, "node1": 6, "node2": 8, "result": True,
        }, {
            "graph": graph_1, "node1": 1, "node2": 3, "result": False,
        }, {
            "graph": graph_1, "node1": 6, "node2": 5, "result": True,
        }, {
            "graph": graph_2, "node1": 4, "node2": 8, "result": True,
        }, {
            "graph": graph_2, "node1": 1, "node2": 6, "result": False,
        }]
        for test in tests:
            graph = test['graph']
            node1 = test['node1']
            node2 = test['node2']
            expected = test['result']
            msg = "Node {} and {} common ancestor: {} in\n{}\n{}".format(
                node1, node2, expected, graph.data, graph.children_map)
            result1 = graph.has_common_ancestor(node1, node2)
            result2 = graph.has_common_ancestor(node2, node1)
            self.assertEqual(result1, expected, msg)
            self.assertEqual(result2, expected, msg)
        pass

    def test_find_ancestor(self):
        graph = GraphNodes([
            (1, 3), (2, 3), (3, 6), (5, 6),
            (5, 7), (4, 5), (4, 8), (8, 10), (11, 2)
        ])
        tests = [{
            "node": 8, "ancestor": 4,
        }, {
            "node": 7, "ancestor": 4,
        }, {
            "node": 6, "ancestor": 11,
        }, {
            "node": 1, "ancestor": None,
        }]

        for test in tests:
            node = test['node']
            ancestor = test['ancestor']
            result = graph.find_ancestor(node)
            self.assertEqual(result, ancestor)
        pass

    def test_find_nodes(self):
        tests = [{
            "data": [
                (1, 3), (2, 3), (3, 6), (5, 6),
                (5, 7), (4, 5), (4, 8), (8, 10)
            ],
            "result": [
              [1, 2, 4],     # nodes with zero parents
              [5, 7, 8, 10]  # nodes with exactly one parent
            ]
        }]
        for test in tests:
            graph = GraphNodes(test['data'])
            result = graph.find_nodes()
            expected = test['result']
            self.assertListEqual(result, expected)
        pass
