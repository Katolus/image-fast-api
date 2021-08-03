"""Stores all the logic responsible to running a FastAPI server"""
from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import PlainTextResponse


from errors import ValidationError
from images import find_image
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
    # Find image
    image = find_image(id)

    # If query paramters passed in the attempt to resize the image

    # If image not found return a NotFound

    # Return the image

    return "This is a GET message"
