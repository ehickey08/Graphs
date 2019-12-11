'''
This was my first approach before class using hte Graph class from day 1:
import sys
sys.path.append('..')

from graph.graph import Graph
from graph.util import Stack


def dfs_tracking(graph, starting_node):
    s = Stack()
    s.push([starting_node])
    longest_path = 2
    ancestor = float("inf")
    while s.size() > 0:
        path = s.pop()
        last_node = path[-1]
        if len(path) > longest_path:
            ancestor = last_node
            longest_path = len(path)
        if len(path) == longest_path and last_node < ancestor:
            ancestor = last_node
        children = graph.get_neighbors(last_node)
        if len(children) > 0:
            for child in children:
                new_path = [*path] + [child]
                s.push(new_path)
    return ancestor if ancestor != float('inf') else -1


def earliest_ancestor(ancestors, starting_node):
    g = Graph()
    for p, c in ancestors:
        g.add_vertex(p)
        g.add_vertex(c)
        g.add_edge(c, p)
    return dfs_tracking(g, starting_node)
'''

# Attempt two: solving like an interview problem
import sys
sys.path.append('..')

from graph.util import Stack

def get_parents(ancestors, starting_node):
    parents = []
    for p,c in ancestors:
        if c == starting_node:
            parents.append(p)
    return parents

def earliest_ancestor(ancestors, starting_node):
    s = Stack()
    s.push([starting_node])
    longest_path = 1
    ancestor = None
    while s.size() > 0:
        path = s.pop()
        v = path[-1]
        if len(path) > longest_path:
            longest_path = len(path)
            ancestor = v
        if len(path) == longest_path and ancestor:
            ancestor = v if v < ancestor else ancestor
        for p in get_parents(ancestors, v):
            path_copy = path.copy()
            path_copy.append(p)
            s.push(path_copy)
    return ancestor if ancestor else -1

