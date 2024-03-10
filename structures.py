import sys
from random import randint

from gdpc import __url__, Editor, Block, Rect
from glm import ivec2
from gdpc.exceptions import BuildAreaNotSetError, InterfaceConnectionError
from gdpc.vector_tools import addY
    
def build_pyramid(block_choice: dict, build_area: Rect, center_vector: ivec2, editor: Editor):
    # Create base for structure
    foundation = build_area.centeredSubRect((7,7))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    # print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    # 2D array containing the blocks for each level of the build
    schematic = [
                 [
                 (["chiseled_sandstone"] + ["sandstone_stairs"] * 5 + ["chiseled_sandstone"]),
                 (["sandstone_stairs"] + ["air"] * 5 + ["sandstone_stairs"]),
                 (["sandstone_stairs"] + ["air"] * 5 + ["sandstone_stairs"]),
                 (["sandstone_stairs"] + ["air"] * 5 + ["sandstone_stairs"]),
                 (["sandstone_stairs"] + ["air"] * 5 + ["sandstone_stairs"]),
                 (["sandstone_stairs"] + ["air"] * 5 + ["sandstone_stairs"]),
                 (["chiseled_sandstone"] + ["sandstone_stairs"] * 5 + ["chiseled_sandstone"])
                 ],

                 [
                 (["chiseled_sandstone"] + ["air"] * 5 + ["chiseled_sandstone"]),
                 (["air"] + ["sandstone_stairs"] * 5 + ["air"]),
                 (["air"] + ["sandstone_stairs"] + ["air"] * 3 + ["sandstone_stairs"] + ["air"]),
                 (["air"] + ["sandstone_stairs"] + ["air"] * 3 + ["sandstone_stairs"] + ["air"]),
                 (["air"] + ["sandstone_stairs"] + ["air"] * 3 + ["sandstone_stairs"] + ["air"]),
                 (["air"] + ["sandstone_stairs"] * 5 + ["air"]),
                 (["chiseled_sandstone"] + ["air"] * 5 + ["chiseled_sandstone"])
                 ],

                 [
                 (["chiseled_sandstone"] + ["air"] * 5 + ["chiseled_sandstone"]),
                 ["air"] * 7,
                 (["air"] * 2 + ["sandstone_stairs"] * 3 + ["air"] * 2), 
                 (["air"] * 2 + ["sandstone_stairs"] + ["gold_block"] + ["sandstone_stairs"] + ["air"] * 2),
                 (["air"] * 2 + ["sandstone_stairs"] * 3 + ["air"] * 2), 
                 ["air"] * 7,
                 (["chiseled_sandstone"] + ["air"] * 5 + ["chiseled_sandstone"])
                 ],

                 [
                 (["gilded_blackstone"] + ["air"] * 5 + ["gilded_blackstone"]),
                 ["air"] * 7,
                 ["air"] * 7,
                 ["air"] * 7,
                 ["air"] * 7,
                 ["air"] * 7,
                 (["gilded_blackstone"] + ["air"] * 5 + ["gilded_blackstone"])
                 ]
                ]
                                
    rotations = [
                 [
                 ([None] + ["east"] * 5 + [None]),
                 (["south"] + [None] * 5 + ["north"]),
                 (["south"] + [None] * 5 + ["north"]),
                 (["south"] + [None] * 5 + ["north"]),
                 (["south"] + [None] * 5 + ["north"]),
                 (["south"] + [None] * 5 + ["north"]),
                 ([None] + ["west"] * 5 + [None])
                 ],
                
                 [
                 [None] * 7,
                 ([None] + ["east"] * 5 + [None]),
                 ([None] + ["south"] + [None] * 3 + ["north"] + [None]),
                 ([None] + ["south"] + [None] * 3 + ["north"] + [None]),
                 ([None] + ["south"] + [None] * 3 + ["north"] + [None]),
                 ([None] + ["west"] * 5 + [None]),
                 [None] * 7
                 ],
                    
                 [
                 [None] * 7,
                 [None] * 7,
                 ([None] * 2 + ["east"] * 3 + [None] * 2),
                 ([None] * 2 + ["south"] + [None] + ["north"] + [None] * 2),
                 ([None] * 2 + ["west"] * 3 + [None] * 2),
                 [None] * 7,
                 [None] * 7
                 ],

                 [
                 [None] * 7,
                 [None] * 7,
                 [None] * 7,
                 [None] * 7,
                 [None] * 7,
                 [None] * 7,
                 [None] * 7
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
    biome = worldSlice.getBiome(addY(foundation.middle, heightmap[tuple(foundation.size - (foundation.size.x / 2, foundation.size.y / 2))]))
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
        print("Level ", y, " done!")
    pass

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
        #print("Level ", y, " done!")


#build a tree of variable height
def build_tree(block_choice: dict, build_area: Rect, center_vector: ivec2, editor: Editor):
    # Create base for structure
    foundation = build_area.centeredSubRect((5,5))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    treeHeight = randint(2, 5)
    # print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    # Returns a 2D 11x11 array for the y ground value of each block in the rectangle
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    # Get the biome at the locally centered block
    biome = worldSlice.getBiome(addY(foundation.middle, heightmap[tuple(foundation.size - (foundation.size.x / 2, foundation.size.y / 2))]))
    if biome == '':
        biome = 'minecraft:plains'
    # Get wood types based on biome
    log = block_choice[biome]['log']
    leaves = block_choice[biome]['leaves']
    # 2D array containing the blocks for each level of the build
    schematic = []
    for block in range(0, treeHeight):
        schematic.append(
        [(["air"] * 5), 
         (["air"] * 5), 
         (["air"] * 2) + [log] + (["air"] * 2), 
         (["air"] * 5), 
         (["air"] * 5)])

    rest = [        
        [([leaves] * 5), 
         ([leaves] * 5), 
         ([leaves] * 2) + [log] + ([leaves] * 2), 
         ([leaves] * 5), 
         ([leaves] * 5)],

        [([leaves] * 5), 
         ([leaves] * 5), 
         ([leaves] * 2) + [log] + ([leaves] * 2), 
         ([leaves] * 5), 
         ([leaves] * 5)],

        [(["air"] * 5), 
         ["air"] + ([leaves] * 3) + ["air"],  
         ["air"] + ([leaves] * 3) + ["air"],
         ["air"] + ([leaves] * 3) + ["air"],
         (["air"] * 5)]
    ]
    schematic.extend(rest)

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
    # print(treeHeight)
    height_max = height + 3 + treeHeight
    # Loop through every coordinate (5 is the maximum height of the structure)
    for y in range(height, height_max):
        for x in range(low_x_cord, high_x_cord + 1):
            for z in range(low_z_cord, high_z_cord + 1):
                # Get the ground height for the block on the outline 
                # Add y-value to 2D vector (only has x,z coordinates)
                editor.placeBlock(addY((x,z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord]))
        # print("Level ", y, " done!")

            
    
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
    foundation = build_area.centeredSubRect((7, 10))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    # 2D array containing the blocks for each level of the swimming pool
    schematic = [
        [(["quartz_block"] * 9)+ ["air"],
        ["quartz_block"] + (["water"] * 7) + ["quartz_block"] + ["air"],
        ["quartz_block"] + (["water"] * 7) + ["quartz_block"] + ["quartz_stairs"],
        ["quartz_block"] + (["water"] * 7) + ["quartz_block"] + ["quartz_stairs"],
        ["quartz_block"] + (["water"] * 7) + ["quartz_block"] + ["quartz_stairs"],
        ["quartz_block"] + (["water"] * 7) + ["quartz_block"] + ["air"],
        (["quartz_block"] * 9) + ["air"]],
        
        [(["dark_oak_fence"]*9) + ["air"],
        ["dark_oak_fence"] + (["air"]*9),
        ["dark_oak_fence"] + (["air"]*9),
        ["dark_oak_fence"] + (["air"]*9),
        ["dark_oak_fence"] + (["air"]*9),
        ["dark_oak_fence"] + (["air"]*9),
        (["dark_oak_fence"]*9) + ["air"]
        ],
        
        [["dark_oak_fence"] + (["air"] * 7) + ["dark_oak_fence"] + ["air"],
        (["air"]*10),
        (["air"]*10),
        (["air"]*10),
        (["air"]*10),
        (["air"]*10),
        ["dark_oak_fence"] + (["air"] * 7) + ["dark_oak_fence"] + ["air"]
        ],

        
        [["glowstone"] + (["air"] * 7) + ["glowstone"] + ["air"],
        (["air"]*10),
        (["air"]*10),
        (["air"]*10),
        (["air"]*10),
        (["air"]*10),
        ["glowstone"] + (["air"] * 7) + ["glowstone"] + ["air"]
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
    height_max = height + 5  # Swimming pool is only one block tall

    for y in range(height, height_max):
        for x in range(low_x_cord, high_x_cord + 1):
            for z in range(low_z_cord, high_z_cord + 1):
                # Get the ground height for the block on the outline
                # Add y-value to 2D vector (only has x,z coordinates)
                editor.placeBlock(addY((x, z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord])) 