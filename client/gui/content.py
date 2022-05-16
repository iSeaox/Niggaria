class Content:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, texture_handler):
        raise NotImplementedError("render() has to be implemented in subclasses")
