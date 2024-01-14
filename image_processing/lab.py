"""
6.101 Lab 1:
Image Processing
"""

#!/usr/bin/env python3

import math

from PIL import Image

# NO ADDITIONAL IMPORTS ALLOWED!


def get_pixel(image, row, col):
    return image["pixels"][col, row]


def set_pixel(image, row, col, color):
    image["pixels"][row, col] = color


def apply_per_pixel(image, func):
    result = {
        "height": image["height"],
        "widht": image["width"],
        "pixels": [],
    }
    for col in range(image["height"]):
        for row in range(image["width"]):
            color = get_pixel(image, col, row)
            new_color = func(color)
        set_pixel(result, row, col, new_color)
    return result


def inverted(image):
    ret_im = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"][:],
    }
    for i in range(len(ret_im["pixels"])):
        pixel = ret_im["pixels"][i]
        difference = 127.5 - pixel
        ret_im["pixels"][i] = round(127.5 + difference)

    return ret_im


# HELPER FUNCTIONS

# defines image
def defineImage(image):
    output = {}
    output["height"] = image["height"]
    output["width"] = image["width"]
    output["pixels"] = image["pixels"].copy()
    return output

# multiplies kernel and temp_array


def mult_kernel(arr, kernel):
    sum = 0
    for i in range(len(kernel)):
        for j in range(len(kernel[0])):
            sum += kernel[i][j] * arr[i][j]
    return sum

# gets extended value at certain index outside of regular image


def getExtend(x, y, image):
    row, col = y, x
    if x < 0:
        col = 0
    elif x >= image["width"]:
        col = image["width"] - 1
    if y < 0:
        row = 0
    elif y >= image["height"]:
        row = image["height"] - 1

    return image["pixels"][(row * image["width"]) + col]

# gets wrapped value at certain index outside of regular image


def getWrap(x, y, image):
    row, col = y, x
    if x < 0:
        col = x + image["width"]
    elif x >= image["width"]:
        col = x - image["width"]
    if y < 0:
        row = y + image["height"]
    elif y >= image["height"]:
        row = y - image["height"]

    return image["pixels"][(row * image["width"]) + col]

# returns blur kernel (all cells are equal and add up to one)


def getBlurKernel(kernel_size):
    w, h = kernel_size, kernel_size
    kernel = [[0 for x in range(w)] for y in range(h)]
    for i in range(kernel_size):
        for j in range(kernel_size):
            kernel[i][j] = 1 / (kernel_size**2)
    return kernel


def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings "zero", "extend", or "wrap",
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of "zero", "extend", or "wrap", return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with "height", "width", and "pixels" keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    Kernel Representation: 2D List
    """
    correlate_im = defineImage(image)

    for i in range(image["height"]):
        for j in range(image["width"]):
            index = (i * image["width"]) + j
            # shows what kernel is overlapping with
            w, h = len(kernel), len(kernel)
            # holds values that overlap with kernel
            temp_arr = [[0 for x in range(w)] for y in range(h)]
            # indexes of out of bounds values from the perspective of image
            x = j - (len(kernel) // 2)
            y = i - (len(kernel) // 2)
            for r in range(len(kernel)):
                # update x
                x = j - (len(kernel) // 2)
                for c in range(len(kernel[0])):
                    temp_index = (y * image["width"]) + x
                    if x < 0 or y < 0 or x >= image["width"] or y >= image["height"]:
                        if boundary_behavior == "zero":
                            temp_arr[r][c] = 0
                        elif boundary_behavior == "extend":
                            temp_arr[r][c] = getExtend(x, y, image)
                        elif boundary_behavior == "wrap":
                            temp_arr[r][c] = getWrap(x, y, image)
                    else:
                        temp_arr[r][c] = image["pixels"][temp_index]
                    x += 1
                y += 1
            correlate_im["pixels"][index] = mult_kernel(temp_arr, kernel)

    return correlate_im


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the "pixels" list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    for i in range(len(image["pixels"])):
        image["pixels"][i] = round(image["pixels"][i])
        if image["pixels"][i] < 0:
            image["pixels"][i] = 0
        elif image["pixels"][i] > 255:
            image["pixels"][i] = 255


# FILTERS


def blurred(image, kernel_size):
    """
    Return a new image representing the result of applying a box blur (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)

    kernel = getBlurKernel(kernel_size)

    blurred_im = defineImage(image)
    # then compute the correlation of the input image with that kernel
    blurred_im = correlate(image, kernel, "extend")
    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    round_and_clip_image(blurred_im)
    return blurred_im


def sharpened(image, n):
    '''
    Returns a new image that is the result of putting both a blurred and a regular form of an image in a sharpened
    equation. 

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    '''
    image_blurred = blurred(image, n)
    sharpened_im = defineImage(image)

    for i in range(len(image["pixels"])):
        sharpened_im["pixels"][i] = (
            2 * (image["pixels"][i]) - image_blurred["pixels"][i]
        )
    round_and_clip_image(sharpened_im)

    return sharpened_im


def edges(image):
    '''
    Returns the result of applying correlations with different kernels on
    the same image and putting it through a function, resulting in an image
    with strong outlines of objects.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    '''
    edges_im = defineImage(image)
    kernel_one = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    kernel_two = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    output_one = correlate(image, kernel_one, "extend")
    output_two = correlate(image, kernel_two, "extend")

    for i in range(len(image["pixels"])):
        edges_im["pixels"][i] = round(
            math.sqrt(output_one["pixels"][i] ** 2 +
                      output_two["pixels"][i] ** 2)
        )

    round_and_clip_image(edges_im)
    return edges_im


# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image("test_images/cat.png")
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the "mode" parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    # bluegill = load_greyscale_image("test_images/bluegill.png")
    # save_greyscale_image(inverted(bluegill), "invert_bluegill.png")

    pixel = load_greyscale_image("test_images/centered_pixel.png")
    blob = load_greyscale_image("test_images/blob.png")
    pigbird = load_greyscale_image("test_images/pigbird.png")
    cat = load_greyscale_image("test_images/cat.png")
    python = load_greyscale_image("test_images/python.png")
    construct = load_greyscale_image("test_images/construct.png")

    w, h = 13, 13
    kernel = [[0 for x in range(w)] for y in range(h)]
    for i in range(len(kernel)):
        for j in range(len(kernel[0])):
            if i == 2 and j == 0:
                kernel[i][j] = 1
            else:
                kernel[i][j] = 0

    temp_arr = [[0] * len(kernel)] * len(kernel)
    # pixel = correlate(pixel, kernel, "zero")
    # blob = correlate(blob, kernel, "zero")
    # pigbird = correlate(pigbird, kernel, "wrap")
    # round_and_clip_image(pigbird)
    # save_greyscale_image(pigbird, "pigbird_wrap.png")
    # pixel = blurred(pixel, 3)
    # save_greyscale_image(pixel, "pixel_blur.png")

    # cat = blurred(cat, 13)
    # save_greyscale_image(cat, "cat_blur.png")

    # python = sharpened(python, 11)
    # save_greyscale_image(python, "python_sharp.png")

    construct = edges(construct)
    save_greyscale_image(construct, "construct_edge.png")
