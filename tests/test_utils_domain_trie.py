"""
# test_domain_trie
"""
import ast
import unittest

from ml.utils.domain_trie import DomainTrie


class DomainTrieTests(unittest.TestCase):
    def test_domain_trie(self):
        domains = [
            '132.22.21.47',
            'xn--2342390.cn',
            'google.com',
            'test.google.com',
            'example.stuff'
        ]

        trie = DomainTrie(domains)
        self.assertIn('.goo.example.stuff', trie)
        self.assertIn('132.22.21.47', trie)
        self.assertIn('a.xn--2342390.cn', trie)
        self.assertIn('api.google.com', trie)
        self.assertIn('goo.example.stuff.', trie)
        self.assertIn('goo.example.stuff', trie)
        self.assertIn('google.com', trie)
        self.assertIn('test.google.com', trie)

        self.assertNotIn('133.22.21.47', trie)
        self.assertNotIn('googl.com', trie)
        self.assertNotIn('google.api.com', trie)
        self.assertNotIn('google.cn', trie)
        self.assertNotIn('stuff', trie)

        domains.remove('test.google.com')
        result = ast.literal_eval(str(trie))
        self.assertEqual(result, domains)
