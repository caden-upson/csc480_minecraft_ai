import sys
from random import randint

from gdpc import __url__, Editor, Block, Rect
from glm import ivec2
from gdpc.exceptions import BuildAreaNotSetError, InterfaceConnectionError
from gdpc.vector_tools import addY

# Builds a basic 11x4x11 house using the build_area given
def build_cabin(block_choice: dict, build_area: Rect, center_vector: ivec2, editor: Editor):
    # Create base for structure
    foundation = build_area.centeredSubRect((11,11))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    # Returns a 2D 11x11 array for the y ground value of each block in the rectangle
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    # Get the biome at the locally centered block
    biome = worldSlice.getBiome(addY(foundation.middle, heightmap[tuple(foundation.size - (foundation.size.x / 2, foundation.size.y / 2))]))
    if biome == '':
        biome = 'minecraft:plains'
    # Get wood types based on biome
    log = block_choice[biome]['log']
    plank = block_choice[biome]['plank']
    door = block_choice[biome]['door']
    slab = block_choice[biome]['slab']
    stairs = block_choice[biome]['stairs']
    # 2D array containing the blocks for each level of the build
    schematic = [[
        ["grass_block"] * 11,
        (["grass_block"] * 6) + ([plank] * 4) + (["grass_block"]),
        (["grass_block"] * 6) + ([plank] * 4) + (["grass_block"]),
        (["grass_block"] * 6) + ([plank] * 4) + (["grass_block"]),
        (["grass_block"] * 6) + ([plank] * 4) + (["grass_block"]),
        (["grass_block"] * 6) + ([plank] * 4) + (["grass_block"]),
        (["grass_block"] * 6) + ([plank] * 4) + (["grass_block"]),
        (["grass_block"] + ([plank] * 9) + ["grass_block"]),
        (["grass_block"] + ([plank] * 9) + ["grass_block"]),
        (["grass_block"] + ([plank] * 9) + ["grass_block"]),
        (["grass_block"] * 11)],
                 
        [(["air"] * 5) + [log] + (["air"] * 4) + [log],
         (["air"] * 6) + ([plank] * 4) + ["air"] + ["air"],
         (["air"] * 6) + [plank] + (["air"] * 2) + [plank] + ["air"],
         (["air"] * 6) + [plank] + (["air"] * 2) + [plank] + ["air"],
         (["air"] * 6) + [plank] + (["air"] * 2) + [plank] + ["air"],
         [log] + (["air"]* 4) + [log] + (["air"] * 3) + [plank] + ["air"],
         ["air"] + [plank] + [door] + [door] + [plank] + (["air"] * 4) + [plank] + ["air"],
         ["air"] + [plank] + (["air"] * 7) + [plank] + ["air"],
         ["air"] + [plank] + (["air"] * 7) + [plank] + ["air"],
         ["air"] + ([plank] * 9) + ["air"],
         [log] + (["air"] * 9) + [log]],
        
        [(["air"] * 5) + [log] + (["air"] * 4) + [log],
         (["air"] * 6) + [plank] + (["glass"] * 2) + [plank] + ["air"],
         (["air"] * 6) + ["glass"] + (["air"] * 2) + ["glass"] + ["air"],
         (["air"] * 6) + ["glass"] + (["air"] * 2) + ["glass"] + ["air"],
         (["air"] * 6) + [plank] + (["air"] * 2) + ["glass"] + ["air"],
         [log] + (["air"]* 4) + [log] + (["air"] * 3) + ["glass"] + ["air"],
         ["air"] + [plank] + [None] + [None] + [plank] + (["air"] * 4) + ["glass"] + ["air"],
         ["air"] + ["glass"] + (["air"] * 7) + ["glass"] + ["air"],
         ["air"] + ["glass"] + (["air"] * 7) + ["glass"] + ["air"],
         ["air"] + ([plank] * 9) + ["air"],
         [log] + (["air"] * 9) + [log]],
        
        [(["air"] * 5) + [log] + (["air"] * 4) + [log],
         (["air"] * 6) + ([plank] * 4) + ["air"],
         (["air"] * 6) + [plank] + (["air"] * 2) + [plank] + ["air"],
         (["air"] * 6) + [plank] + (["air"] * 2) + [plank] + ["air"],
         (["air"] * 6) + [plank] + (["air"] * 2) + [plank] + ["air"],
         [log] + (["air"]* 4) + [log] + (["air"] * 3) + [plank] + ["air"],
         ["air"] + [plank] + [plank] + [plank] + [plank] + (["air"] * 4) + [plank] + ["air"],
         ["air"] + [plank] + (["air"] * 7) + [plank] + ["air"],
         ["air"] + [plank] + (["air"] * 7) + [plank] + ["air"],
         ["air"] + ([plank] * 9) + ["air"],
         [log] + (["air"] * 9) + [log]],
        
        [(["air"] * 5) + ([slab] * 6),
         (["air"] * 6) + ([slab] * 4) + ["air"],
         (["air"] * 6) + ([slab] * 4) + ["air"],
         (["air"] * 6) + ([slab] * 4) + ["air"],
         (["air"] * 6) + ([slab] * 4) + ["air"],
         ([slab] * 10) + ["air"],
         ["air"] + ([slab] * 9) + ["air"],
         ["air"] + ([slab] * 9) + ["air"],
         ["air"] + ([slab] * 9) + ["air"],
         ["air"] + ([slab] * 9) + ["air"],
         ([slab] * 11)]
    ]
    # Gets the two opposite corners of the rectangle
    opposite_corners = get_opposing_corners(foundation.corners)
    # Get bounds for loop
    low_x_cord = min(opposite_corners[0].x, opposite_corners[1].x)
    high_x_cord = max(opposite_corners[0].x, opposite_corners[1].x)
    low_z_cord = min(opposite_corners[0].y, opposite_corners[1].y)
    high_z_cord = max(opposite_corners[0].y, opposite_corners[1].y)
    # Get ground height
    height = heightmap[tuple((foundation.center) - foundation.offset)]
    # How tall the structure will be
    height_max = height + 4
    # Loop through every coordinate (4 is the maximum height of the structure)
    for y in range(height, height_max + 1):
        for x in range(low_x_cord, high_x_cord + 1):
            for z in range(low_z_cord, high_z_cord + 1):
                # Get the ground height for the block on the outline 
                # Add y-value to 2D vector (only has x,z coordinates)
                editor.placeBlock(addY((x,z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord]))
        print("Level ", y, " done!")
            
    
# Gets the opposite corners of the rectangle object
def get_opposing_corners(corners: list):
    result = []
    for corner in corners:
        if len(result) == 0:
            result.append(corner)
        else:
            for corner_in_list in result:
                if (corner.x != corner_in_list.x) and (corner.y != corner_in_list.y):
                    result.append(corner)
    return result
                