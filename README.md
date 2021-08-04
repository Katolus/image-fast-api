# Image processing API build with FastAPI
An simple, filesystem based image processing API build on top of the [FastAPI](https://fastapi.tiangolo.com/) framework. The purpose of this project is to display an API building expertise while researching the capabilities of a very promising library. 


## Goals 

I wanted to create an **API** capable of handling images via **POST** and **GET** requests. 

 - `POST "/images/"` is capable of receiving image files and returning its a unique `id`.

 - `GET "/images/:id?w=xx&h=xx"` is capable of returning images stored in the filesystem. It takes **3** arguments where
    - `id` is the reference id of the image previously stored via POST requests.
    - `w` if specified is the width of an image to be returned.
    - `h` if specified is the height of an image to be returned.

   Additionally if only one of the optional (`w` or `h`) parameters is missing then the other will need to be calculated per ratio of the one provided, following this formula.

$$
    h = (w/image.width) * image.height
$$


## System Environment

- Python >= 3.9 (**3.9.6** recommended).
- `FastAPI` requires you to have a **Rust** bundler/compiler when installing a `venv` environment.

## Setup

1. Create a virtual environment by running `python -m venv venv` in your root directory. 
2. Install required packages by running `venv/bin/pip install -r requirements.txt`. 


## Running the server locally

In a `venv` shell run `uvicorn server:app --reload`. 
Given no errors, the server should be available per default configuration on http://127.0.0.1:8000. Go to `http://127.0.0.1:8000/docs` to see the implemented endpoints.