"""
ml/misc/trie.py
"""


class Trie:
    def __init__(self, words: list, name='trie'):
        self._root = {}
        _, self.count = Trie._build_tree(words, self._root)
        self.name = name
        pass

    def __contains__(self, word):
        found, node = self.has_match(word)
        return found and None in node

    def __iter__(self):
        for result in Trie._iterator(self._root):
            yield result

    def __str__(self):
        words = []
        for word in self:
            words.append(word)
        return '\n'.join(words)

    @staticmethod
    def _add_node(tree, word, index=0):
        if index >= len(word):
            # adding a special key (None) to indicate the end of a word
            tree[None] = '.'  # or tree[None] = word
            return
        char = word[index]
        node = tree.get(char, {})
        if node == {}:
            tree[char] = node
        Trie._add_node(node, word, index+1)
        pass

    @staticmethod
    def _build_tree(words: list, tree: dict={}):
        count = 0
        for v in words:
            value = v.strip()  # trimmed string value
            if len(value) > 0:
                # print('adding', value, 'to', tree)
                Trie._add_node(tree, value)
                count += 1
        return tree, count

    @staticmethod
    def _iterator(tree, chars=[], prefix=''):
        """
        List all words from specific tree node.
        """
        for key in tree:
            if key is not None:
                chars.append(key)
                for x in Trie._iterator(tree[key], chars, prefix):
                    yield x
                chars.pop()  # remove what has been processed
            else:
                suffix = ''.join(chars) if len(chars) > 0 else ''
                complete_word = prefix + suffix
                if complete_word:
                    yield complete_word

    @staticmethod
    def _list(tree, chars=[], prefix=''):
        return list(Trie._iterator(tree, chars, prefix))

    def extend(self, words: list):
        _, count = Trie._build_tree(words, self._root)
        self.count += count
        pass

    def get_matches(self, prefix: str):
        results = []
        found, node = self.has_match(prefix)
        if found and node is not None:
            results.extend(Trie._iterator(node, [], prefix))
        return results

    def has(self, word):
        return self.__contains__(word)

    def has_match(self, prefix: str) -> (bool, dict):
        """
        Check if there is prefix in the trie list.
        """
        if not prefix:
            return False, None
        node = self._root
        for ch in prefix:
            tree = node.get(ch)
            if tree is None:  # cannot find sub-tree/node for the char
                return False, None
            node = tree
        return True, node

    def has_prefix(self, prefix):
        found, node = self.has_match(prefix)
        return found and node is not None

    def list(self):
        return Trie._list(self._root)
