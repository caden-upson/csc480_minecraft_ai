#!/usr/bin/env python3

"""
Place and retrieve a single block in the world.
"""

import sys
from random import randint

from gdpc import __url__, Editor, Block, Rect
from gdpc.exceptions import BuildAreaNotSetError, InterfaceConnectionError
from gdpc.vector_tools import addY

import random 
from glm import ivec2
from collections import defaultdict
import structures
import util
import biome
import road
import astar

# Create an editor object.
# The Editor class provides a high-level interface to interact with the Minecraft world.
editor = Editor()


# Check if the editor can connect to the GDMC HTTP interface.
try:
    editor.checkConnection()
except InterfaceConnectionError:
    print(
        f"Error: Could not connect to the GDMC HTTP interface at {editor.host}!\n"
        "To use GDPC, you need to use a \"backend\" that provides the GDMC HTTP interface.\n"
        "For example, by running Minecraft with the GDMC HTTP mod installed.\n"
        f"See {__url__}/README.md for more information."
    )
    sys.exit(1)


# Get the build area.
try:
    buildArea = editor.getBuildArea()
except BuildAreaNotSetError:
    print(
        "Error: failed to get the build area!\n"
        "Make sure to set the build area with the /setbuildarea command in-game.\n"
        "For example: /setbuildarea ~0 0 ~0 ~64 200 ~64"
    )
    sys.exit(1)


# buildArea is a Box object, which is defined by an offset and a size.
print(f"Build area offset: {tuple(buildArea.offset)}")
print(f"Build area size:   {tuple(buildArea.size)}")

# The Box class has many convenience methods and properties. Here are a few.
print(f"Build area end:    {tuple(buildArea.end)}")
print(f"Build area last:   {tuple(buildArea.last)}") # Last is inclusive, end is exclusive.
print(f"Build area center: {tuple(buildArea.center)}")



print("Loading world slice...")
buildRect = buildArea.toRect()
worldSlice = editor.loadWorldSlice(buildRect)
print("World slice loaded!")

heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    
center = buildRect.center
print("Biome = ", worldSlice.getBiomeGlobal(addY(buildRect.middle, heightmap[tuple((0, 0))])))
# for x in range(0, center.x + 32):
#     for z in range(0, center.y + 32):
#         editor.placeBlock((x, height, z), Block("air"))


'''
Creates a Rect(), holding coordinates of where a building should be
middle: middle location of the settlement 
locations: a dictionary holding: { building_name : Rect(location) }
buildling: add False to argument, to not be connected on the road
z_size: the x length of the settlement
z_size: the z length of the settlement 
TODO: Currently, buildings can clash into each other, needs to be fixed
'''
spots_taken = set()
def create_building_location(middle: Rect, x_size=64, z_size=64):
    
    # This is so it does not build ON the wall 
    blocks_away_from_wall = 12
    max_x = (x_size // 2) - blocks_away_from_wall 
    max_z = (z_size // 2) - blocks_away_from_wall

    # because (1, 2) and (2, 2) are unique, buildings can build on each other (bad)
    # this will fix it
    off_dist = 10 
    x_random_offset = randint(-max_x // off_dist, max_x // off_dist) * off_dist
    z_random_offset = randint(-max_z // off_dist, max_z // off_dist) * off_dist

    position = (
        middle.offset[0] + x_random_offset,
        middle.offset[1] + z_random_offset
    )

    # Checks if location is taken already 
    if position in spots_taken: 
        return create_building_location(middle)
    else: 
        loc = Rect(position, middle.size)
        spots_taken.add(position) 
        return loc 
    pass 


'''
Generates a settlement 
returns a dictionary of building names to locations (as Rects)
'''
def generate_settlement(): 

    middle_location = buildRect # use this to base off create_building_offset

    locations = defaultdict(tuple)

    # Build wall to highlight build area
    print("Building wall")
    util.build_wall(buildRect, heightmap, editor)

    # Clear trees from build area
    print("Clearing trees")
    util.clear_trees(worldSlice, buildRect, editor)
    # Build structures
    
    # 11x4x11
    print("Building Cabin")
    loc = create_building_location(middle_location)
    locations['cabin'] = structures.build_cabin(biome.biome_block_choice, loc, buildRect.middle, editor)
    
    # 3x4x3
    print("Building Well")
    loc = create_building_location(middle_location)
    locations['well'] = structures.build_well(biome.biome_block_choice, loc, buildRect.middle, editor)
    # 5xYx5
    print("Building Tree")
    loc = create_building_location(middle_location)
    locations['tree'] = structures.build_tree(biome.biome_block_choice, loc, buildRect.middle, editor)

    # 9x4x9
    print("Building Pyramid")
    loc = create_building_location(middle_location)
    locations['pyramid'] = structures.build_pyramid(biome.biome_block_choice, loc, buildRect.between((3,12), (10, 19)), editor)

    # print("Building Swimming Pool")
    # loc = create_building_location(middle_location)
    # locations["pool"] = loc
    # structures.build_swimming_pool(biome_block_choice, loc, buildRect.middle, editor)

    print("Building Hut")
    loc = create_building_location(middle_location)
    locations['hut'] = structures.build_hut(biome.biome_block_choice, loc, buildRect.middle, editor)

    return locations

worldSlice = editor.loadWorldSlice(buildRect)
building_locations = generate_settlement()
heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
filtered_dict = {key: value for key, value in building_locations.items() if key != 'tree'}
# filtered_dict = {"cabin" : (-233, 84, 270), "well" : (-243, 70, 249)}
start_point = (filtered_dict["well"][0]-3, filtered_dict["well"][1], filtered_dict["well"][2]-3)
goal_point = (filtered_dict["cabin"][0]-3, filtered_dict["cabin"][1], filtered_dict["cabin"][2]-3)
path = road.a_star(start_point, goal_point, road.get_all_forbidden(filtered_dict))
print("Astar done")
for block in path:
    util.placeDirtPath(Editor(), (block[0], heightmap[(block[0] - buildRect.offset.x, block[2] - buildRect.offset.y)] - 1, block[2]))
start_point = (filtered_dict["well"][0]-3, filtered_dict["well"][1], filtered_dict["well"][2]-3)
goal_point = (filtered_dict["hut"][0]-7, filtered_dict["hut"][1], filtered_dict["hut"][2]-7)
path = road.a_star(start_point, goal_point, road.get_all_forbidden(filtered_dict))
print("Astar done")
for block in path:
    util.placeDirtPath(Editor(), (block[0], heightmap[(block[0] - buildRect.offset.x, block[2] - buildRect.offset.y)] - 1, block[2]))
start_point = (filtered_dict["pyramid"][0]-5, filtered_dict["pyramid"][1], filtered_dict["pyramid"][2]-5)
goal_point = (filtered_dict["hut"][0]-7, filtered_dict["hut"][1], filtered_dict["hut"][2]-7)
path = road.a_star(start_point, goal_point, road.get_all_forbidden(filtered_dict))
print("Astar done")
for block in path:
    util.placeDirtPath(Editor(), (block[0], heightmap[(block[0] - buildRect.offset.x, block[2] - buildRect.offset.y)] - 1, block[2]))