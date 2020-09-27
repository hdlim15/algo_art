from os import mkdir
from PIL import Image
import random

class Painting:
    def __init__(self, algorithm, seed=None):
        self.algorithm = algorithm
        self.seed = seed or random.randint(0, 2048)

        random.seed(seed)

    def paint(self):
        self.algorithm.run()
        image = Image.fromarray(self.algorithm.canvas.data)
        self.save_painting_to_file(image)

    def save_painting_to_file(self, image):
        try:
            mkdir(f'paintings/{self.algorithm}')
        except FileExistsError:
            pass

        image.save(f'paintings/{self.algorithm}/{self}.png')
        image.show()

    def __str__(self):
        return f'{self.algorithm}_{self.seed}'
