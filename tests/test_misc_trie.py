"""
# test_misc_trie.py

"""
import logging
import os
import unittest

from ml.misc.trie import Trie
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class TrieTests(unittest.TestCase):
    """
    TrieTests includes all unit tests for ml.misc.trie module
    """
    @classmethod
    def load_dict(cls, dict_path):
        results = []
        if os.path.isfile(dict_path):
            with open(dict_path, 'rt') as fh:
                for word in fh:
                    results.append(word.strip())
        return results

    @classmethod
    def setUpClass(cls):
        """setup for all tests"""
        cls.test_path = os.path.dirname(os.path.realpath(__file__))
        cls.data_path = os.path.join(cls.test_path, 'data')
        cls.dict_1000 = os.path.join(cls.data_path, 'en-1000.dict')
        cls.dict_4000 = os.path.join(cls.data_path, 'en-4000.dict')
        cls.dict_test = os.path.join(cls.data_path, 'trie_test.dict')
        cls.data_1000 = cls.load_dict(cls.dict_1000)
        cls.data_4000 = cls.load_dict(cls.dict_4000)
        cls.data_test = cls.load_dict(cls.dict_test)
        cls.trie_1000 = Trie(cls.data_1000, 'data_1000')
        cls.trie_4000 = Trie(cls.data_4000, 'data_4000')
        cls.trie_test = Trie(cls.data_test, 'data_test')
        pass

    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    def test_build(self):
        """
        test.ml.misc.trie :: Trie :: extend and list
        """
        list1 = ['abc', 'word1', 'word2', 'word3']
        list2 = ['word1', 'word2.71', 'word3.14', 'word4', 'abc']

        trie1 = Trie(list1)
        self.assertEqual(str(trie1), '\n'.join(list1))
        self.assertListEqual(trie1.list(), list1)
        self.assertTrue('word2' in trie1)
        trie2 = Trie(list2)
        self.assertEqual(str(trie2), '\n'.join(list2))
        self.assertListEqual(trie2.list(), list2)
        self.assertFalse('word2' in trie2)

        trie2.extend(list1)
        result = trie2.list()
        result.sort()
        expected = list(set(list1+list2))
        expected.sort()
        self.assertListEqual(result, expected)
        pass

    def test_get_matches(self):
        """
        test.ml.misc.trie :: Trie :: get_matches
        """
        trie = TrieTests.trie_test
        tests = [{
            "prefix": "al", "words": [
                "album", "all", "allow", "almost", "along", "already", "also", "although", "always",
            ]
        }, {
            "prefix": "cha", "words": [
                "chance", "change", "changed",
            ]
        }, {
            "prefix": "play", "words": [
                "play", "played", "playing",
            ]
        }]
        for idx, test in enumerate(tests):
            prefix = test.get('prefix')
            expected = test.get('words', [])
            result = trie.get_matches(prefix)
            msg = "should find by prefix '%s' => %s" % (prefix, expected)
            self.assertListEqual(result, expected, msg)
        pass

    def test_has(self):
        """
        test.ml.misc.trie :: Trie :: has
        """
        tests = [{
            "trie": TrieTests.trie_1000, "word": "xyz", "has": False,
        }, {
            "trie": TrieTests.trie_4000, "word": "xyz", "has": False,
        }, {
            "trie": TrieTests.trie_test, "word": "xyz", "has": False,
        }, {
            "trie": TrieTests.trie_test, "word": "subject", "has": True,
        }, {
            "trie": TrieTests.trie_test, "word": "", "has": False,
        }]
        for idx, test in enumerate(tests):
            trie = test.get('trie')
            word = test.get('word')
            expected = test.get('has', False)
            result = trie.has(word)
            msg = "should find word '%s' in %s" % (word, trie.name)
            self.assertEqual(result, expected, msg)
        pass

    def test_has_prefix(self):
        """
        test.ml.misc.trie :: Trie :: has_prefix
        """
        tests = [{
            "trie": TrieTests.trie_1000, "word": "xyz", "has": False,
        }, {
            "trie": TrieTests.trie_4000, "word": "xyz", "has": False,
        }, {
            "trie": TrieTests.trie_test, "word": "xyz", "has": False,
        }, {
            "trie": TrieTests.trie_test, "word": "al", "has": True,
        }, {
            "trie": TrieTests.trie_test, "word": "be", "has": True,
        }, {
            "trie": TrieTests.trie_test, "word": "", "has": False,
        }]
        for idx, test in enumerate(tests):
            trie = test.get('trie')
            word = test.get('word')
            expected = test.get('has', False)
            result = trie.has_prefix(word)
            msg = "should find word '%s' in %s" % (word, trie.name)
            self.assertEqual(result, expected, msg)
        pass
