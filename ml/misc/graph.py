"""
ml/misc/graph.py
@see https://www.geeksforgeeks.org/top-10-algorithms-in-interview-questions/
"""
from collections import defaultdict


class Graph:
    """
    Graph class represents a directed graph using adjacency list representation.
    """
    def __init__(self):
        """
        Graph constructor
        """
        # default dictionary to store graph
        self.graph = defaultdict(list)

    def _dfs_recursive(self, p, visited, results):
        # mark the current node as visited and append to results
        visited[p] = True
        results.append(p)
        # for all the vertices adjacent to this vertex
        for v in self.graph[p]:
            if visited[v] is False:
                self._dfs_recursive(v, visited, results)

    def add_edge(self, s, e):
        """
        Add an edge to graph.
        """
        self.graph[s].append(e)

    def get_bfs(self, s):
        """
        Return BFS (Breadth First Search) paths.
        """
        # create a queue for BFS
        queue = []
        # mark all the vertices as not visited
        visited = [False] * (len(self.graph))
        # mark the start node as visited and enqueue it
        visited[s] = True
        queue.append(s)
        results = []

        while queue:
            # dequeue a vertex from queue and append to results.
            p = queue.pop(0)
            results.append(p)
            # get all adjacent vertices of the dequeued vertex s,
            # and for any unvisited adjacent, mark it visited and enqueue it.
            for v in self.graph[p]:
                if visited[v] is False:
                    visited[v] = True
                    queue.append(v)

        return results

    def get_dfs(self, s):
        """
        Return DFS (Depth First Search) paths.
        """
        results = []
        # mark all the vertices as not visited
        visited = [False] * (len(self.graph))
        self._dfs_recursive(s, visited, results)
        return results
