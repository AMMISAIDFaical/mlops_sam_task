FROM tiangolo/uvicorn-gunicorn:python3.11
LABEL authors="Faical"

RUN apt update && \
    apt install -y htop libgl1-mesa-glx libglib2.0-0

# Set the working directory to /app
WORKDIR ./app

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000
COPY ./api .
COPY ./tools.py .
COPY ./main.py .
COPY ./mobile_sam.pt .

# Run api.py when the container launches
CMD ["python", "api.py"]