from queue import PriorityQueue
import math
from glm import ivec2
import sys
from random import randint

from gdpc import __url__, Editor, Block, Rect
from gdpc.exceptions import BuildAreaNotSetError, InterfaceConnectionError
from gdpc.vector_tools import addY

# Define a function to calculate the Manhattan distance between two points
def manhattan_distance(point1, point2):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

# Implement the A* algorithm
def astar(graph, start, goal):
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
def generate_roads(locations, editor): 
    graph = {building_name: set() for building_name in locations}
    for building_name1 in locations:
        for building_name2 in locations:
            if building_name1 != building_name2:
                # Calculate the midpoint between the two buildings
                midpoint = ivec2((locations[building_name1].x + locations[building_name2].x) // 2,
                                (locations[building_name1].y + locations[building_name2].y) // 2)
                # Add the midpoint as a node in the graph
                graph[midpoint] = set()
                # Add edges between the buildings and the midpoint
                graph[building_name1].add(midpoint)
                graph[midpoint].add(building_name1)
                graph[building_name2].add(midpoint)
                graph[midpoint].add(building_name2)

    # Calculate and place roads
    for building_name1 in locations:
        for building_name2 in locations:
            if building_name1 != building_name2:
                path = astar(graph, building_name1, building_name2)
                if path:
                    # Place road blocks along the path
                    for point in path:
                        # Adjust this to place road blocks in Minecraft
                        editor.placeBlock((point.x, 0, point.y), Block("road"))  
    print("Roads generated successfully.")

# Call the function to generate roads
building_locations = generate_settlement()
print(building_locations)
generate_roads(building_locations)
