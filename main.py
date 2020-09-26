from canvas import Canvas
from algorithm import *
from painting import Painting


def main():
    canvas = Canvas()
    algorithm = SlicedCurves()
    painting = Painting(canvas, algorithm)
    painting.paint()


if __name__ == '__main__':
    main()
