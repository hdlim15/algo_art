import numpy as np

class Canvas:
    def __init__(self, height=512, width=1024, data=None):
        if data is None:
            data = np.zeros((height, width, 3), dtype=np.uint8)

        self.height = height
        self.width = width
        self.data = data

    def set_background(self, color):
        for y in range(self.height):
            for x in range(self.width):
                self.data[y, x] = color


    def draw_pixel(self, y, x, rgb):
        self.data[y, x] = rgb
        return rgb

    def get_pixel(self, y, x):
        return self.data[y, x]
