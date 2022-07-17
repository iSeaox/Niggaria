class Biome:
    def __init__(self, name, height_coef, cave_coef, moisture_interval, temperature_interval):
        self.name = name
        self.height_coef = height_coef
        self.cave_coef = cave_coef

        self.moisture_interval = moisture_interval
        self.temperature_interval = temperature_interval
