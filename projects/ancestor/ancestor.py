#how do I do thse imports?
from graph import Graph
from util import Stack

def dfs_tracking(graph, starting_node):
    s = Stack()
    visited = set()
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
        if last_node not in visited:
            visited.add(last_node)
            children = graph.get_neighbors(last_node)
            for child in children:
                new_path = [*path] + [child]
                s.push(new_path)
    return ancestor if ancestor != float('inf') else -1


def earliest_ancestor(ancestors, starting_node):
    g = Graph()
    for p,c in ancestors:
        g.add_vertex(p)
        g.add_vertex(c)
        g.add_edge(c,p)
    return dfs_tracking(g, starting_node)

