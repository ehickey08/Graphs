import sys
sys.path.append('..')
from graph.util import Stack

def get_neighbors(x, y, matrix):
    neighbors = []
    if y > 0 and matrix[y-1][x] == 1:
        neighbors.append((x, y-1))
    if y<len(matrix) -1 and matrix[y+1][x] == 1:
        neighbors.append((x, y+1))
    if x > 0 and matrix[y][x - 1] == 1:
        neighbors.append((x-1 , y))
    if x <len(matrix[0]) -1 and matrix[y][x + 1] == 1:
        neighbors.append((x + 1, y))
    return neighbors

def dft(start_x, start_y, visited, matrix):
    s = Stack()
    s.push((start_x, start_y))

    while s.size() > 0:
        v = s.pop()
        x = v[0]
        y = v[1]

        if not visited[y][x]:
            visited[y][x] = True
            for neighbor in get_neighbors(x, y, matrix):
                s.push(neighbor)
    return visited

def island_counter(matrix):
    matrix_height = len(matrix)
    matrix_width = len(matrix[0])
    visited = []
    counter = 0
    for i in range(matrix_height):
        visited.append([False] * matrix_width)
    for x in range(matrix_width):
        for y in range(matrix_height):
            if not visited[y][x]:
                if matrix[y][x] == 1:
                    visited = dft(x, y, visited, matrix)
                    counter += 1
    return counter




small_islands = [[0, 1, 0, 1, 0],
                 [1, 1, 0, 1, 1],
                 [0, 0, 1, 0, 0],
                 [0, 0, 1, 0, 0],
                 [1, 1, 0, 0, 0]]

print(island_counter(small_islands))