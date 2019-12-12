from room import Room
from player import Player
from world import World
from roomGraphs import roomGraph
import random
from collections import deque

# Load world
world = World()

world.loadGraph(roomGraph)

# UNCOMMENT TO VIEW MAP
world.printRooms()

player = Player("Name", world.startingRoom)
opp_dirs = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w', 'start': 'all'}

'''
#First naive approach, dft, ignore cycles



def traverse(room, visited=None):
    if visited is None:
        visited = set()
    path = []

    visited.add(room.id)
    for dir in room.getExits():
        new_room = room.getRoomInDirection(dir)
        if new_room.id not in visited:
            new_room_path = traverse(new_room, visited)
            if new_room_path:
                local_path = [dir] + new_room_path + [opp_dirs[dir]]
            else:
                local_path = [dir, opp_dirs[dir]]
            path = path + local_path
    return path
'''


# Fill this out
def direction_conversion(path, graph):
    directions = []
    while len(path) > 1:
        room = path.pop()
        next_room = path[-1]
        for dir in graph[room.id]:
            if graph[room.id][dir] == next_room.id:
                directions.append(opp_dirs[dir])
    directions.reverse()
    return directions


def bfs(start_room, graph):
    bfs_visited = set()
    q = deque()
    q.append([start_room])
    while len(q) > 0:
        path = q.popleft()
        room = path[-1]
        if find_options(room, graph):
            return direction_conversion(path, graph), room
        if room.id not in bfs_visited:
            bfs_visited.add(room.id)
            for dir in graph[room.id]:
                path_copy = path.copy()
                new_room = room.getRoomInDirection(dir)
                path_copy.append(new_room)
                q.append(path_copy)


def store_room(room, graph):
    if room.id not in graph:
        graph[room.id] = {}
        for dir in room.getExits():
            graph[room.id][dir] = '?'


def find_options(room, graph):
    options = []
    for dir in graph[room.id]:
        if graph[room.id][dir] == '?':
            options.append(dir)
    return options


def dead_end(test_room, dir):
    room = test_room.getRoomInDirection(dir)
    exits = room.getExits()
    if len(exits) == 1:
        return True


def traverse(options, path, room, graph):
    rand_index = random.randint(0, len(options) - 1)
    dir = options[rand_index]
    for opt in options:
        if dead_end(room, opt):
            dir = opt
    path.append(dir)
    new_room = room.getRoomInDirection(dir)
    graph[room.id][dir] = new_room.id
    store_room(new_room, graph)
    graph[new_room.id][opp_dirs[dir]] = room.id
    return new_room


def make_path(starting_room):
    graph = {}
    room = starting_room
    path = []
    while len(graph) < len(roomGraph):
        store_room(room, graph)
        options = find_options(room, graph)
        if options:
            room = traverse(options, path, room, graph)
        else:
            bfs_result = bfs(room, graph)
            next_path = bfs_result[0]
            room = bfs_result[1]
            path = path + next_path
    return path


def shortest_path(start):
    shortest_length = 1000
    path = []
    for i in range(5000000):
        if i % 50000 == 0 and i != 0:
            print(i, shortest_length)
        attempt = make_path(start)
        if len(attempt) < shortest_length:
            shortest_length = len(attempt)
            path = attempt
            print(i, shortest_length)
            if shortest_length < 930:
                print(path)
    return path


traversalPath = shortest_path(player.currentRoom)
print(traversalPath)

# TRAVERSAL TEST
visited_rooms = set()
player.currentRoom = world.startingRoom
visited_rooms.add(player.currentRoom)

for move in traversalPath:
    player.travel(move)
    visited_rooms.add(player.currentRoom)

if len(visited_rooms) == len(roomGraph):
    print(
        f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")
