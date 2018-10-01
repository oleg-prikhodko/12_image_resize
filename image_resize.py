import argparse
import os.path
import sys
from functools import partial

from PIL import Image


def resize_image(path_to_original, width=None, height=None, scale=None):
    image = Image.open(path_to_original)
    resized_image = None
    if width is not None and height is not None:
        if image.width / image.height != width / height:
            print("Aspect ratio will differ from an existing one")
        resized_image = image.resize((width, height))
    elif width is not None and height is None:
        scale = width / image.width
        resized_image = image.resize((width, int(image.height * scale)))
    elif width is None and height is not None:
        scale = height / image.height
        resized_image = image.resize((int(image.width * scale), height))
    elif width is None and height is None and scale is not None:
        resized_image = image.resize(
            (int(image.width * scale), int(image.height * scale))
        )
    else:
        return image
    return resized_image


def positive_finite_number(numeric_type, value):
    numeric_value = numeric_type(value)
    min_value = 0
    max_value = 10000
    if numeric_value <= min_value:
        raise argparse.ArgumentTypeError(
            "{} is not a positive number".format(value)
        )
    elif numeric_value > max_value:
        raise argparse.ArgumentTypeError(
            "{} should not be more than {}".format(value, max_value)
        )
    return numeric_value


positive_finite_int = partial(positive_finite_number, int)
positive_finite_float = partial(positive_finite_number, float)


def load_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", nargs="?")
    parser.add_argument("-W", "--width", type=positive_finite_int)
    parser.add_argument("-H", "--height", type=positive_finite_int)
    parser.add_argument("-S", "--scale", type=positive_finite_float)
    parser.add_argument("-O", "--output")
    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":
    try:
        arguments = load_arguments()
        if arguments.scale is not None and (
            arguments.width is not None or arguments.height is not None
        ):
            sys.exit("You should use either width and height or scale option")

        resized_image = resize_image(
            arguments.image, arguments.width, arguments.height, arguments.scale
        )
        if arguments.output is None:
            basename, extension = arguments.image.rsplit(".", maxsplit=1)
            output_filepath = "{}__{}x{}.{}".format(
                basename, resized_image.width, resized_image.height, extension
            )
            resized_image.save(output_filepath)
        else:
            resized_image.save(arguments.output)
    except FileNotFoundError:
        sys.exit("Image file not found")
    except OSError as error:
        sys.exit(error)
