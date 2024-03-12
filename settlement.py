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
# for x in range(0, center.x + 32):
#     for z in range(0, center.y + 32):
#         editor.placeBlock((x, height, z), Block("air"))

biome_block_choice = {"minecraft:plains": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves",
                                           "fence":"oak_fence"},
                      "minecraft:meadow": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves",
                                           "fence":"oak_fence"},
                      "minecraft:dark_forest": {"log":"oak_log",
                                           "plank":"oak_plank",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"dark_oak_leaves",}}
# print(worldSlice.getBiome(addY(buildRect.middle, heightmap[tuple(buildRect.offset)])))

# rect is defined as: 
# offset, and size  (x z) 
# buildRect:  Rect((-15, 24), (65, 65))
'''
Creates a Rect(), holding coordinates of where a building should be
middle: middle location of the settlement 
z_size: the x length of the settlement
z_size: the z length of the settlement 
TODO: Currently, buildings can clash into each other, needs to be fixed
'''
def create_building_location(middle: Rect, locations: defaultdict, building_name, x_size=64, z_size=64):
    max_x = x_size // 2
    max_z = z_size // 2 
    x_random_offset = randint(-max_x, max_x)
    z_random_offset = randint(-max_z, max_z)

    new_offset = (
        middle.offset[0] + x_random_offset,
        middle.offset[1] + z_random_offset
    )

    loc = Rect(new_offset, middle.size)
    locations[building_name] = loc 
    return loc 
    pass 


'''
Generates a settlement 
returns a dictionary of building names to locations (as Rects)
'''
def generate_settlement(): 
    # "BuildingName" : Ivec2()
    middle_location = buildRect # use this to base off create_building_offset

    # need an map of {"building name" : location } 
    # where location: is a Rect created by create_building_offset
    # for path finding
    locations = defaultdict(lambda: "Building does not exist")

    # Build wall to highlight build area
    print("Building wall")
    #util.build_wall(buildRect, heightmap, editor)

    # Clear trees from build area
    print("Clearing trees")
    #util.clear_trees(worldSlice, buildRect, editor)
    # Build structures
    
    # 11x4x11
    print("Building Cabin")
    loc = create_building_location(middle_location, locations, "cabin")
    structures.build_cabin(biome_block_choice, loc, buildRect.middle, editor)
    
    # 3x4x3
    print("Building Well")
    loc = create_building_location(middle_location, locations, "well")
    structures.build_well(biome_block_choice, loc, buildRect.middle, editor)
    # 5xYx5
    print("Building Tree")
    loc = create_building_location(middle_location, locations, "tree")
    structures.build_tree(biome_block_choice, loc, buildRect.middle, editor)

    # 9x4x9
    print("Building Pyramid")
    loc = create_building_location(middle_location, locations, "pyramid")
    structures.build_pyramid(biome_block_choice, loc, buildRect.between((3,12), (10, 19)), editor)
    
    # print("Building Swimming Pool")
    # loc = create_building_location(middle_location)
    # locations["pool"] = loc
    # structures.build_swimming_pool(biome_block_choice, loc, buildRect.middle, editor)

    print("Building Hut")
    loc = create_building_location(middle_location, locations, "hut")
    structures.build_hut(biome_block_choice, loc, buildRect.middle, editor)

    print("Building Farm")
    loc = create_building_location(middle_location, locations, "farm")
    structures.build_farmland(biome_block_choice, loc, buildRect.middle, editor)

     
    return locations
    pass


'''
Creates a road network between the buildings 
TODO: After the settlement is created, pathfind 

'''
def road_network(locations): 
    # TODO 
    pass 
building_locations = generate_settlement()
