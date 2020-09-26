from PIL import Image
import random

class Painting:
    def __init__(self, canvas, algorithm, seed=None):
        self.canvas = canvas
        self.algorithm = algorithm
        self.seed = seed or random.randint(0, 2048)

        random.seed(seed)


    def paint(self):
        self.algorithm.run(self.canvas)
        image = Image.fromarray(self.canvas.data)
        image.save(f'{self}.png')
        image.show()

    def __str__(self):
        return f'{self.algorithm.__class__.__name__}{self.seed}_({self.canvas.height}x{self.canvas.width})'
