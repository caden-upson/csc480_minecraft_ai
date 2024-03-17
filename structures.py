from gdpc import __url__, Editor, Block, Rect
from glm import ivec2
from gdpc.vector_tools import addY
import schematics
    
def build_pyramid(build_area: Rect, center_vector: ivec2, editor: Editor):
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
    
    schematic = schematics.getPyramidSchematic(biome)
    rotations = schematics.getPyramidRotations()
          
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
                rotation = rotations[y - height][x - low_x_cord][z - low_z_cord] 
                if rotation is not None:
                    editor.placeBlock(addY((x,z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord], {"facing": rotation}))
                else:
                    editor.placeBlock(addY((x,z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord]))
    return (foundation.middle.x, height, foundation.middle.y)

# builds a basic well 
# Builds a basic 11x4x11 house using the build_area given
def build_well(build_area: Rect, center_vector: ivec2, editor: Editor):
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
    
    schematic = schematics.getWellSchematic(biome)

                 
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
                editor.placeBlock(addY((x,z), y), Block(schematic[y - height][x - low_x_cord][z - low_z_cord]))
    return (foundation.middle.x, height, foundation.middle.y)

# Builds a basic 11x4x11 house using the build_area given
def build_cabin(build_area: Rect, center_vector: ivec2, editor: Editor):
    # Create base for structure
    foundation = build_area.centeredSubRect((11,11))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)

    # Gets the ground height (the y value the highest block excluding leaves is located)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    # Get the biome at the locally centered block
    biome = worldSlice.getBiomeGlobal(addY(foundation.middle, heightmap[tuple((0,0))]))
    if biome == '':
        biome = 'minecraft:plains'
    # Get wood types based on biome

    schematic = schematics.getCabinSchematic(biome)

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
def build_tree(build_area: Rect, center_vector: ivec2, editor: Editor):
    # Create base for structure
    foundation = build_area.centeredSubRect((5,8))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)

    # Gets the ground height (the y value the highest block excluding leaves is located)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    # Get the biome at the locally centered block
    biome = worldSlice.getBiomeGlobal(addY(foundation.middle, heightmap[tuple((0,0))]))
    if biome == '':
        biome = 'minecraft:plains'

    schematic = schematics.getTreeSchematic(biome)

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


def build_hut(build_area: Rect, center_vector: ivec2, editor: Editor):
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
    
    schematic = schematics.getHutSchematic(biome)

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


def build_small_house(build_area: Rect, center_vector: ivec2, editor: Editor):
    foundation = build_area.centeredSubRect((5, 6))
    # Load worldSlice to get the biomes as well as ground height
    worldSlice = editor.loadWorldSlice(foundation)
    print("World slice loaded!")
    # Gets the ground height (the y value the highest block excluding leaves is located)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    biome = worldSlice.getBiomeGlobal(addY(foundation.middle, heightmap[tuple((0,0))]))

    if biome == '':
        biome = 'minecraft:plains'
    
    schematic = schematics.getSmallHouseSchematic(biome)

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