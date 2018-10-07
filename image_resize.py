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


def validate_required_arguments(arguments):
    if all(
        (
            arguments.scale is None,
            arguments.width is None,
            arguments.height is None,
        )
    ):
        argparse.ArgumentParser().error("No arguments provided")


def validate_compatible_arguments(arguments):
    if arguments.scale is not None and (
        arguments.width is not None or arguments.height is not None
    ):
        raise argparse.ArgumentTypeError(
            "You should use either width/height or scale option"
        )


def is_positive_number(input_value):
    min_value = 0
    return input_value > min_value


def validate_positive_arguments(arguments):
    if any(
        (
            arguments.scale is not None
            and not is_positive_number(arguments.scale),
            arguments.width is not None
            and not is_positive_number(arguments.width),
            arguments.height is not None
            and not is_positive_number(arguments.height),
        )
    ):
        raise argparse.ArgumentTypeError("Arguments should be positive")


def validate_image_argument(arguments):
    if arguments.image is None:
        raise argparse.ArgumentTypeError("No image file provided")


def validate_existing_file(arguments):
    if not exists(arguments.image):
        raise argparse.ArgumentTypeError("File does not exist")


def validate_not_directory(arguments):
    if isdir(arguments.image):
        raise argparse.ArgumentTypeError("Directories is not allowed")


def validate_arguments(arguments):
    validate_image_argument(arguments)
    validate_existing_file(arguments)
    validate_not_directory(arguments)
    validate_required_arguments(arguments)
    validate_compatible_arguments(arguments)
    validate_positive_arguments(arguments)


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


def calculate_dimensions(old_dimensions, width, height, scale):
    if width is not None and height is not None:
        print("Aspect ratio will differ from an existing one")
        new_dimensions = width, height
    elif width is not None and height is None:
        new_dimensions = calculate_dimensions_using_width(
            old_dimensions, width
        )
    elif width is None and height is not None:
        new_dimensions = calculate_dimensions_using_height(
            old_dimensions, height
        )
    else:
        new_dimensions = calculate_dimensions_using_scale(
            old_dimensions, scale
        )
    return new_dimensions


if __name__ == "__main__":
    try:
        arguments = load_arguments()
        validate_arguments(arguments)
        image = Image.open(arguments.image)
        new_dimensions = calculate_dimensions(
            image.size,
            arguments.width,
            arguments.height,
            arguments.scale
        )
        resized_image = image.resize(new_dimensions)
        output_filepath = arguments.output
        if output_filepath is None:
            basename, extension = splitext(arguments.image)
            output_filepath = "{}__{}x{}{}".format(
                basename, resized_image.width, resized_image.height, extension
            )
        resized_image.save(output_filepath)

    except (OSError, argparse.ArgumentTypeError) as error:
        sys.exit(error)
