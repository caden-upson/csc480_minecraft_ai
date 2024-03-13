import sys
from random import randint

from gdpc import __url__, Editor, Block, Rect
from glm import ivec2
from gdpc.exceptions import BuildAreaNotSetError, InterfaceConnectionError
from gdpc.vector_tools import addY
    
def build_pyramid(block_choice: dict, build_area: Rect, center_vector: ivec2, editor: Editor):
    # Create base for structure
    foundation = build_area.centeredSubRect((9,9))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    # print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    
    biome = worldSlice.getBiomeGlobal(addY(foundation.middle, heightmap[tuple((0,0))]))
    print("Biome = ", biome)
    if biome == '':
        biome = 'minecraft:plains'
    plank = block_choice[biome]['slab']

    # 2D array containing the blocks for each level of the build
    schematic = [
                 [
                 [plank] * 9,
                 ([plank] + ["chiseled_sandstone"] + ["sandstone_stairs"] * 5 + ["chiseled_sandstone"] + [plank]),
                 ([plank] + ["sandstone_stairs"] + ["air"] * 5 + ["sandstone_stairs"] + [plank]),
                 ([plank] + ["sandstone_stairs"] + ["air"] * 5 + ["sandstone_stairs"] + [plank]),
                 ([plank] + ["sandstone_stairs"] + ["air"] * 5 + ["sandstone_stairs"] + [plank]),
                 ([plank] + ["sandstone_stairs"] + ["air"] * 5 + ["sandstone_stairs"] + [plank]),
                 ([plank] + ["sandstone_stairs"] + ["air"] * 5 + ["sandstone_stairs"] + [plank]),
                 ([plank] + ["chiseled_sandstone"] + ["sandstone_stairs"] * 5 + ["chiseled_sandstone"] + [plank]),
                 [plank] * 9,
                 ],
 
                 [
                 ["air"] * 9,
                 (["air"] + ["chiseled_sandstone"] + ["air"] * 5 + ["chiseled_sandstone"] + ["air"]),
                 (["air"] * 2 + ["sandstone_stairs"] * 5 + ["air"] * 2),
                 (["air"] * 2 + ["sandstone_stairs"] + ["air"] * 3 + ["sandstone_stairs"] + ["air"] * 2),
                 (["air"] * 2 + ["sandstone_stairs"] + ["air"] * 3 + ["sandstone_stairs"] + ["air"] * 2),
                 (["air"] * 2 + ["sandstone_stairs"] + ["air"] * 3 + ["sandstone_stairs"] + ["air"] * 2),
                 (["air"] * 2 + ["sandstone_stairs"] * 5 + ["air"] * 2),
                 (["air"] + ["chiseled_sandstone"] + ["air"] * 5 + ["chiseled_sandstone"] + ["air"]),
                 ["air"] * 9
                 ],

                 [
                 ["air"] * 9,
                 (["air"] + ["chiseled_sandstone"] + ["air"] * 5 + ["chiseled_sandstone"] + ["air"]),
                 ["air"] * 9,
                 (["air"] * 3 + ["sandstone_stairs"] * 3 + ["air"] * 3), 
                 (["air"] * 3 + ["sandstone_stairs"] + ["gold_block"] + ["sandstone_stairs"] + ["air"] * 3),
                 (["air"] * 3 + ["sandstone_stairs"] * 3 + ["air"] * 3), 
                 ["air"] * 9,
                 (["air"] + ["chiseled_sandstone"] + ["air"] * 5 + ["chiseled_sandstone"] + ["air"]),
                 ["air"] * 9
                 ],

                 [
                 ["air"] * 9, 
                 (["air"] + ["gilded_blackstone"] + ["air"] * 5 + ["gilded_blackstone"] + ["air"]),
                 ["air"] * 9,
                 ["air"] * 9,
                 ["air"] * 9,
                 ["air"] * 9,
                 ["air"] * 9,
                 (["air"] + ["gilded_blackstone"] + ["air"] * 5 + ["gilded_blackstone"] + ["air"]),
                 ["air"] * 9
                 ]
                ]
                                
    rotations = [
                 [
                 [None] * 9,
                 ([None] * 2 + ["east"] * 5 + [None] * 2),
                 ([None] + ["south"] + [None] * 5 + ["north"] + [None]),
                 ([None] + ["south"] + [None] * 5 + ["north"] + [None]),
                 ([None] + ["south"] + [None] * 5 + ["north"] + [None]),
                 ([None] + ["south"] + [None] * 5 + ["north"] + [None]),
                 ([None] + ["south"] + [None] * 5 + ["north"] + [None]),
                 ([None] * 2 + ["west"] * 5 + [None] * 2),
                 [None] * 9
                 ],
                
                 [
                 [None] * 9,
                 [None] * 9,
                 ([None] * 2 + ["east"] * 5 + [None] * 2),
                 ([None] * 2 + ["south"] + [None] * 3 + ["north"] + [None] * 2),
                 ([None] * 2 + ["south"] + [None] * 3 + ["north"] + [None] * 2),
                 ([None] * 2 + ["south"] + [None] * 3 + ["north"] + [None] * 2),
                 ([None] * 2 + ["west"] * 5 + [None] * 2),
                 [None] * 9,
                 [None] * 9
                 ],
                    
                 [
                 [None] * 9,
                 [None] * 9,
                 [None] * 9,
                 ([None] * 3 + ["east"] * 3 + [None] * 3),
                 ([None] * 3 + ["south"] + [None] + ["north"] + [None] * 3),
                 ([None] * 3 + ["west"] * 3 + [None] * 3),
                 [None] * 9,
                 [None] * 9,
                 [None] * 9
                 ],

                 [[None] * 9] * 9
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

    for y in range(height, height_max):
        for x in range(low_x_cord, high_x_cord + 1):
            for z in range(low_z_cord, high_z_cord + 1):
                # Get the ground height for the block on the outline 
                # Add y-value to 2D vector (only has x,z coordinates)
                # print("Indices:", y - height, x - low_x_cord, z - low_z_cord)
                rotation = rotations[y - height][x - low_x_cord][z - low_z_cord] 
                if rotation is not None:
                    editor.placeBlock(addY((x,z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord], {"facing": rotation}))
                else:
                    editor.placeBlock(addY((x,z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord]))
    return (foundation.middle.x, height, foundation.middle.y)

# builds a basic well 
# Builds a basic 11x4x11 house using the build_area given
def build_well(block_choice: dict, build_area: Rect, center_vector: ivec2, editor: Editor):
    # Create base for structure
    foundation = build_area.centeredSubRect((3,3))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    # Returns a 2D 11x11 array for the y ground value of each block in the rectangle
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    # Get the biome at the locally centered block
    biome = worldSlice.getBiomeGlobal(addY(foundation.middle, heightmap[tuple((0,0))]))
    if biome == '':
        biome = 'minecraft:plains'
    plank = block_choice[biome]['plank']
    fence = block_choice[biome]['fence']
    slab = block_choice[biome]['slab']
    # Get wood types based on biome
    # 2D array containing the blocks for each level of the build
    schematic = [[["stone_bricks"] * 3,
                 (["stone_bricks"] + ["water"] + ["stone_bricks"]),
                 ["stone_bricks"] * 3],

                 [([fence] + ["air"] + [fence]),
                 (["air"] + ["cauldron"] + ["air"]),
                 ([fence] + ["air"] + [fence])],

                 [([fence] + ["air"] + [fence]),
                 (["air"] + ["chain"] + ["air"]),
                 ([fence] + ["air"] + [fence])],

                 [[slab] * 3,
                 ([slab] + [plank] + [slab]),
                 [slab] * 3]
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

    for y in range(height, height_max):
        for x in range(low_x_cord, high_x_cord + 1):
            for z in range(low_z_cord, high_z_cord + 1):
                # Get the ground height for the block on the outline 
                # Add y-value to 2D vector (only has x,z coordinates)
                # print("Indices:", y - height, x - low_x_cord, z - low_z_cord)
                editor.placeBlock(addY((x,z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord]))
        # print("Level ", y, " done!")
    return (foundation.middle.x, height, foundation.middle.y)

# Builds a basic 11x4x11 house using the build_area given
def build_cabin(block_choice: dict, build_area: Rect, center_vector: ivec2, editor: Editor):
    # Create base for structure
    foundation = build_area.centeredSubRect((11,11))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    # print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    # Returns a 2D 11x11 array for the y ground value of each block in the rectangle
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    # Get the biome at the locally centered block
    biome = worldSlice.getBiomeGlobal(addY(foundation.middle, heightmap[tuple((0,0))]))
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
        #print("Level ", y, " done!")
    return (foundation.middle.x, height, foundation.middle.y)

#build a tree of variable height
def build_tree(block_choice: dict, build_area: Rect, center_vector: ivec2, editor: Editor):
    # Create base for structure
    foundation = build_area.centeredSubRect((5,8))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    # treeHeight = randint(2, 5)
    # print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    # Returns a 2D 11x11 array for the y ground value of each block in the rectangle
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    # Get the biome at the locally centered block
    biome = worldSlice.getBiomeGlobal(addY(foundation.middle, heightmap[tuple((0,0))]))
    if biome == '':
        biome = 'minecraft:plains'
    # Get wood types based on biome
    log = block_choice[biome]['wood']
    leaves = block_choice[biome]['leaves']
    # 2D array containing the blocks for each level of the build
    schematic = [
        [
            ["air"] * 8,
            (["air"] * 3 + [log] + ["air"] * 4),
            (["air"] * 2 + [log] * 4 + ["air"] * 2),
            (["air"] * 4 + [log] + ["air"] * 3),
            ["air"] * 8
        ],

        [
            ["air"] * 8,
            (["air"] * 3 + [log] + ["air"] * 4),
            (["air"] * 3 + [log] * 2 + ["air"] * 3),
            ["air"] * 8,
            ["air"] * 8
        ],

        [
            ["air"] * 8,
            ["air"] * 8,
            (["air"] * 3 + [log] * 2 + ["air"] * 3),
            ["air"] * 8,
            ["air"] * 8
        ],

        [
            ["air"] * 8,
            ["air"] * 8,
            (["air"] * 2 + [log] * 2 + ["air"] * 4),
            ["air"] * 8,
            ["air"] * 8
        ],

        [
            ["air"] * 8,
            (["air"] + [leaves] * 4 + ["air"] * 3),
            ([leaves] + [log] * 2 + [leaves] * 3 + ["air"] * 2),
            (["air"] + [leaves] * 4 + ["air"] * 3),
            ["air"] * 8
        ],

        [
            (["air"] * 4 + [leaves] + ["air"] * 3),
            (["air"] * 2 + [leaves] * 4 + ["air"] * 2),
            (["air"] + [leaves] * 2 + [log] * 2 + [leaves] * 2 + ["air"]),
            (["air"] * 2 + [leaves] * 5 + ["air"] * 1),
            ["air"] * 8
        ],

        [
            (["air"] * 3 + [leaves] * 4 + ["air"]),
            (["air"] * 2 + [leaves] * 6),
            (["air"] * 2 + [leaves] * 6),
            (["air"] * 3 + [leaves] * 5),
            (["air"] * 3 + [leaves] * 3 + ["air"] * 2),
        ],

        [
            ["air"] * 8,
            (["air"] * 4 + [leaves] * 3 + ["air"]),
            (["air"] * 3 + [leaves] * 4 + ["air"]),
            (["air"] * 4 + [leaves] + ["air"] + [leaves] + ["air"]),
            ["air"] * 8,
        ]
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
    height_max = height + 8
    # Loop through every coordinate (5 is the maximum height of the structure)
    for y in range(height, height_max):
        for x in range(low_x_cord, high_x_cord + 1):
            for z in range(low_z_cord, high_z_cord + 1):
                # Get the ground height for the block on the outline 
                # Add y-value to 2D vector (only has x,z coordinates)
                editor.placeBlock(addY((x,z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord]))
        # print("Level ", y, " done!")
    return (foundation.middle.x, height, foundation.middle.y)            
    
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
                


def build_swimming_pool(block_choice: dict, build_area: Rect, center_vector: ivec2, editor: Editor):
    # Create base for the swimming pool
    foundation = build_area.centeredSubRect((7, 11))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    biome = worldSlice.getBiomeGlobal(addY(foundation.middle, heightmap[tuple((0,0))]))

    if biome == '':
        biome = 'minecraft:plains'

    fence = block_choice[biome]['fence']
    plank = block_choice[biome]['plank']
    stairs = block_choice[biome]['stairs']

    # 2D array containing the blocks for each level of the swimming pool
    schematic = [
        [([plank]*9) + (["air"]*2),
         ([plank]*9) + (["air"]*2),
         ([plank]*10) + ["quartz_stairs"],
         ([plank]*10) + ["quartz_stairs"],
         ([plank]*10) + ["quartz_stairs"],
         ([plank]*9) + (["air"]*2),
         ([plank]*9) + (["air"]*2)
         ],

        [([plank] * 9)+ (["air"]*2),
        [plank] + (["water"] * 7) + [plank] + (["air"]*2),
        [plank] + (["water"] * 7) + [plank] + [stairs] + ["air"],
        [plank] + (["water"] * 7) + [plank] + [stairs] + ["air"],
        [plank] + (["water"] * 7) + [plank] + [stairs] + ["air"],
        [plank] + (["water"] * 7) + [plank] + (["air"]*2),
        ([plank] * 9) + (["air"]*2)],
        
        [([fence]*9) + (["air"]*2),
        [fence] + (["air"]*10),
        [fence] + (["air"]*10),
        [fence] + (["air"]*10),
        [fence] + (["air"]*10),
        [fence] + (["air"]*10),
        ([fence]*9) + (["air"]*2)
        ],
        
        [[fence] + (["air"] * 7) + [fence] + (["air"]*2),
        (["air"]*11),
        (["air"]*11),
        (["air"]*11),
        (["air"]*11),
        (["air"]*11),
        [fence] + (["air"] * 7) + [fence] + (["air"]*2)
        ],

        
        [["glowstone"] + (["air"] * 7) + ["glowstone"] + (["air"]*2),
        (["air"]*11),
        (["air"]*11),
        (["air"]*11),
        (["air"]*11),
        (["air"]*11),
        ["glowstone"] + (["air"] * 7) + ["glowstone"] + (["air"]*2)
        ]

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
    height_max = height + 6  # Swimming pool is 6 blocks tall

    for y in range(height, height_max):
        for x in range(low_x_cord, high_x_cord + 1):
            for z in range(low_z_cord, high_z_cord + 1):
                # Get the ground height for the block on the outline
                # Add y-value to 2D vector (only has x,z coordinates)
                editor.placeBlock(addY((x, z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord])) 
    return (foundation.middle.x, height, foundation.middle.y)

def build_hut(block_choice: dict, build_area: Rect, center_vector: ivec2, editor: Editor):
    # Create base for the swimming pool
    foundation = build_area.centeredSubRect((7, 7))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    biome = worldSlice.getBiomeGlobal(addY(foundation.middle, heightmap[tuple((0,0))]))

    if biome == '':
        biome = 'minecraft:plains'

    plank = block_choice[biome]['plank']
    log = block_choice[biome]['log']
    door = block_choice[biome]['door']

    # 2D array containing the blocks for each level of the swimming pool
    schematic = [
        [
        (["grass_block"] * 7),
        ["grass_block"] + ([plank] * 5) + ["grass_block"],
        ["grass_block"] + ([plank] * 5) + ["grass_block"],
        ["grass_block"] + ([plank] * 5) + ["grass_block"],
        ["grass_block"] + ([plank] * 5) + ["grass_block"],
        ["grass_block"] + ([plank] * 5) + ["grass_block"],
        (["grass_block"] * 7)],

        [[log] + (["air"]*5) + [log],
        ["air"] + ([plank]*2) + [door] + ([plank]*2) + ["air"],
        ["air"] + [plank] + (["air"] * 3) + [plank] + ["air"],
        ["air"] + [plank] + (["air"] * 3) + [plank] + ["air"],
        ["air"] + [plank] + (["air"] * 3) + [plank] + ["air"],
        ["air"] + ([plank]*5) + ["air"],
        [log] + (["air"]*5) + [log]
         ],

        [[log] + (["air"]*5) + [log],
        ["air"] + ([plank]*2) + [None] + ([plank]*2) + ["air"],
        ["air"] + [plank] + (["air"] * 3) + [plank] + ["air"],
        ["air"] + [plank] + (["air"] * 3) + [plank] + ["air"],
        ["air"] + [plank] + (["air"] * 3) + [plank] + ["air"],
        ["air"] + ([plank]*5) + ["air"],
        [log] + (["air"]*5) + [log]
         ],

         [[log] + (["air"]*5) + [log],
        ["air"] + ([plank]*5) + ["air"],
        ["air"] + ["glass"] + (["air"] * 3) + ["glass"] + ["air"],
        ["air"] + ["glass"] + (["air"] * 3) + ["glass"] + ["air"],
        ["air"] + ["glass"] + (["air"] * 3) + ["glass"] + ["air"],
        ["air"] + ([plank]*5) + ["air"],
        [log] + (["air"]*5) + [log]
         ],

         [[log] + (["air"]*5) + [log],
        ["air"] + [plank] + (["glass"] * 3) + [plank] + ["air"],
        ["air"] + ["glass"] + (["air"] * 3) + ["glass"] + ["air"],
        ["air"] + ["glass"] + (["air"] * 3) + ["glass"] + ["air"],
        ["air"] + ["glass"] + (["air"] * 3) + ["glass"] + ["air"],
        ["air"] + [plank] + (["glass"] * 3) + [plank] + ["air"],
        [log] + (["air"]*5) + [log]
         ],

         [[log] + (["air"]*5) + [log],
        ["air"] + [plank] + (["glass"] * 3) + [plank] + ["air"],
        ["air"] + [plank] + (["air"] * 3) + [plank] + ["air"],
        ["air"] + [plank] + (["air"] * 3) + [plank] + ["air"],
        ["air"] + [plank] + (["air"] * 3) + [plank] + ["air"],
        ["air"] + [plank] + (["glass"] * 3) + [plank] + ["air"],
        [log] + (["air"]*5) + [log]
         ],

         [[log] + (["air"]*5) + [log],
        ["air"] + ([plank]*5) + ["air"],
        ["air"] + [plank] + (["air"] * 3) + [plank] + ["air"],
        ["air"] + [plank] + (["air"] * 3) + [plank] + ["air"],
        ["air"] + [plank] + (["air"] * 3) + [plank] + ["air"],
        ["air"] + ([plank]*5) + ["air"],
        [log] + (["air"]*5) + [log]
         ],

         [
         (["stone_brick_slab"] * 7),
         (["stone_brick_slab"] * 7),
         (["stone_brick_slab"] * 7),
         (["stone_brick_slab"] * 7),
         (["stone_brick_slab"] * 7),
         (["stone_brick_slab"] * 7),
         (["stone_brick_slab"] * 7)
         ]

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
    height_max = height + 8 

    for y in range(height, height_max):
        for x in range(low_x_cord, high_x_cord + 1):
            for z in range(low_z_cord, high_z_cord + 1):
                # Get the ground height for the block on the outline
                # Add y-value to 2D vector (only has x,z coordinates)
                editor.placeBlock(addY((x, z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord])) 
    return (foundation.middle.x, height, foundation.middle.y)


def build_fountain(block_choice: dict, build_area: Rect, center_vector: ivec2, editor: Editor):
    # Create base for the swimming pool
    foundation = build_area.centeredSubRect((9, 9))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    biome = worldSlice.getBiome(addY(foundation.middle, heightmap[tuple(foundation.size - (foundation.size.x / 2, foundation.size.y / 2))]))
    biome = worldSlice.getBiomeGlobal(addY(foundation.middle, heightmap[tuple((0,0))]))

    if biome == '':
        biome = 'minecraft:plains'



    # 2D array containing the blocks for each level of the "farmland"
    schematic = [
        [(["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9)],

        [(["dirt"] * 9),
         (["farmland"] * 7) + ["air"] + ["dirt"],
         (["farmland"] * 7) + ["air"] + ["dirt"],
         (["farmland"] * 7) + ["air"] + ["dirt"],
         (["farmland"] * 7) + ["air"] + ["dirt"],
         (["farmland"] * 7) + ["air"] + ["dirt"],
         (["farmland"] * 7) + ["air"] + ["dirt"],
         (["farmland"] * 7) + ["air"] + ["dirt"],
         (["dirt"] * 9)],

        [(["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9),
         (["dirt"] * 9)]]

    plank = block_choice[biome]['plank']
    leaves = block_choice[biome]['leaves']

    # 2D array containing the blocks for each level of the swimming pool
    schematic = [
        [
            (["air"] * 2) + ([plank] * 5) + (["air"] * 2),
            ["air"] + ["glowstone"] + ([plank] * 5) + ["glowstone"] + ["air"],
            ([plank] * 9),
            ([plank] * 9),
            ([plank] * 9),
            ([plank] * 9),
            ([plank] * 9),
            ["air"] + ["glowstone"] + ([plank] * 5) + ["glowstone"] + ["air"],
            (["air"] * 2) + ([plank] * 5) + (["air"] * 2)
        ],

        [
            (["air"] * 9),
            ["air"] +  [leaves] + ["stone_slab"] + (["stone_bricks"] * 3) + ["stone_slab"] + [leaves] + ["air"],
            ["air"] + ["stone_slab"] + ["stone_bricks"] + (["air"] * 3) + ["stone_bricks"] + ["stone_slab"] + ["air"],
            ["air"] + ["stone_bricks"] + (["air"] * 5) + ["stone_bricks"] + ["air"],
            ["air"] + ["stone_bricks"] + (["air"] * 2) + ["stone_bricks"] + (["air"] * 2) + ["stone_bricks"] + ["air"],
            ["air"] + ["stone_bricks"] + (["air"] * 5) + ["stone_bricks"] + ["air"],
            ["air"] + ["stone_slab"] + ["stone_bricks"] + (["air"] * 3) + ["stone_bricks"] + ["stone_slab"] + ["air"],
            ["air"] +  [leaves] + ["stone_slab"] + (["stone_bricks"] * 3) + ["stone_slab"] + [leaves] + ["air"],
            (["air"] * 9)
        ],

        [
            (["air"] * 9),
            ["air"] + [leaves] + (["air"] * 5) + [leaves] + ["air"],
            (["air"] * 2) + ["air"] + (["air"] * 3) + ["air"] + (["air"] * 2),
            (["air"] * 9),
            (["air"] * 4) + ["stone_bricks"] + (["air"] * 4),
            (["air"] * 9),
            (["air"] * 2) + ["air"] + (["air"] * 3) + ["air"] + (["air"] * 2),
            ["air"] + [leaves] + (["air"] * 5) + [leaves] + ["air"],
            (["air"] * 9)
        ],

        [
            (["air"] * 9),
            ["air"] + [leaves] + (["air"] * 5) + [leaves] + ["air"],
            (["air"] * 2) + ["air"] + (["air"] * 3) + ["air"] + (["air"] * 2),
            (["air"] * 9),
            (["air"] * 4) + ["stone_bricks"] + (["air"] * 4),
            (["air"] * 9),
            (["air"] * 2) + ["air"] + (["air"] * 3) + ["air"] + (["air"] * 2),
            ["air"] + [leaves] + (["air"] * 5) + [leaves] + ["air"],
            (["air"] * 9)
        ],

        [
            (["air"] * 9),
            (["air"] * 9),
            (["air"] * 9),
            (["air"] * 9),
            (["air"] * 4) + ["stone_bricks"] + (["air"] * 4),
            (["air"] * 9),
            (["air"] * 9),
            (["air"] * 9),
            (["air"] * 9)
        ],

        [
            (["air"] * 9),
            (["air"] * 9),
            (["air"] * 9),
            (["air"] * 9),
            (["air"] * 4) + ["water"] + (["air"] * 4),
            (["air"] * 9),
            (["air"] * 9),
            (["air"] * 9),
            (["air"] * 9)
        ]
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
    height_max = height + 6

    for y in range(height, height_max):
        for x in range(low_x_cord, high_x_cord + 1):
            for z in range(low_z_cord, high_z_cord + 1):
                # Get the ground height for the block on the outline
                # Add y-value to 2D vector (only has x,z coordinates)
                editor.placeBlock(addY((x, z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord])) 
    return (foundation.middle.x, height, foundation.middle.y)


def build_small_house(block_choice: dict, build_area: Rect, center_vector: ivec2, editor: Editor):
    foundation = build_area.centeredSubRect((5, 6))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    biome = worldSlice.getBiomeGlobal(addY(foundation.middle, heightmap[tuple((0,0))]))

    if biome == '':
        biome = 'minecraft:plains'

    plank = block_choice[biome]['plank']
    log = block_choice[biome]['log']
    door = block_choice[biome]['door']

    # 2D array containing the blocks for each level of the swimming pool
    schematic = [
        [
        ["air"] + (["cobblestone"] * 5),
        ["air"] + (["cobblestone"] * 5),
        ["torch"] + (["cobblestone"] * 5),
        ["air"] + (["cobblestone"] * 5),
        ["torch"] + (["cobblestone"] * 5)
        ],

        [
        ["air"] + ([plank] * 4) + [log],
        ["air"] + [plank] + (["air"] * 2) + ["crafting_table"] + [plank],
        ["air"] + [log] + (["air"] * 2) + ["furnace"] + [plank],
        ["air"] + [door] + (["air"] * 3) + [plank],
        ["air"] + [log] + ([plank] * 3) + [log]
        ],

        [
        ["air"] + (["glass_pane"] * 3) + [plank] + [log],
        ["air"] + ["glass_pane"] + (["air"] * 3) + [plank],
        ["air"] + [log] + (["air"] * 3) + ["glass_pane"],
        ["air"] + [None] + (["air"] * 3) + [plank],
        ["air"] + [log] + [plank] + ["glass_pane"] + [plank] + [log]
        ],

        [
        ["air"] + ([plank] * 4) + [log],
        ["air"] + [plank] + (["air"] * 3) + [plank],
        ["air"] + [log] + (["air"] * 3) + [plank],
        ["air"] + [plank] + (["air"] * 3) + [plank],
        ["air"] + [log] + ([plank] * 3) + [log]
        ],

        [
        ["air"] + (["stone_slab"] * 5),
        ["air"] + (["stone_slab"] * 5),
        ["air"] + (["stone_slab"] * 5),
        ["air"] + (["stone_slab"] * 5),
        ["air"] + (["stone_slab"] * 5)
        ]]

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
    height_max = height + 5

    for y in range(height, height_max):
        for x in range(low_x_cord, high_x_cord + 1):
            for z in range(low_z_cord, high_z_cord + 1):
                # Get the ground height for the block on the outline
                # Add y-value to 2D vector (only has x,z coordinates)

                if schematic[y - height][x - low_x_cord][z - low_z_cord] == ["farmland"]: 
                    editor.placeBlock(addY((x, z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord], {"moisture": 7}))
                else: 
                    editor.placeBlock(addY((x, z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord], {}))
    # Plant crops in the "farmland"
    for y in range(height, height_max):
      for x in range(low_x_cord + 1, high_x_cord):
          for z in range(low_z_cord + 1, high_z_cord):
              editor.placeBlock(addY((x, z), height + 1), Block(['seed']))
              editor.placeBlock(addY((x, z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord])) 
    return (foundation.middle.x, height, foundation.middle.y)
