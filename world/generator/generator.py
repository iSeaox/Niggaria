import abc


class Generator(abc.ABC):
    def __init__(self, noise):
        self.noise = noise

    def gen(self, world, **kwargs):
        pass
