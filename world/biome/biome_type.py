from enum import Enum
import world.biome.biome as biome


class BiomeType(Enum):
    OCEAN = biome.Biome("ocean", [], [])