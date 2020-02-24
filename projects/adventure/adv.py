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
opp_dirs = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

'''
#First naive approach, dft, ignore cycles - got 998



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


def dead_end(test_room, dir, visited):
    visited.add(test_room.id)
    room = test_room.getRoomInDirection(dir)
    exits = room.getExits()
    viable_exits = [exit for exit in exits if room.getRoomInDirection(exit).id
                    not in visited]
    if len(viable_exits) == 0:
        return 1
    else:
        total = 1
        for new_dir in viable_exits:
            total += dead_end(room, new_dir, visited)
        return total

def traverse(options, path, room, graph):
    shortest = float("inf")
    for opt in options:
        possible_path = dead_end(room, opt, set())
        if possible_path < shortest:
            shortest = possible_path
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

traversalPath = make_path(player.currentRoom)

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
