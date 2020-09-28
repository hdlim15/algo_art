import argparse

from .canvas import Canvas
from .algorithm import Algorithm
from .painting import Painting


ALGORITHM_MAP = {algo.name: algo for algo in Algorithm.__subclasses__()}

def main(algorithm, seed=None, height=768, width=1024):
    if algorithm not in ALGORITHM_MAP:
        print(f'Could not find algorithm {algorithm}')
        exit(1)

    canvas = Canvas(height, width)
    algorithm = ALGORITHM_MAP[algorithm](canvas)
    painting = Painting(algorithm, seed)
    return painting.paint()
