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
    NUM_BIG_SQUARES = 6

    def validate_point(self, y, x):
        for square in self.covered_space:
            if (
                y >= square[0] - 1
                and y <= square[0] + square[2] + 1
                and x >= square[1] - 1
                and x <= square[1] + square[2] + 1
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
        LARGEST_SIDE = 100

        height = self.canvas.height
        width = self.canvas.width

        self.covered_space = []

        self.canvas.set_background(self.COLORS[0])

        y_offset = (height - (height // LARGEST_SIDE * LARGEST_SIDE)) // 2
        x_offset = (width - (width // LARGEST_SIDE * LARGEST_SIDE)) // 2

        if y_offset < LARGEST_SIDE / 2:
            y_offset += LARGEST_SIDE // 2

        if x_offset < LARGEST_SIDE / 2:
            x_offset += LARGEST_SIDE // 2

        # Draw the four large squares in the corners
        # self.draw_square(y_offset, x_offset, LARGEST_SIDE, self.COLORS[1])
        # self.draw_square(y_offset, width - (x_offset + LARGEST_SIDE), LARGEST_SIDE, self.COLORS[3])
        # self.draw_square(height - (y_offset + LARGEST_SIDE), x_offset, LARGEST_SIDE, self.COLORS[2])
        # self.draw_square(height - (y_offset + LARGEST_SIDE), width - (x_offset + LARGEST_SIDE), LARGEST_SIDE, self.COLORS[4])

        drawn = 0
        while drawn < 4:
            start_y = random.randrange(y_offset, height - y_offset, LARGEST_SIDE)
            start_x = random.randrange(x_offset, width - x_offset, LARGEST_SIDE)

            success = self.draw_square(start_y, start_x, LARGEST_SIDE, self.COLORS[drawn % 4 + 1])

            if success:
                drawn += 1


        # next smallest squares
        drawn = 0
        while drawn < 14:
            start_y = random.randrange(y_offset, height - y_offset, LARGEST_SIDE // 2)
            start_x = random.randrange(x_offset, width - x_offset, LARGEST_SIDE // 2)

            success = self.draw_square(start_y, start_x, LARGEST_SIDE // 2, self.COLORS[drawn % 4 + 1])

            if success:
                drawn += 1

        drawn = 0
        while drawn < 50:
            start_y = random.randrange(y_offset, height - y_offset, LARGEST_SIDE // 4)
            start_x = random.randrange(x_offset, width - x_offset, LARGEST_SIDE // 4)

            success = self.draw_square(start_y, start_x, LARGEST_SIDE // 4, self.COLORS[drawn % 4 + 1])

            if success:
                drawn += 1

        drawn = 0
        while drawn < 50:
            start_y = random.randrange(y_offset, height - y_offset, LARGEST_SIDE // 8)
            start_x = random.randrange(x_offset, width - x_offset, LARGEST_SIDE // 8)

            success = self.draw_square(start_y, start_x, LARGEST_SIDE // 8, self.COLORS[drawn % 4 + 1])

            if success:
                drawn += 1

        drawn = 0
        while drawn < 100:
            start_y = random.randrange(y_offset, height - y_offset, LARGEST_SIDE // 16)
            start_x = random.randrange(x_offset, width - x_offset, LARGEST_SIDE // 16)

            success = self.draw_square(start_y, start_x, LARGEST_SIDE // 16, self.COLORS[drawn % 4 + 1])

            if success:
                drawn += 1
