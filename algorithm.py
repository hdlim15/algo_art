import random
import numpy as np

from utils import random_pixel, near_pixel, random_grayscale, draw_rectangle
from colors import *


class Algorithm:

    def run(self, canvas):
        raise NotImplementedError



class RandomPixels(Algorithm):

    def run(self, canvas):
        for i in range(canvas.height):
            for j in range(canvas.width):
                canvas.draw_pixel(i, j, random_pixel())


class RandomNearPixels(Algorithm):

    DISTANCE = 15

    def run(self, canvas):
        previous_pixel = random_pixel()

        for i in range(canvas.height):
            for j in range(canvas.width):
                canvas.draw_pixel(i, j, near_pixel(previous_pixel, self.DISTANCE))
            previous_pixel = canvas.data[i, 0]


class Quadrant(Algorithm):

    def run(self, canvas):
        midpoint_y = canvas.height / 2
        midpoint_x = canvas.width / 2

        for i in range(canvas.height):
            for j in range(canvas.width):
                if i < midpoint_y:
                    if j < midpoint_x:
                        canvas.draw_pixel(i, j, RED)
                    else:
                        canvas.draw_pixel(i, j, GREEN)
                else:
                    if j < midpoint_x:
                        canvas.draw_pixel(i, j, BLUE)
                    else:
                        canvas.draw_pixel(i, j, WHITE)


class RandomSpiral(Algorithm):
    DISTANCE = 25

    THICKNESS = 15

    def run(self, canvas):
        left_column = 0
        top_row = 0

        right_column = canvas.width
        bottom_row = canvas.height

        previous_pixel = random_pixel()

        while (left_column < right_column and top_row < bottom_row):
            for x in range(left_column, right_column):
                previous_pixel = canvas.draw_pixel(top_row, x, near_pixel(previous_pixel, self.DISTANCE))
                for t in range(1, self.THICKNESS):
                    canvas.draw_pixel(top_row + t, x, previous_pixel)

            top_row += self.THICKNESS

            for y in range(top_row, bottom_row):
                previous_pixel = canvas.draw_pixel(y, right_column - 1, near_pixel(previous_pixel, self.DISTANCE))
                for t in range(1, self.THICKNESS):
                    canvas.draw_pixel(y, right_column - 1 - t, previous_pixel)

            right_column -= self.THICKNESS

            for x in range(right_column - 1, left_column - 1, -1):
                previous_pixel = canvas.draw_pixel(bottom_row - 1, x, near_pixel(previous_pixel, self.DISTANCE))
                for t in range(1, self.THICKNESS):
                    canvas.draw_pixel(bottom_row - 1 - t, x, previous_pixel)

            bottom_row -= self.THICKNESS

            for y in range(bottom_row - 1, top_row - 1, -1):
                previous_pixel = canvas.draw_pixel(y, left_column, near_pixel(previous_pixel, self.DISTANCE))
                for t in range(1, self.THICKNESS):
                    canvas.draw_pixel(y, left_column + t, previous_pixel)

            left_column += self.THICKNESS


class GrayscaleRectangles(Algorithm):

    MAX_LENGTH = 500
    MIN_WIDTH = 5
    MAX_WIDTH = 15

    PERCENT_VERTICAL = 0.3

    NUM_RECTANGLES = 30

    def run(self, canvas):
        canvas.set_background(random_pixel())


        for i in range(self.NUM_RECTANGLES):

            # determine the width and height of the rectangle
            width = random.randint(self.MIN_WIDTH, self.MAX_WIDTH)
            height = random.randint(self.MAX_LENGTH / 2, self.MAX_LENGTH)
            if random.random() > self.PERCENT_VERTICAL:
                width, height = height, width

            # determine the starting point of the rectangle
            y, x = random.randint(0, canvas.height) - canvas.height // 2, random.randint(0, canvas.width) - canvas.width // 2

            # draw the rectangle
            random_gray = random_grayscale()
            draw_rectangle(y, y + height, x, x + width, random_gray, canvas)


class SlicedCurves(Algorithm):
    """
    https://res.infoq.com/news/2020/01/solandra-typescript-art/en/resources/1lewitt-1577881245947.png
    """

    COLORS = (RED, BLUE, YELLOW)

    NUM_CURVES = 20
    NUM_SLICES = 10

    THICKNESS = 5

    def run(self, canvas):
        for i in range(self.NUM_CURVES):
            self.draw_curve(canvas)

        self.slice_vertically()


    def draw_curve(self, canvas):
        start_y = random.randint(0, canvas.height - self.THICKNESS - 1)
        end_y = random.randint(0, canvas.height - self.THICKNESS)

        x = 0


        while x < canvas.width - 1:
            color = random.choice(self.COLORS)
            steepness = random.randint(-4, 4) * 5
            # steepness = random.randint(-10, 10)
            # distance = random.randint(50, 300)

            # distance_covered = 0

            if x + abs(steepness) < canvas.width:
                length = abs(steepness)
            else:
                length = canvas.width - x

            draw_rectangle(start_y, start_y + self.THICKNESS, x, x + length, color, canvas)

            x += length
            start_y = start_y + np.sign(steepness) * self.THICKNESS



    def slice_vertically(self):
        pass







