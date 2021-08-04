"""Stores all the logic defining how to store items."""
import datetime
import hashlib
import os
from typing import List
from typing import Tuple

from fastapi import UploadFile

from settings import IMAGE_DIRECTORY


def ensure_directory_exists(dir_path: str):
    """Creates a directory under a `dir_path` if it does not exist."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_extension_from_image(image: UploadFile) -> str:
    """Returns an extension from an upload image file dogs.jpg -> .jpg"""
    return os.path.splitext(image.filename)[1]


def save_image_on_disk(image: UploadFile, image_id: str):
    """Write an image to disk."""
    ensure_directory_exists(IMAGE_DIRECTORY)
    image_extension = get_extension_from_image(image)

    with open(
        os.path.join(IMAGE_DIRECTORY, f"{image_id}{image_extension}"), "wb"
    ) as image_file:
        image_file.write(
            image.file.read()
        )  # Read all image's bytes into the `image_file`. u


def generate_image_id(image: UploadFile) -> str:
    """Returns a unique image id in a md5 format"""
    now = datetime.datetime.now()
    h = hashlib.md5()
    h.update(f"{image.filename}_{now}".encode())
    return h.hexdigest()


def filter_images_matching_id(files: List[str], id: str) -> Tuple[str, str]:
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        if file_name == id:
            return file_name, file_extension


def search_image(id, dir_path=IMAGE_DIRECTORY) -> Tuple[str, str]:
    """Searches storage for an image path."""
    for dirpath, dirnames, filenames in os.walk(IMAGE_DIRECTORY):
        image_name, image_extension = filter_images_matching_id(filenames, id)
        if image_name and image_extension:
            return (
                os.path.join(dir_path, f"{image_name}{image_extension}"),
                image_extension,
            )


def store_image(image) -> str:
    """
    Stores and image in a `IMAGE_DIRECTORY` in the current file system.

    It uses a md5 hashing algorithm to ensure that uniqueness of an image id.
    """
    image_id = generate_image_id(image)

    save_image_on_disk(image, image_id)

    return image_id
