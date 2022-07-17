class Biome:
    def __init__(self, name, height_coef, cave_coef, moisture_interval, temperature_interval, is_ocean):
        self.name = name
        self.height_coef = height_coef # empty for no change
        self.cave_coef = cave_coef

        self.moisture_interval = moisture_interval
        self.temperature_interval = temperature_interval

        self.is_ocean = is_ocean
