"""Holds implementations of all the validation logic."""
from typing import List

from fastapi import UploadFile

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
