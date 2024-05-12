import json
import os
import io
from http.client import HTTPException
from io import BytesIO
from fastapi import FastAPI, File

import uvicorn
from PIL import Image
from fastapi.responses import StreamingResponse
from main import segment_everything

app = FastAPI(title="Inference API for Segmentation with SAM ")

def get_image_from_bytes(binary_image: bytes) -> Image:
    """Convert image from bytes to PIL RGB format
    **Args:**
        - **binary_image (bytes):** The binary representation of the image
    **Returns:**
        - **PIL.Image:** The image in PIL RGB format
    """
    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    return input_image

def get_bytes_from_image(image: Image) -> bytes:
    """
    Convert PIL image to Bytes
    Args:
    image (Image): A PIL image instance
    Returns:
    bytes : BytesIO object that contains the image in JPEG format with quality 85
    """
    return_image = io.BytesIO()
    image.save(return_image, format='PNG', quality=85)  # save the image in png format with quality 85
    return_image.seek(0)  # set the pointer to the beginning of the file
    return return_image

@app.post("/segment-image")
async def segment_img(file: bytes = File(...)):
    # get image from bytes
    img = get_image_from_bytes(file)
    seg_img = segment_everything(
        image = img
    )
    # return image in bytes format
    return StreamingResponse(content=get_bytes_from_image(seg_img), media_type="image/png")

if __name__ == '__main__':
    uvicorn.run("api:app", host="0.0.0.0",
                port=8000, reload=True)