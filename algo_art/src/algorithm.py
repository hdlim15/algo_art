import random
import numpy as np

from .utils import random_pixel, near_pixel, random_grayscale, draw_rectangle
from .colors import *
from .palettes import *


class Algorithm:

    def __init__(self, canvas):
        self.canvas = canvas

    def run(self):
        raise NotImplementedError

    def __str__(self):
        return self.name


class RandomNearPixels(Algorithm):

    name = 'random_near_pixels'

    DISTANCE = 15

    def run(self):
        previous_pixel = random_pixel()

        for i in range(self.canvas.height):
            for j in range(self.canvas.width):
                self.canvas.draw_pixel(i, j, near_pixel(previous_pixel, self.DISTANCE))
            previous_pixel = self.canvas.data[i, 0]


class RandomSpiral(Algorithm):
    name = 'random_spiral'

    DISTANCE = 25

    THICKNESS = 15

    def run(self):
        left_column = 0
        top_row = 0

        right_column = self.canvas.width
        bottom_row = self.canvas.height

        previous_pixel = random_pixel()

        while (left_column < right_column and top_row < bottom_row):
            for x in range(left_column, right_column):
                previous_pixel = self.canvas.draw_pixel(top_row, x, near_pixel(previous_pixel, self.DISTANCE))
                for t in range(1, self.THICKNESS):
                    self.canvas.draw_pixel(top_row + t, x, previous_pixel)

            top_row += self.THICKNESS

            for y in range(top_row, bottom_row):
                previous_pixel = self.canvas.draw_pixel(y, right_column - 1, near_pixel(previous_pixel, self.DISTANCE))
                for t in range(1, self.THICKNESS):
                    self.canvas.draw_pixel(y, right_column - 1 - t, previous_pixel)

            right_column -= self.THICKNESS

            for x in range(right_column - 1, left_column - 1, -1):
                previous_pixel = self.canvas.draw_pixel(bottom_row - 1, x, near_pixel(previous_pixel, self.DISTANCE))
                for t in range(1, self.THICKNESS):
                    self.canvas.draw_pixel(bottom_row - 1 - t, x, previous_pixel)

            bottom_row -= self.THICKNESS

            for y in range(bottom_row - 1, top_row - 1, -1):
                previous_pixel = self.canvas.draw_pixel(y, left_column, near_pixel(previous_pixel, self.DISTANCE))
                for t in range(1, self.THICKNESS):
                    self.canvas.draw_pixel(y, left_column + t, previous_pixel)

            left_column += self.THICKNESS


class GrayscaleRectangles(Algorithm):
    name = 'grayscale_rectangles'

    MAX_LENGTH = 500
    MIN_WIDTH = 5
    MAX_WIDTH = 15

    PERCENT_VERTICAL = 0.4

    NUM_RECTANGLES = 30

    def run(self):
        self.canvas.set_background(random_pixel())


        for i in range(self.NUM_RECTANGLES):

            # determine the width and height of the rectangle
            width = random.randint(self.MIN_WIDTH, self.MAX_WIDTH)
            height = random.randint(self.MAX_LENGTH / 2, self.MAX_LENGTH)
            if random.random() > self.PERCENT_VERTICAL:
                width, height = height, width

            # determine the starting point of the rectangle
            y = random.randint(-self.canvas.height / 4, self.canvas.height)
            x = random.randint(-self.canvas.width / 4, self.canvas.width)

            # draw the rectangle
            random_gray = random_grayscale()
            draw_rectangle(y, x, height, width, random_gray, self.canvas)


class SlicedCurves(Algorithm):
    """
    https://res.infoq.com/news/2020/01/solandra-typescript-art/en/resources/1lewitt-1577881245947.png
    """
    name = 'sliced_curves'

    COLORS = (RED, BLUE, YELLOW)

    NUM_CURVES = 20
    NUM_SLICES = 10

    THICKNESS = 5

    def run(self):
        for i in range(self.NUM_CURVES):
            self.draw_curve()

        self.slice_vertically()


    def draw_curve(self):
        start_y = random.randint(0, self.canvas.height - self.THICKNESS - 1)
        end_y = random.randint(0, self.canvas.height - self.THICKNESS)

        x = 0

        while x < self.canvas.width - 1:
            color = random.choice(self.COLORS)
            steepness = random.randint(-4, 4) * 5

            iterations = random.randint(1, 5)

            for _ in range(iterations):
                if x + abs(steepness) < self.canvas.width:
                    length = abs(steepness)
                else:
                    length = self.canvas.width - x

                draw_rectangle(start_y, x, self.THICKNESS, length, color, self.canvas)

                x += length
                start_y = start_y + np.sign(steepness) * self.THICKNESS



    def slice_vertically(self):
        pass


class RecursiveSquares(Algorithm):
    name = 'recursive_squares'

    COLORS = PALETTE_4

    def validate_point(self, y, x):
        for square in self.covered_space:
            if (
                y >= square[0] - 3
                and y <= square[0] + square[2] + 3
                and x >= square[1] - 3
                and x <= square[1] + square[2] + 3
            ):
                return False

        return True

    def draw_square(self, start_y, start_x, length, color):
        if (
            not self.validate_point(start_y, start_x)
            or not self.validate_point(start_y + length, start_x)
            or not self.validate_point(start_y, start_x + length)
            or not self.validate_point(start_y + length, start_x + length)
        ):
            return False

        draw_rectangle(start_y, start_x, length, length, color, self.canvas)
        self.covered_space.append([start_y, start_x, length])
        return True

    def run(self):
        height = self.canvas.height
        width = self.canvas.width

        LARGEST_SIDE = min(height, width) // 7
        NUM_SQUARES = [4, 14, 50, 50, 100]

        # Set the background color. No squares have yet been drawn
        self.canvas.set_background(self.COLORS[0])
        self.covered_space = []

        # Calculate the offset from the top and bottom so that the squares all fit neatly on their grids
        y_offset = (height - (height // LARGEST_SIDE * LARGEST_SIDE)) // 2
        x_offset = (width - (width // LARGEST_SIDE * LARGEST_SIDE)) // 2

        # Readjust offset if it's too small
        if y_offset < LARGEST_SIDE / 2:
            y_offset += LARGEST_SIDE // 2

        if x_offset < LARGEST_SIDE / 2:
            x_offset += LARGEST_SIDE // 2


        for index, num_squares in enumerate(NUM_SQUARES):
            drawn = 0
            side_length = LARGEST_SIDE // (2 ** index)

            while drawn < num_squares:
                start_y = random.randrange(y_offset, height - y_offset - side_length, side_length)
                start_x = random.randrange(x_offset, width - x_offset - side_length, side_length)

                success = self.draw_square(start_y, start_x, side_length, self.COLORS[drawn % 4 + 1])

                if success:
                    if start_x + side_length > 1020:
                        print(start_x)
                        print(side_length)
                        print(index)
                    drawn += 1
