"""Holds implementations of all the validation logic."""
from typing import List

from fastapi import UploadFile
from PIL import Image

from errors import ValidationError


class ImageContentTypeError(ValidationError):
    """Invalid content type of an image."""

    pass


class ImageContentType:
    JPEG = "image/jpeg"
    PNG = "image/png"

    @classmethod
    @property
    def valid_types(cls) -> List[str]:
        return [cls.JPEG, cls.PNG]


def validate_image(image: UploadFile):
    """
    Validate image for required attributes.
    """
    if image.content_type not in ImageContentType.valid_types:
        raise ImageContentTypeError(
            f"Image - {image.filename} content type ({image.content_type}) is not supported"
        )


def validate_query_params(image: Image, width: int, height: int):
    """Validate width and height image params"""
    if not width and not height:
        raise ValidationError(
            "Either `width` or `height` must passed into the function"
        )

    if width <= 0:
        raise ValidationError(f"Width needs to be above `0`")

    if width > image.width:
        raise ValidationError(
            f"Width cannot be larged that the width ({image.width}) of a selected image"
        )

    if height <= 0:
        raise ValidationError(f"Height needs to be above `0`")

    if height > image.height:
        raise ValidationError(
            f"Height cannot be larged that the height ({image.height}) of a selected image"
        )
