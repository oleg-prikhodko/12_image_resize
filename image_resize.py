import argparse
import sys
from os.path import exists, isdir, splitext

from PIL import Image


def load_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", nargs="?")
    parser.add_argument("-W", "--width", type=int)
    parser.add_argument("-H", "--height", type=int)
    parser.add_argument("-S", "--scale", type=float)
    parser.add_argument("-O", "--output")
    arguments = parser.parse_args()
    return arguments


def is_positive_number(input_value):
    min_value = 0
    if input_value <= min_value:
        return False
    return True


def validate_arguments(arguments):
    # TODO function cleanup
    if arguments.image is None:
        raise ValueError("No image file provided")
    elif not exists(arguments.image) or isdir(arguments.image):
        raise argparse.ArgumentTypeError("Invalid image file")
    elif (
        splitext(arguments.image)[1].lower() != ".png"
        and splitext(arguments.image)[1].lower() != ".jpg"
    ):
        print(splitext(arguments.image)[1].lower())
        raise argparse.ArgumentTypeError("Invalid image file format")
    elif (
        arguments.scale is None
        and arguments.width is None
        and arguments.height is None
    ):
        raise ValueError("No arguments provided")
    elif arguments.scale is not None and (
        arguments.width is not None or arguments.height is not None
    ):
        raise ValueError("You should use either width/height or scale option")
    elif (
        (
            arguments.scale is not None
            and not is_positive_number(arguments.scale)
        )
        or (
            arguments.width is not None
            and not is_positive_number(arguments.width)
        )
        or (
            arguments.height is not None
            and not is_positive_number(arguments.height)
        )
    ):
        raise argparse.ArgumentTypeError("Arguments should be positive")


def calculate_dimensions_using_width(old_dimensions, new_width):
    old_width, old_height = old_dimensions
    scale_factor = new_width / old_width
    new_height = int(scale_factor * old_height)
    return new_width, new_height


def calculate_dimensions_using_height(old_dimensions, new_height):
    old_width, old_height = old_dimensions
    scale_factor = new_height / old_height
    new_width = int(scale_factor * old_width)
    return new_width, new_height


def calculate_dimensions_using_scale(old_dimensions, scale_factor):
    old_width, old_height = old_dimensions
    new_width = int(scale_factor * old_width)
    new_height = int(scale_factor * old_height)
    return new_width, new_height


if __name__ == "__main__":
    try:
        arguments = load_arguments()
        validate_arguments(arguments)
        image = Image.open(arguments.image)

        if arguments.width is not None and arguments.height is not None:
            print("Aspect ratio will differ from an existing one")
            new_dimensions = arguments.width, arguments.height
        elif arguments.width is not None and arguments.height is None:
            new_dimensions = calculate_dimensions_using_width(
                image.size, arguments.width
            )
        elif arguments.width is None and arguments.height is not None:
            new_dimensions = calculate_dimensions_using_height(
                image.size, arguments.height
            )
        else:
            new_dimensions = calculate_dimensions_using_scale(
                image.size, arguments.scale
            )

        resized_image = image.resize(new_dimensions)
        output_filepath = arguments.output
        if output_filepath is None:
            basename, extension = splitext(arguments.image)
            output_filepath = "{}__{}x{}{}".format(
                basename, resized_image.width, resized_image.height, extension
            )
        resized_image.save(output_filepath)

    except (argparse.ArgumentTypeError, OSError, ValueError) as error:
        sys.exit(error)
