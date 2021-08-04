"""Stores the logic specific to images"""
from typing import List

from PIL import Image


class ImageProcessingError(Exception):
    """Error that occurred during process of an image."""

    pass


class ImageContentType:
    JPEG = "image/jpeg"
    PNG = "image/png"

    @classmethod
    @property
    def valid_types(cls) -> List[str]:
        return [cls.JPEG, cls.PNG]


def get_format_from_extension(image_extension: str) -> str:
    """Returns a format from a hard coded map."""
    return {
        ".jpg": "JPEG",
        ".jpeg": "JPEG",
        ".png": "PNG",
    }[image_extension]


def get_media_type_from_extension(image_extension: str) -> str:
    """Returns a media type from a hard coded map."""
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
    }[image_extension]


def calculate_width(image: Image, height: int) -> int:
    return int((height / image.height) * image.width)


def calculate_height(image: Image, width: int) -> int:
    return int((width / image.width) * image.height)


def resize_image(image: Image, width: int = None, height: int = None):
    """
    Resizes image given width or height. Either width or height must be present.

    Calculates a missing one from the ration and one value present.
    """
    if not width and not height:
        ImageProcessingError("Either `width` or `height` must passed into the function")

    width = width or calculate_width(image, height)
    height = height or calculate_height(image, width)

    return image.resize((width, height))
