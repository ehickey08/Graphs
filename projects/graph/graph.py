"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            if v1 in self.vertices:
                raise IndexError(f"{v2} is not a valid vertex in Graph")
            else:
                raise IndexError(f"{v1} is not a valid vertex in Graph")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        queue = Queue()
        visited = set()
        queue.enqueue(starting_vertex)

        while queue.size() > 0:
            node = queue.dequeue()
            if node not in visited:
                print(node)
                visited.add(node)
                neighbors = self.get_neighbors(node)
                for node in neighbors:
                    queue.enqueue(node)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        stack = Stack()
        visited = set()
        stack.push(starting_vertex)
        while stack.size() > 0:
            node = stack.pop()
            if node not in visited:
                print(node)
                visited.add(node)
                neighbors = self.get_neighbors(node)
                for node in neighbors:
                    stack.push(node)

    def dft_recursive(self, starting_vertex, visited=set()):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if starting_vertex not in visited:
            print(starting_vertex)
            visited.add(starting_vertex)
            neighbors = self.get_neighbors(starting_vertex)
            for node in neighbors:
                self.dft_recursive(node)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        queue = Queue()
        visited = set()
        queue.enqueue([starting_vertex])

        while queue.size() > 0:
            path = queue.dequeue()
            last_node = path[-1]
            if last_node == destination_vertex:
                return path
            if last_node not in visited:
                visited.add(last_node)
                neighbors = self.get_neighbors(last_node)
                for node in neighbors:
                    new_path = [*path] + [node]
                    queue.enqueue(new_path)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        stack = Stack()
        visited = set()
        stack.push([starting_vertex])

        while stack.size() > 0:
            path = stack.pop()
            last_node = path[-1]
            if last_node == destination_vertex:
                return path
            if last_node not in visited:
                visited.add(last_node)
                neighbors = self.get_neighbors(last_node)
                for node in neighbors:
                    new_path = [*path] + [node]
                    stack.push(new_path)

    def dfs_recursive(self, start, destination, path = [], visited=set()):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        final_path = None
        if len(path) == 0:
            path.append(start)
        last_node = path[-1]
        if last_node == destination:
            return path
        if last_node not in visited:
            visited.add(last_node)
            neighbors = self.get_neighbors(last_node)
            for node in neighbors:
                new_path = [*path] + [node]
                final_path = self.dfs_recursive(start, destination, new_path)
        return final_path



if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)
    print('bft end\n')

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    print('dft end\n')
    graph.dft_recursive(1)
    print('dft_recursive end\n')

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))
    print('bfs end\n')

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print('dfs end\n')
    print(graph.dfs_recursive(1, 6))
    print('dfs_recursive end\n')
