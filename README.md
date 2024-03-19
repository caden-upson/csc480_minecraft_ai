# CSC 480: GDMC Group 1

This project is a part of Professor Rodrigo Canaan's CSC 480 class at Cal Poly. The framework used is the GDPC (Generative Design Python Client) made specifically for the Generative Design in Minecraft competition. This python script is to be run along with the GDMC-HTTP mod for Minecraft.

<<<<<<< HEAD
The best, most up-to-date branch for this repository is the brian3 branch. To get the best results, use brian3 rather than the main branch.

=======
>>>>>>> 04fa55d78d9f564b01269c40d03c7852ceac6157
## Usage

1. Run Minecraft 1.20.0 with GDMC-HTTP mod installed (with Forge)
2. Set the build area using `/setbuildarea ~0 0 ~0 ~64 200 ~64`
3. Run `python settlement.py` to generate a settlement
4. The settlement will be created in Minecraft in front of the player

## Notes

The best results for this generator is to run it in mostly flat terrain. This agent can take in all biomes, including new biomes introduced in Minecraft 1.20, into account when selecting blocks for the settlement. Most of the time running the generator is taken by removing trees from the build area. Specific seeds that feature different, flat environments are best used for this agent.
