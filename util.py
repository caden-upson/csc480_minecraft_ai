import sys
from random import randint

from gdpc import __url__, Editor, Block, WorldSlice, Rect
from gdpc.exceptions import BuildAreaNotSetError, InterfaceConnectionError
from gdpc.vector_tools import addY, Vec3iLike

import structures

# Clears the build area of trees
def clear_trees(worldSlice: WorldSlice, buildRect: Rect, editor: Editor):
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING"]
    opposite_corners = structures.get_opposing_corners(buildRect.corners)
    # Get bounds for loop
    low_x_cord = min(opposite_corners[0].x, opposite_corners[1].x)
    high_x_cord = max(opposite_corners[0].x, opposite_corners[1].x)
    low_z_cord = min(opposite_corners[0].y, opposite_corners[1].y)
    high_z_cord = max(opposite_corners[0].y, opposite_corners[1].y)
    # Loop through the highest block in the rectangular build area
    for x in range(low_x_cord, high_x_cord + 1):
        for z in range(low_z_cord, high_z_cord + 1):
            point = (x, z)
            height = heightmap[tuple((point) - buildRect.offset)]
            # Check if the block is a tree
            if (editor.getBlock(addY(point, height - 1)).id.endswith('leaves')):
                remove_tree(editor, addY(point, height - 1))

# Removes a structure categorized as a tree by this program.
# Something is a tree if there is a leaf block above either another leaf block or a kind of log.
def remove_tree(editor: Editor, position: Vec3iLike):
    # Loop through the y value of the current block to go from top to bottom
    # Remove if the block is a leaf or a log, replace with air block
    while (editor.getBlock(position).id.endswith('log') or editor.getBlock(position).id.endswith('leaves')):
        editor.placeBlock(position, Block("air"))
        # In case tree has a weird structure
        remove_around_base(editor, position)
        # Decrement y-value
        position = position - (0, 1, 0)
    
# For removing logs around base
def remove_around_base(editor: Editor, position: Vec3iLike):
    if (editor.getBlock(position - (1, 0, 0)).id.endswith('log')):
        editor.placeBlock(position - (1, 0, 0), Block("air"))
    if (editor.getBlock(position - (0, 0, 1)).id.endswith('log')):
        editor.placeBlock(position - (0, 0, 1), Block("air"))
    if (editor.getBlock(position + (1, 0, 0)).id.endswith('log')):
        editor.placeBlock(position - (1, 0, 0), Block("air"))
    if (editor.getBlock(position - (0, 0, 1)).id.endswith('log')):
        editor.placeBlock(position + (0, 0, 1), Block("air"))
        
# Builds a wall around the build area
def build_wall(buildRect: Rect, heightmap: dict, editor: Editor):
    # print("Placing walls...")

    for point in buildRect.outline:
        # Point is a 2D vector that has the x and z coordinates
        # addY adds a Y component to the 2D vector to make it a 3D vector
        
        height = heightmap[tuple(point - buildRect.offset)]
            
        # Build a wall on the surface that is made from a random selection of blocks
        for y in range(height, height + 5):
            i = randint(0, 4)
            wallPalette = [Block(id) for id in 3*["stone_bricks"] + ["cobblestone", "polished_andesite"]]
            if y == height + 4:
                editor.placeBlock(addY(point, y), Block("oak_fence"))
            else:
                editor.placeBlock(addY(point, y), Block(wallPalette[i]))