"""Holds implementations of all the validation logic."""
from fastapi import UploadFile
from PIL import Image

from images import ImageContentType
from errors import BadRequest
from errors import UnsupportedMediaTypeError


def validate_image(image: UploadFile):
    """
    Validate image for required attributes.
    """
    if image.content_type not in ImageContentType.valid_types:
        raise UnsupportedMediaTypeError(
            f"Error: Image - {image.filename} content type ({image.content_type}) is not supported"
        )


def validate_query_params(image: Image, width: int, height: int):
    """Validate width and height image params"""
    if not width and not height:
        raise BadRequest(
            "Error: Either `width` or `height` must passed into the function"
        )

    if width:
        if width <= 0:
            raise BadRequest(f"Error: Width needs to be above `0`")

        if width > image.width:
            raise BadRequest(
                f"Error: Width cannot be larged that the width ({image.width}) of a selected image"
            )

    if height:
        if height <= 0:
            raise BadRequest(f"Error: Height needs to be above `0`")

        if height > image.height:
            raise BadRequest(
                f"Error: Height cannot be larged that the height ({image.height}) of a selected image"
            )
