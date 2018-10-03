import argparse
import sys
from functools import partial

from PIL import Image


def resize_image(image_file, width, height, scale):
    image = Image.open(image_file)
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
    elif scale is not None:
        resized_image = image.resize(
            (int(image.width * scale), int(image.height * scale))
        )
    else:
        return image
    return resized_image


def positive_finite_number(numeric_type, input_value):
    numeric_value = numeric_type(input_value)
    min_value = 0
    max_value = 10000
    if numeric_value <= min_value:
        raise argparse.ArgumentTypeError(
            "{} is not a positive number".format(input_value)
        )
    elif numeric_value > max_value:
        raise argparse.ArgumentTypeError(
            "{} should not be more than {}".format(input_value, max_value)
        )
    return numeric_value


positive_finite_int = partial(positive_finite_number, int)
positive_finite_float = partial(positive_finite_number, float)


def load_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", nargs="?", type=argparse.FileType(mode="rb"))
    parser.add_argument("-W", "--width", type=positive_finite_int)
    parser.add_argument("-H", "--height", type=positive_finite_int)
    parser.add_argument("-S", "--scale", type=positive_finite_float)
    parser.add_argument("-O", "--output")
    arguments = parser.parse_args()

    if arguments.image is None:
        raise ValueError("No image file provided")
    elif arguments.scale is not None and (
        arguments.width is not None or arguments.height is not None
    ):
        raise ValueError("You should use either width/height or scale option")

    return arguments


if __name__ == "__main__":
    try:
        arguments = load_arguments()
        resized_image = resize_image(
            arguments.image, arguments.width, arguments.height, arguments.scale
        )
        if arguments.output is None:
            basename, extension = arguments.image.name.rsplit(".", maxsplit=1)
            output_filepath = "{}__{}x{}.{}".format(
                basename, resized_image.width, resized_image.height, extension
            )
            resized_image.save(output_filepath)
        else:
            resized_image.save(arguments.output)
    except (ValueError, OSError) as error:
        sys.exit(error)
