from enum import Enum

import utils.serializable as serializable

import world.world as world
import world.biome.biome as biome

OCEAN_HEIGHT = 200


class BiomeType(Enum):
    OCEAN = biome.Biome("ocean", [], [], [0, 2], [0, 2], True)
    SAVANNA = biome.Biome("savanna", [], [], [0.55, 2], [1, 2], False)
    DESERT = biome.Biome("desert", [], [], [0, 0.55], [0, 2], False)
    FOREST = biome.Biome("forest", [], [], [1.2, 2], [0, 1], False)
    SHRUBLAND = biome.Biome("shrubland", [], [], [0.55, 1.2], [0, 1], False)


def get_biome_by_name(name):
    for b in BiomeType:
        if b.value.name == name:
            return b


def get_chunk_biome(moisture, temperature, height):
    min_height = world.CHUNK_HEIGHT
    max_height = 0

    for h in height:
        if h < min_height:
            min_height = h

        if h > max_height:
            max_height = h

    if max_height <= OCEAN_HEIGHT:
        return BiomeType.OCEAN
    else:
        avg_moisture = 0
        avg_temperature = 0

        for m in moisture:
            avg_moisture += m
        avg_moisture /= world.CHUNK_WIDTH

        for t in temperature:
            avg_temperature += t
        avg_temperature /= world.CHUNK_WIDTH

        for b in BiomeType:
            if not b.value.is_ocean:
                if b.value.moisture_interval[0] <= avg_moisture < b.value.moisture_interval[1] and b.value.temperature_interval[0] <= avg_temperature < b.value.temperature_interval[1]:
                    return b

    return None
