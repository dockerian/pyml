r"""
misc/graph_nodes.py

Some input data, formatted as a list of (parent, child) pairs, describes a
graph of relationships between parents and children over multiple generations.
Each individual node is assigned a unique integer identifier.


1. Write a function that takes this data as input and returns two collections:
   one containing all individuals with zero known parents, and one containing
   all individuals with exactly one known parent.

   For example, in this diagram, 3 is a child of 1 and 2, and 5 is a child of 4:

        1   2   4
         \ /   / \
          3   5   8
           \ / \   \
            6   7   10
    ```
    # Sample input/output (pseudodata):

    data1_graph = [
        (1, 3), (2, 3), (3, 6), (5, 6),
        (5, 7), (4, 5), (4, 8), (8, 10)
    ]

    find_nodes(data1_graph) => [
      [1, 2, 4],    // Individuals with zero parents
      [5, 7, 8, 10] // Individuals with exactly one parent
    ]
    ```

2. Write a function that takes the graph, as well as two node IDs in the dataset
   and return true if and only if they share at least one ancestor.

    ```
    # Output example:

    has_common_ancestor(data1_graph, 3, 8) # => false
    has_common_ancestor(data1_graph, 5, 8) # => true
    has_common_ancestor(data1_graph, 6, 8) # => true
    has_common_ancestor(data1_graph, 1, 3) # => false
    has_common_ancestor(data1_graph, 6, 5) # => true

    # Additional example: In this diagram, 4 and 8 have a common ancestor of 10.

              10
             /  \
        1   2    5
         \ /    / \
          3    6   7
           \        \
            4        8

    data2_graph = [
        (10, 2), (10, 5), (1, 3), (2, 3),
        (3, 4), (5, 6), (5, 7), (7, 8)
    ]

    has_common_ancestor(data2_graph, 4, 8) # => true
    has_common_ancestor(data2_graph, 1, 6) # => false
    ```

3. Write a function that, for a given individual node in the dataset, return the
   earliest known ancestor -- the one at the farthest distance from the input
   node. If there is more than one ancestor tied for "earliest", return any one
   of them. If the input individual has no parents, return null (None).

    ```
    # Sample input and output:

          11
           \
        1   2   4
         \ /   / \
          3   5   8
           \ / \   \
            6   7   10

    data3_graph = [
        (1, 3), (2, 3), (3, 6), (5, 6),
        (5, 7), (4, 5), (4, 8), (8, 10), (11, 2)
    ]

    find_ancestor(data3_graph, 8) # => 4
    find_ancestor(data3_graph, 7) # => 4
    find_ancestor(data3_graph, 6) # => 11
    find_ancestor(data3_graph, 1) # => None
    ```
"""


class GraphNodes:

    def __init__(self, data):
        self._build(data)
        self.data = data
        pass

    def _build(self, data: list) -> dict:
        self.children_map = {}
        for parent, child in data:
            if self.children_map.get(parent) is None:
                self.children_map[parent] = []
            if self.children_map.get(child):
                self.children_map[child].append(parent)
            else:
                self.children_map[child] = [parent]
        return self.children_map

    def _get_parents(self, node, depth=0):
        results = []
        parents = self.children_map.get(node)
        if parents:
            for node in parents:
                results.append((node, depth))
            depth += 1
            for parent in parents:
                results.extend(self._get_parents(parent, depth))
        return results

    def has_common_ancestor(self, node1, node2):
        set1 = set([p for p, v in self._get_parents(node1)])
        set2 = set([p for p, v in self._get_parents(node2)])
        result = set1.intersection(set2)
        return True if result else False

    def find_ancestor(self, node):
        parents = self._get_parents(node)
        depth = -1
        ancester = None
        for (node, length) in parents:
            if length > depth:
                ancester = node
                depth = length
        return ancester

    def find_nodes(self) -> list:
        no_parents = []
        one_parent = []
        for child in self.children_map:
            parents = self.children_map.get(child)
            if len(parents) == 0:
                no_parents.append(child)
            elif len(parents) == 1:
                one_parent.append(child)
        return [no_parents, one_parent]
