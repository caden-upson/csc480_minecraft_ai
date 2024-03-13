from queue import PriorityQueue
import math
from glm import ivec2
import sys
from random import randint

from gdpc import __url__, Editor, Block, Rect
from gdpc.exceptions import BuildAreaNotSetError, InterfaceConnectionError
from gdpc.vector_tools import addY

import settlement


# Define a function to calculate the Manhattan distance between two points
def manhattan_distance(point1, point2):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

def calculate_connections(buildings, threshold):
    connections = {}
    for building1, coord1 in buildings.items():
        connections[building1] = []
        for building2, coord2 in buildings.items():
            if building1 != building2 and manhattan_distance(coord1._offset, coord2._offset) <= threshold:
                connections[building1].append(building2)
    return connections

def getY(build_area: Rect, editor=Editor): 
    foundation = build_area.centeredSubRect((1, 1))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    #ground height 
    height = heightmap[tuple((foundation.center) - foundation.offset)]
    return height 

# Implement the A* algorithm
def astar(graph, start, end, editor):
    # build_area is a rect(),

    # editor is editor
    height = getY(start)
    point = ()
    print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    open_set = PriorityQueue()
    open_set.put(start, 0)
    came_from = {}
    g_score = {node: math.inf for node in graph}
    g_score[start] = 0
    f_score = {node: math.inf for node in graph}
    f_score[start] = manhattan_distance(start, goal)

    while not open_set.empty():
        current = open_set.get()

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            print(path) 
            return path[::-1]

        for neighbor in graph[current]:
            tentative_g_score = g_score[current] + manhattan_distance(current, neighbor)
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)
                if neighbor not in open_set.queue:
                    open_set.put(neighbor, f_score[neighbor])
    return None

# Generate roads between buildings
'''
Creates a road network between the buildings 
TODO: After the settlement is created, pathfind 
Access the points by:
class Rect
    _offset: ivec2, where first coodinate is x, second is z 
    _size:   ivec2
locations: is a default dict holding items such as: {'cabin': Rect((1046, -245), (65, 65)), 'well': Rect((1014, -269), (65, 65)), 'tree': Rect((1022, -253), (65, 65)), 'pyramid': Rect((1022, -245), (65, 65)), 'hut': Rect((1046, -253), (65, 65))})
a point is the Rect's offset (x, z) , y should always be 
'''

# threshold_distance = 25 # Adjust this value as needed
buildings = settlement.generate_settlement()
# # Calculate connections dynamically based on threshold distance
print(buildings)
# connections = calculate_connections(buildings, threshold_distance)
# print('connections', connections)
