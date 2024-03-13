from queue import PriorityQueue
import math
from glm import ivec2
import sys
from random import randint

from gdpc import __url__, Editor, Block, Rect
from gdpc.exceptions import BuildAreaNotSetError, InterfaceConnectionError
from gdpc.vector_tools import addY

import util
import math
from queue import PriorityQueue
import heapq
import math

def manhattan_distance_2d(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[2] - point2[2])

def neighbors(point):
    x, y, z = point
    return [(x+dx, y+dy, z+dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1) if not (dx == 0 and dy == 0 and dz == 0)]

def a_star(start, goal, forbidden):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance_2d(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in neighbors(current):
            if neighbor not in forbidden:
              tentative_g_score = g_score[current] + 1
              if tentative_g_score < g_score.get(neighbor, float('inf')):
                  came_from[neighbor] = current
                  g_score[neighbor] = tentative_g_score
                  f_score[neighbor] = tentative_g_score + manhattan_distance_2d(neighbor, goal)
                  heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


def get_all_forbidden(buildings):
    forbidden = set()
    for k, v in buildings.items():
        forbidden.update(get_forbidden(v, k))
    return forbidden
        
def get_forbidden(center, building):
    forbidden = set()
    sizes = {"cabin" : 11, "pyramid" : (5,3), "hut" : (7,3), "well" : (3,1)}
    if building == "cabin":
        center = (center[0]+1, center[1], center[2]+1)
        for x in range(7):
            for y in range(6):
                forbidden.add((center[0]+x,center[2]+y))
        center = (center[0]-5, center[1], center[2])
        for x in range(11):
            for y in range(6):
                forbidden.add((center[0]+x,center[2]+y))
    else:
      center = (center[0]-sizes[building][1], center[1], center[2]-sizes[building][1])
      for x in range(sizes[building][0]):
          for y in range(sizes[building][0]):
              forbidden.add((center[0]+x,center[2]+y))
    return forbidden
        
  
    


