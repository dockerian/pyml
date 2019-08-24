"""
DomainTrie class, as a data structure example.
"""
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class DomainTrie(object):
    """
    DomainTrie is a trie-based domains list, being used to quickly check if
    a domain, or part of its hostnames, is a member of the domains list.
    """

    def __init__(self, domains):
        self._trie = DomainTrie._build_tree(domains)

    def __contains__(self, domain):
        """
        Check if a domain is in the DomainTrie.

        @param domain: A dot separated domain.
        @return boolean: True if domain is in the trie; otherwise, False.
        """
        result = False
        parts = [part for part in domain.split('.')[::-1] if part != '']
        node = self._trie  # start from the trie root
        for part in parts:
            if part not in node:
                break
            node = node[part]
            if '.' in node:
                return True
        return result

    def __iter__(self):
        for result in DomainTrie._list(self._trie, []):
            yield result

    def __str__(self):
        result = []
        for domain in self:
            result.append(domain)
        return str(result)

    @staticmethod
    def _add_node(domain_pieces, tree, idx=0):
        """
        add specific level of domain part to the tree.
        """
        if idx >= len(domain_pieces):
            tree['.'] = None
            return
        # stop at "." because it is only building topper levels
        if "." not in tree:
            part = domain_pieces[idx]
            node = tree.get(part, {})
            if node == {}:
                tree[part] = node  # adding a new node
            DomainTrie._add_node(domain_pieces, node, idx + 1)

    @staticmethod
    def _build_tree(domains):
        tree = {}
        for domain in domains:
            d = domain.strip() if isinstance(domain, str) else ''
            domain_pieces = [piece for piece in d.split('.') if piece != '']
            if len(domain_pieces) > 1:
                DomainTrie._add_node(domain_pieces[::-1], tree)
            else:
                LOGGER.warn('Invalid domain: "%s"', domain)
        return tree

    @staticmethod
    def _list(tree, domain_pieces=[]):
        results = []
        if '.' in tree and len(domain_pieces) > 0:
            results.append('.'.join(domain_pieces[::-1]))
            return results
        for piece in tree.keys():
            if not piece == '.':
                domain_pieces.append(piece)
                results.extend(DomainTrie._list(tree[piece], domain_pieces))
                domain_pieces.pop()
        return results
