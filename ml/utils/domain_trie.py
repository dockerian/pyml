"""
DomainTrie class, as a data structure example.
"""


class DomainTrie(object):
    """
    DomainTrie is a trie-based domains list, being used to quickly check if
    a domain, or part of its hostnames, is a member of the domains list.
    """

    def __init__(self, domains):
        self._trie = DomainTrie._make_tree(domains)

    def __contains__(self, domain):
        """
        Check if a domain is in the DomainTrie.

        @param domain: A dot separated domain.
        @return boolean: True if domain is in the trie; otherwise, False.
        """
        parts = [part for part in domain.split('.')[::-1] if part != '']
        res = False
        ref = self._trie
        for part in parts:
            if part in ref:
                ref = ref[part]
                if '' in ref:
                    res = True
                    break
            else:
                break
        return res

    def __iter__(self):
        for result in DomainTrie._walk(self._trie, []):
            yield result

    def __str__(self):
        result = []
        for domain in self:
            result.append(domain)
        return str(result)

    @staticmethod
    def _add_branch(domain, tree, idx=0):
        # BASE CASE: out of character to add to this branch
        if idx == len(domain):
            tree[''] = None
        else:
            if '' not in tree:
                domain_piece = domain[idx]
                if domain_piece in tree:
                    branch = tree[domain_piece]
                else:
                    branch = {}
                    tree[domain_piece] = branch
                DomainTrie._add_branch(domain, branch, idx + 1)

    @staticmethod
    def _make_tree(domains):
        tree = {}
        for domain in domains:
            domain_pieces = [piece for piece in domain.split('.') if piece != '']
            if len(domain_pieces) > 1:
                DomainTrie._add_branch(domain_pieces[::-1], tree)
        return tree

    @staticmethod
    def _walk(tree, domain_pieces):
        result = []
        if '' in tree:
            result.append('.'.join(domain_pieces[::-1]))
        else:
            for piece in tree.keys():
                domain_pieces.append(piece)
                result.extend(DomainTrie._walk(tree[piece], domain_pieces))
                domain_pieces.pop()
        return result
