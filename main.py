import argparse

from canvas import Canvas
from algorithm import *
from painting import Painting


ALGORITHM_MAP = {
    'random_pixels': RandomPixels,
    'random_near_pixels': RandomNearPixels,
    'quadrant': Quadrant,
    'random_spiral': RandomSpiral,
    'grayscale_rectangles': GrayscaleRectangles,
    'sliced_curves': SlicedCurves,
}



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--algorithm", help="Algorithm name")
    parser.add_argument("-s", "--seed", help="Random seed", type=int)
    parser.add_argument("-y", "--height", help="Canvas height", type=int, default=768)
    parser.add_argument("-x", "--width", help="Canvas width", type=int, default=1024)

    args = parser.parse_args()

    if args.algorithm not in ALGORITHM_MAP:
        print(f'Could not find algorithm {args.algorithm}')
        exit(1)

    algorithm = ALGORITHM_MAP[args.algorithm]()
    canvas = Canvas(args.height, args.width)
    painting = Painting(canvas, algorithm, args.seed)
    painting.paint()


if __name__ == '__main__':
    main()
