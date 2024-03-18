from gdpc import __url__, Editor
from util import placeDirtPath
import heapq

# a* algorithm to generate paths between two points
# heuristic: 2d manhattan distance from goal (y change not included)
# cost: cost to move to next point (includes y change)
def a_star(start, goal, forbidden, center):
    max_iterations = 100000
    iterations = 0
    print(f"Pathing from {start} to {goal}")
    open_set = []
    heapq.heappush(open_set, (0, start))
    closed_set = set()
    came_from = {}
    g_score = {start: 0}

    while open_set:
        iterations += 1
        if iterations >= max_iterations:
            return []
        _, current = heapq.heappop(open_set)

        if (current[0], current[2]) == (goal[0], goal[2]):
            path = []
            # Backtrack to start position
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        else:
            closed_set.add(current)
            for neighbor in neighbors(current):
                if (neighbor[0], neighbor[2]) not in forbidden \
                and in_bounds(neighbor, center) \
                and neighbor not in closed_set:
                    tentative_g_score = g_score[current] + cost(neighbor, current)
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + manhattan_distance_2d(neighbor, goal)
                        heapq.heappush(open_set, (f_score, neighbor))
    return []

def manhattan_distance_2d(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[2] - point2[2])

def cost(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[2] - point2[2]) + abs(point1[1] - point2[1])

def neighbors(point):
    return ((point[0]+1, point[1], point[2]), (point[0]-1, point[1], point[2]),
            (point[0], point[1]-1, point[2]), (point[0], point[1]+1, point[2]),
             (point[0], point[1], point[2]-1), (point[0], point[1], point[2]+1))


#get the points around each building where paths cannot be places
def get_all_forbidden(buildings):
    forbidden = set()
    for k, v in buildings.items():
        forbidden.update(get_forbidden(v, k))
    return forbidden

#helper for above function
def get_forbidden(center, building):
    if building != 'small house' or building != "tree":
      forbidden = set()
      sizes = {"cabin" : 11, "pyramid" : (10,5), "hut" : (10,5), "well" : (4,2), "small house" : (7, 5)}

      #special cabin case
      if building == "cabin":
        center = (center[0]+1, center[1], center[2]+1)
        for x in range(8):
            for y in range(7):
                forbidden.add((center[0]+x,center[2]-y))
        center = (center[0]-6, center[1], center[2]-2)
        for x in range(12):
            for y in range(8):
                forbidden.add((center[0]+x,center[2]+y))
      else:
        center = (center[0]-sizes[building][1], center[1], center[2]-sizes[building][1])
        for x in range(sizes[building][0]):
            for y in range(sizes[building][0]):
                forbidden.add((center[0]+x,center[2]+y))
    return forbidden

#check if a point is within the walls
def in_bounds(point, rec):
    if point[0] > (rec._offset.x + rec._size.x) or (point[0] < rec._offset.x):
        return False
    elif point[2] > (rec._offset.y + rec._size.y) or (point[2] < rec._offset.y):
        return False
    else:
        return True
    
#generate paths between buildings
def generate_paths(building_locations, buildRect, editor):
  worldSlice = editor.loadWorldSlice(buildRect)
  heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
  filtered_dict = {key: value for key, value in building_locations.items() if key != 'tree'}

  start_point = (filtered_dict["well"][0]-3, filtered_dict["well"][1], filtered_dict["well"][2]-3)
  goal_point = (filtered_dict["cabin"][0]-3, filtered_dict["cabin"][1], filtered_dict["cabin"][2]-3)
  path = a_star(start_point, goal_point, get_all_forbidden(filtered_dict), buildRect)
  print("Astar done : well to cabin")
  for block in path:
        placeDirtPath(Editor(), (block[0], heightmap[(block[0] - buildRect.offset.x, block[2] - buildRect.offset.y)] - 1, block[2]))

  start_point = (filtered_dict["well"][0]-3, filtered_dict["well"][1], filtered_dict["well"][2]-3)
  goal_point = (filtered_dict["hut"][0]-7, filtered_dict["hut"][1], filtered_dict["hut"][2])
  path = a_star(start_point, goal_point, get_all_forbidden(filtered_dict), buildRect)
  print("Astar done: well to hut")
  for block in path:
        placeDirtPath(Editor(), (block[0], heightmap[(block[0] - buildRect.offset.x, block[2] - buildRect.offset.y)] - 1, block[2]))

  start_point = (filtered_dict["pyramid"][0]-5, filtered_dict["pyramid"][1], filtered_dict["pyramid"][2])
  goal_point = (filtered_dict["hut"][0]-7, filtered_dict["hut"][1], filtered_dict["hut"][2])
  path = a_star(start_point, goal_point, get_all_forbidden(filtered_dict), buildRect)
  print("Astar done: hut to pyramid")
  for block in path:
        placeDirtPath(Editor(), (block[0], heightmap[(block[0] - buildRect.offset.x, block[2] - buildRect.offset.y)] - 1, block[2]))

  start_point = (filtered_dict["pyramid"][0]-5, filtered_dict["pyramid"][1], filtered_dict["pyramid"][2])
  goal_point = (filtered_dict["small house"][0]+1, filtered_dict["small house"][1], filtered_dict["small house"][2]-3)
  path = a_star(start_point, goal_point, get_all_forbidden(filtered_dict), buildRect)
  print("Astar done: pyramid to small house")
  for block in path:
        placeDirtPath(Editor(), (block[0], heightmap[(block[0] - buildRect.offset.x, block[2] - buildRect.offset.y)] - 1, block[2]))