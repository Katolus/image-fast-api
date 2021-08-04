"""Stores all the logic responsible to running a FastAPI server"""
import io
from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import Response
from fastapi import UploadFile
from fastapi.responses import PlainTextResponse
from PIL import Image

from errors import ValidationError
from images import get_format_from_extension
from images import get_media_type_from_extension
from images import resize_image
from storage import search_image
from storage import store_image
from validators import validate_image

app = FastAPI()


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=422)


@app.post("/images/")
async def post_images(image: UploadFile = File(...)):
    """
    Accepts `JPEG` and `PNG` images and stores them.

    Returns an `image_id` value when success.

    Returns a ValidationError when validation fails.
    """
    validate_image(image)
    image_id: str = store_image(image)

    return {"image_id": image_id}


@app.get("/images/{id}")
async def get_images(id: str, w: int = None, h: int = None):
    """
    Accepts `id` as a positional argument and two additional query parameters `w` and `h`.

    - `id` - unique identifier for an an image [required].
    - `w` - width of the image returned.
    - `h` - height of the image returned.

    Returns an image when the `id` matches stored images.
        If the query paramters are valid, the image will be resized accordingly.

        Returns an invalid input error when either of the query parameters doesn't match criteria.

    Returns a NotFound message if the `id` doesn't match any existing images.
    """
    image_path, image_extension = search_image(id)
    if not image_path:
        raise HTTPException(status_code=404, detail=f"Image ({id}) was not found!")

    response_bytes = io.BytesIO()
    image_format = get_format_from_extension(image_extension)
    image_media_type = get_media_type_from_extension(image_extension)

    try:
        with Image.open(image_path) as image:
            if w or h:
                image = resize_image(image, w, h)

            image.save(response_bytes, format=image_format)

        return Response(content=response_bytes.getvalue(), media_type=image_media_type)
    finally:
        response_bytes.close()
