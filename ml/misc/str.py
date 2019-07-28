"""
ml/misc/string.py functions that are for interview practice
"""
import copy


def check_longest_common(s1: str, s2: str) -> str:
    """
    Find the longest common substring from 2 input strings.
    """
    s1_size = len(s1)
    s2_size = len(s2)
    if s1_size == 0 or s2_size == 0:
        return ''
    matrix = [[0 for x in range(s2_size + 1)] for y in range(s1_size + 1)]
    max_bound = None
    max_count = 0
    for i in range(s1_size):
        for j in range(s2_size):
            if s1[i] == s2[j]:
                count = matrix[i+1][j+1] = 1 if i == 0 or j == 0 else matrix[i][j] + 1
                max_count = max(count, max_count)
                if count == max_count:
                    max_bound = (i, j)
    i, j = max_bound
    idx_start, idx_end = (i+1) - max_count, (i+1)
    return s1[idx_start:idx_end]


def check_match_patterns(p: str, s: str, mapping={}):
    """
    Check if string, e.g. 'postmanpostman', matches a pattern, e.g. 'abab'.

    @param p: pattern string.
    @param s: substring or source input string.
    @param mapping: an internal dictionary (initialized as {}) that maps
        a character in p to a substring of s.
    @return: True if s matches p; otherwise, False.
    """
    # pattern is longer than provided string. impossible match.
    if len(p) > len(s):
        return False
    # both pattern and string ran out at the same time. yay
    if len(p) == 0 and len(s) == 0:
        # print('---- matched (%s, %s, %s)' % (p, s, mapping))
        return True
    # pattern ran out but not the string. boo
    if len(p) == 0:
        return False

    # current key we're considering
    key = p[0]
    # if key is already included in our mapping, check if s indeed
    # begins with the value of this key. if not, then we can't
    # continue with this particular set of mapping
    if key in mapping:
        mapped = mapping.get(key)
        if mapped and s.startswith(mapped):
            # print('key: %s, mapped: %s, mapping: %s' % (key, mapped, mapping))
            # print('---- checking (%s, %s) in mapping [%s]' % (p[1:], s[len(mapped):], mapping))
            return check_match_patterns(p[1:], s[len(mapped):], mapping)
        else:
            return False
    # else:
    # if key doesn't exist in our mapping, then we brute-forcely
    # guess all substrings of s to be the value of this key and
    # recursively call check_match_patterns on each map
    for i in range(1, len(s)):
        guess = s[:i]
        # this guess_mapping is very important. it allows us to
        # try different keys in the recursive calls w/o affecting
        # our original mapping
        guess_mapping = copy.copy(mapping)
        guess_mapping[key] = guess
        # print('%3d: guess mapping [%s] = %s' % (i, key, guess))
        # print('---- checking (%s, %s) in guess mapping [%s]' % (p[1:], s[len(guess):], guess_mapping))
        if check_match_patterns(p[1:], s[len(guess):], guess_mapping):
            # print('---- matched (%s, %s, %s)' % (p, s, mapping))
            return True

    return False
