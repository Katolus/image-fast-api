"""Stores all the logic responsible to running a FastAPI server"""
import io
from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import Response
from fastapi import UploadFile
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
from PIL import Image

from errors import BadRequest
from errors import UnsupportedMediaTypeError
from images import get_format_from_extension
from images import get_media_type_from_extension
from images import resize_image
from storage import search_image
from storage import store_image
from validators import validate_image
from validators import validate_query_params

app = FastAPI()


@app.exception_handler(UnsupportedMediaTypeError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=415)


@app.exception_handler(BadRequest)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.post("/images/")
async def post_images(image: UploadFile = File(...)):
    """
    Accepts `JPEG`, `JPG` and `PNG` images and stores them in disk space.

    Returns an `image_id` value when successful.

    Returns a `415` [Unsupported Media Type] response if the file wasn't in a correct format.
    """
    validate_image(image)
    image_id: str = store_image(image)

    return JSONResponse(content={"image_id": image_id}, status_code=201)


@app.get("/images/{id}")
async def get_images(id: str, w: int = None, h: int = None):
    """
    Accepts `id` as a URL argument and two additional query parameters: `w` and `h`.

    - `id` - unique identifier of an image.
    - `w` - new width of a image returned.
    - `h` - new height of a image returned.

    Returns a resized image (given the query parameters) if `id` matches a stored image.

    Returns a `NotFound` message if the `id` doesn't match any existing images.

    Returns a `400` Bad Request when invalid query parameters are passed in.
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
                validate_query_params(image, w, h)
                image = resize_image(image, w, h)

            image.save(response_bytes, format=image_format)

        return Response(content=response_bytes.getvalue(), media_type=image_media_type)
    finally:
        response_bytes.close()
