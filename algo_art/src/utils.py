import random

def inbounds_y(y, canvas):
    """
    Returns a value for y that is guaranteed to be within bounds of the canvas
    """
    return min(max(y, 0), canvas.height - 1)

def inbounds_x(x, canvas):
    """
    Returns a value for x that is guaranteed to be within bounds of the canvas
    """
    return min(max(x, 0), canvas.width - 1)

def random_pixel():
    """
    Returns a pixel with a random RGB value.
    """
    return [random.randint(0,255), random.randint(0,255), random.randint(0,255)]

def random_grayscale():
    """
    Returns a random grayscale pixel
    """
    grayness = random.randint(0,255)
    return [grayness] * 3



def near_pixel(pixel, distance):
    """
    Returns a pixel that is similar to another pixel
    """
    red_delta = random.randint(-distance, distance)
    green_delta = random.randint(-distance, distance)
    blue_delta = random.randint(-distance, distance)

    new_red = min(255, max(0, pixel[0] + red_delta))
    new_green = min(255, max(0, pixel[1] + green_delta))
    new_blue = min(255, max(0, pixel[2] + blue_delta))

    return [new_red, new_green, new_blue]


def draw_rectangle(start_y, start_x, height, width, color, canvas):
    for i in range(inbounds_y(start_y, canvas), inbounds_y(start_y + height, canvas)):
        for j in range(inbounds_x(start_x, canvas), inbounds_x(start_x + width, canvas)):
            canvas.draw_pixel(i, j, color)
