#!/usr/bin/env python3

"""
Place and retrieve a single block in the world.
"""

import sys
from random import randint

from gdpc import __url__, Editor, Block, Rect
from gdpc.exceptions import BuildAreaNotSetError, InterfaceConnectionError
from gdpc.vector_tools import addY

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
# Build wall to highlight build area
print("Building wall")
util.build_wall(buildRect, heightmap, editor)
# Clear trees from build area
print("Clearing trees")
util.clear_trees(worldSlice, buildRect, editor)
# Build structures
# 11x4x11
print("Building Cabin")
structures.build_cabin(biome_block_choice, buildRect.between((41,41), (52, 52)), buildRect.middle, editor)
# 3x4x3
print("Building Well")
structures.build_well(biome_block_choice, buildRect.between((4,31), (7, 34)), buildRect.middle, editor)
# 5xYx5
print("Building Tree")
structures.build_tree(biome_block_choice, buildRect.between((11,19), (16, 24)), buildRect.middle, editor)
# 7x4x7
print("Building Pyramid")
structures.build_pyramid(buildRect, buildRect.between((3,12), (10, 19)), editor)