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
print("Biome = ", worldSlice.getBiome(addY(buildRect.middle, heightmap[tuple((0, 0))])))
# for x in range(0, center.x + 32):
#     for z in range(0, center.y + 32):
#         editor.placeBlock((x, height, z), Block("air"))

biome_block_choice = {"minecraft:plains": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:meadow": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:dark_forest": {"log":"dark_oak_log",
                                           "plank":"dark_oak_plank",
                                           "fence":"dark_oak_fence",
                                           "stairs":"dark_oak_stairs",
                                           "slab":"dark_oak_slab",
                                           "door":"dark_oak_door",
                                           "leaves":"dark_oak_leaves",},
                      "minecraft:ocean": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:deep_ocean": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:warm_ocean": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:luke_warm_ocean": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:deep_luke_warm_ocean": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:cold_ocean": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:deep_cold_ocean": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:frozen_ocean": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:deep_frozen_ocean": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:mushroom_fields": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:jagged_peaks": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:frozen_peaks": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:stony_peaks": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:cherry_grove": {"log":"cherry_log",
                                           "plank":"cherry_planks",
                                           "fence":"cherry_fence",
                                           "stairs":"cherry_stairs",
                                           "slab":"cherry_slab",
                                           "door":"cherry_door",
                                           "leaves":"cherry_leaves"},
                      "minecraft:grove": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:snowy_slopes": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:windswept_hills": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:windswept_gravelly_hills": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:windswept_forest": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:forest": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:flower_forest": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:taiga": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:old_growth_pine_taiga": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:old_growth_spruce_taiga": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:snowy_taiga": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:birch_forest": {"log":"birch_log",
                                           "plank":"birch_planks",
                                           "fence":"birch_fence",
                                           "stairs":"birch_stairs",
                                           "slab":"birch_slab",
                                           "door":"birch_door",
                                           "leaves":"birch_leaves"},
                      "minecraft:old_growth_birch_forest": {"log":"birch_log",
                                           "plank":"birch_planks",
                                           "fence":"birch_fence",
                                           "stairs":"birch_stairs",
                                           "slab":"birch_slab",
                                           "door":"birch_door",
                                           "leaves":"birch_leaves"},
                      "minecraft:dark_forest": {"log":"dark_oak_log",
                                           "plank":"dark_oak_planks",
                                           "fence":"dark_oak_fence",
                                           "stairs":"dark_oak_stairs",
                                           "slab":"dark_oak_slab",
                                           "door":"dark_oak_door",
                                           "leaves":"dark_oak_leaves"},
                      "minecraft:jungle": {"log":"jungle_log",
                                           "plank":"jungle_planks",
                                           "fence":"jungle_fence",
                                           "stairs":"jungle_stairs",
                                           "slab":"jungle_slab",
                                           "door":"jungle_door",
                                           "leaves":"jungle_leaves"},
                      "minecraft:sparse_jungle": {"log":"jungle_log",
                                           "plank":"jungle_planks",
                                           "fence":"jungle_fence",
                                           "stairs":"jungle_stairs",
                                           "slab":"jungle_slab",
                                           "door":"jungle_door",
                                           "leaves":"jungle_leaves"},
                      "minecraft:bamboo_jungle": {"log":"jungle_log",
                                           "plank":"jungle_planks",
                                           "fence":"jungle_fence",
                                           "stairs":"jungle_stairs",
                                           "slab":"jungle_slab",
                                           "door":"jungle_door",
                                           "leaves":"jungle_leaves"},
                      "minecraft:river": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:frozen_river": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:swamp": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:mangrove_swamp": {"log":"mangrove_log",
                                           "plank":"mangrove_planks",
                                           "fence":"mangrove_fence",
                                           "stairs":"mangrove_stairs",
                                           "slab":"mangrove_slab",
                                           "door":"mangrove_door",
                                           "leaves":"mangrove_leaves"},
                      "minecraft:beach": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:snowy_beach": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:stony_shore": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:sunflower_plains": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:snowy_plains": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:ice_spikes": {"log":"spruce_log",
                                           "plank":"spruce_planks",
                                           "fence":"spruce_fence",
                                           "stairs":"spruce_stairs",
                                           "slab":"spruce_slab",
                                           "door":"spruce_door",
                                           "leaves":"spruce_leaves"},
                      "minecraft:desert": {"log":"red_sandstone",
                                           "plank":"sandstone",
                                           "fence":"oak_fence",
                                           "stairs":"sandstone_stairs",
                                           "slab":"sandstone_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:savanna": {"log":"acacia_log",
                                           "plank":"acacia_planks",
                                           "fence":"acacia_fence",
                                           "stairs":"acacia_stairs",
                                           "slab":"acacia_slab",
                                           "door":"acacia_door",
                                           "leaves":"acacia_leaves"},
                      "minecraft:savanna_plateau": {"log":"acacia_log",
                                           "plank":"acacia_planks",
                                           "fence":"acacia_fence",
                                           "stairs":"acacia_stairs",
                                           "slab":"acacia_slab",
                                           "door":"acacia_door",
                                           "leaves":"acacia_leaves"},
                      "minecraft:windswept_savanna": {"log":"acacia_log",
                                           "plank":"acacia_planks",
                                           "fence":"acacia_fence",
                                           "stairs":"acacia_stairs",
                                           "slab":"acacia_slab",
                                           "door":"acacia_door",
                                           "leaves":"acacia_leaves"},
                      "minecraft:badlands": {"log":"dark_oak_log",
                                           "plank":"dark_oak_planks",
                                           "fence":"dark_oak_fence",
                                           "stairs":"dark_oak_stairs",
                                           "slab":"dark_oak_slab",
                                           "door":"dark_oak_door",
                                           "leaves":"dark_oak_leaves"},
                      "minecraft:wooded_badlands": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"},
                      "minecraft:eroded_badlands": {"log":"oak_log",
                                           "plank":"oak_planks",
                                           "fence":"oak_fence",
                                           "stairs":"oak_stairs",
                                           "slab":"oak_slab",
                                           "door":"oak_door",
                                           "leaves":"oak_leaves"}}
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
def create_building_location(middle: Rect, x_size=64, z_size=64):
    max_x = x_size // 2
    max_z = z_size // 2 
    x_random_offset = randint(-max_x, max_x)
    z_random_offset = randint(-max_z, max_z)

    new_offset = (
        middle.offset[0] + x_random_offset,
        middle.offset[1] + z_random_offset
    )

    return Rect(new_offset, middle.size)
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
    util.build_wall(buildRect, heightmap, editor)

    # Clear trees from build area
    print("Clearing trees")
    util.clear_trees(worldSlice, buildRect, editor)
    # Build structures
    
    # 11x4x11
    print("Building Cabin")
    loc = create_building_location(middle_location)
    locations["cabin"] = loc
    structures.build_cabin(biome_block_choice, loc, buildRect.middle, editor)
    
    # 3x4x3
    print("Building Well")
    loc = create_building_location(middle_location)
    locations["well"] = loc
    structures.build_well(biome_block_choice, loc, buildRect.middle, editor)
    # 5xYx5
    print("Building Tree")
    loc = create_building_location(middle_location)
    locations["tree"] = loc
    structures.build_tree(biome_block_choice, loc, buildRect.middle, editor)

    # 9x4x9
    print("Building Pyramid")
    loc = create_building_location(middle_location)
    locations["pyramid"] = loc
    structures.build_pyramid(biome_block_choice, loc, buildRect.between((3,12), (10, 19)), editor)
    
    # print("Building Swimming Pool")
    # loc = create_building_location(middle_location)
    # locations["pool"] = loc
    # structures.build_swimming_pool(biome_block_choice, loc, buildRect.middle, editor)
   
    print("Building Hut")
    loc = create_building_location(middle_location)
    locations["hut"] = loc
    structures.build_hut(biome_block_choice, loc, buildRect.middle, editor)
    return locations


'''
Creates a road network between the buildings 
TODO: After the settlement is created, pathfind 

'''
def road_network(locations): 
    # TODO 
    pass 
building_locations = generate_settlement()
