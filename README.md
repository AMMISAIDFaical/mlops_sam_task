# Segment_Anything_Model-FastAPI:
This repository serves as a template for segmentation using SAM and FastAPI. 
With SAM, you get a popular Multi-Segmentation model and with FastAPI, 
you get a modern, fast (high-performance) web framework for building APIs. 
The project also includes Docker, a platform for easily building, shipping, and running distributed applications.

### Sample
Here's a sample of what you can expect to see with this project:
<img width=600 src="./resources/dog.jpg" alt="sample example of the results of SAM segmentation">

# Getting Started
You have two options to start the application: using Docker or locally on your machine.

## Using Docker
after cloning the repo and making sure docker working properly and starting it (docker deamon) we just need to build 
Dockerfile "docker build -t sam-ss-prod ." then we need to run the container with command docker run -d -p 8000:8000 sam-ss-prod   
in case of everything went well,  you should access swagger ui http://localhost:8000/docs#/ :
```
docker build -t sam-ss-prod .         
docker run -d -p 8000:8000 sam-ss-prod
```

## Locally
To start the application locally, follow these steps:

1. Install the required packages:

```
pip install -r requirements.txt
```
2. Start the application:
```
run the api.py 
```  
* Doing that you will get link that you need to append to it '/docs#' so that you can get swagger GUI so you can interact
with the model :
by uploading you own image and executing you need to consider a 3 to 5 min waiting for the response (depending on the
machine and assuming that you will use the cpu "my machine mine took 4 min" ) 
* 
### FASTAPI Docs url:
http://localhost:8000/docs#/

<img width=600 src="./generated/Screenshot_te_segmentation.png" alt="FASTAPI">    

---
# Code Breakdown
We will focus on the new added file api.py as the rest of the code was provided by spacesense mlops team
### Byte file to image converting method   

```python
from PIL import Image
import io
def get_image_from_bytes(binary_image: bytes) -> Image:
    """Convert image from bytes to PIL RGB format
    **Args:**
        - **binary_image (bytes):** The binary representation of the image
    **Returns:**
        - **PIL.Image:** The image in PIL RGB format
    """
    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    return input_image
```

### Image to Byte file to  converting method    

```python
from PIL import Image
import io

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
```

### Segmentation method integrated in post http request 
This code globes the previous functions and also the post methode that calls sam function def in main
and returns streaming response.

```python
import io
from fastapi import FastAPI, File
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
    return StreamingResponse(content=get_bytes_from_image(seg_img), media_type="image/jpeg")
```

---

# Overview of the code
* [main.py](./main.py) - Base SAM implementation method and run saves result in /generated   
* [app.py](./api.py) - FASTAPI functions and api endpoints def     
* [tools.py](tools.py) - SAM helper functions
---
# Attention:
if you succeeded in cloning the repository and running docker and getting the localhost/8000 port working and also you
have been able to see the swagger gui that's is would be perfect whoever if you uploaded file (image) and executed 
the request will take 5 to 4 min if you have cpu so if everything went well you will receive you image segmented after
that period of time.
