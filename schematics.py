from biome import biome_block_choice

# retrieves the schematic for the pyramid
def getPyramidSchematic(biome):
    plank = biome_block_choice[biome]['slab']

    # 2D array containing the blocks for each level of the build
    return [
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

# retrieves the rotations schematic for the pyramid
def getPyramidRotations():
    return [
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


# retrieves the schematic for the well
def getWellSchematic(biome):
    plank = biome_block_choice[biome]['plank']
    fence = biome_block_choice[biome]['fence']
    slab = biome_block_choice[biome]['slab']
    # Get wood types based on biome
    # 2D array containing the blocks for each level of the build
    return [
            [["stone_bricks"] * 3,
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


# retrieves the schematic for the cabin
def getCabinSchematic(biome):
    log = biome_block_choice[biome]['log']
    plank = biome_block_choice[biome]['plank']
    door = biome_block_choice[biome]['door']
    slab = biome_block_choice[biome]['slab']
    stairs = biome_block_choice[biome]['stairs']
    # 2D array containing the blocks for each level of the build
    return [
        [["grass_block"] * 11,
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


# retrieves the schematic for the tree
def getTreeSchematic(biome):
    # Get wood types based on biome
    log = biome_block_choice[biome]['wood']
    leaves = biome_block_choice[biome]['leaves']
    # 2D array containing the blocks for each level of the build
    return [
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

# retrieves the schematic for the hut
def getHutSchematic(biome):
    plank = biome_block_choice[biome]['plank']
    log = biome_block_choice[biome]['log']
    door = biome_block_choice[biome]['door']

    # 2D array containing the blocks for each level of the swimming pool
    return [
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


#retrieves the schematic for the small house
def getSmallHouseSchematic(biome):
    plank = biome_block_choice[biome]['plank']
    log = biome_block_choice[biome]['log']
    door = biome_block_choice[biome]['door']

    # 2D array containing the blocks for each level of the swimming pool
    return [
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
        ]
      ]
    