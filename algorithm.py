import random
import numpy as np

from utils import random_pixel, near_pixel, random_grayscale, draw_rectangle
from colors import *


class Algorithm:

    def __init__(self, canvas):
        self.canvas = canvas

    def run(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class RandomPixels(Algorithm):

    def run(self):
        for i in range(self.canvas.height):
            for j in range(self.canvas.width):
                self.canvas.draw_pixel(i, j, random_pixel())

    def __str__(self):
        return 'random_pixels'


class RandomNearPixels(Algorithm):

    DISTANCE = 15

    def run(self):
        previous_pixel = random_pixel()

        for i in range(self.canvas.height):
            for j in range(self.canvas.width):
                self.canvas.draw_pixel(i, j, near_pixel(previous_pixel, self.DISTANCE))
            previous_pixel = self.canvas.data[i, 0]

    def __str__(self):
        return 'random_near_pixels'


class Quadrant(Algorithm):

    def run(self):
        midpoint_y = self.canvas.height / 2
        midpoint_x = self.canvas.width / 2

        for i in range(self.canvas.height):
            for j in range(self.canvas.width):
                if i < midpoint_y:
                    if j < midpoint_x:
                        self.canvas.draw_pixel(i, j, RED)
                    else:
                        self.canvas.draw_pixel(i, j, GREEN)
                else:
                    if j < midpoint_x:
                        self.canvas.draw_pixel(i, j, BLUE)
                    else:
                        self.canvas.draw_pixel(i, j, WHITE)

    def __str__(self):
        return 'quadrant'


class RandomSpiral(Algorithm):
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

    def __str__(self):
        return 'random_spiral'


class GrayscaleRectangles(Algorithm):

    MAX_LENGTH = 500
    MIN_WIDTH = 5
    MAX_WIDTH = 15

    PERCENT_VERTICAL = 0.3

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
            y = random.randint(0, self.canvas.height) - self.canvas.height // 2
            x = random.randint(0, self.canvas.width) - self.canvas.width // 2

            # draw the rectangle
            random_gray = random_grayscale()
            draw_rectangle(y, y + height, x, x + width, random_gray, self.canvas)

    def __str__(self):
        return 'grayscale_rectangles'


class SlicedCurves(Algorithm):
    """
    https://res.infoq.com/news/2020/01/solandra-typescript-art/en/resources/1lewitt-1577881245947.png
    """

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

        color = random.choice(self.COLORS)
        while x < self.canvas.width - 1:
            steepness = random.randint(-4, 4) * 5

            iterations = random.randint(1, 5)

            for _ in range(iterations):
                if x + abs(steepness) < self.canvas.width:
                    length = abs(steepness)
                else:
                    length = self.canvas.width - x

                draw_rectangle(start_y, start_y + self.THICKNESS, x, x + length, color, self.canvas)

                x += length
                start_y = start_y + np.sign(steepness) * self.THICKNESS



    def slice_vertically(self):
        pass

    def __str__(self):
        return 'sliced_curves'
