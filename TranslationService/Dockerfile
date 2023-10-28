# Dockerfile, Image, Container
FROM python:3.10

ADD *.py .

# Configure the Linux System
RUN apt update
RUN pip install --upgrade pip
RUN apt-get --yes install libsndfile1

WORKDIR /build

# Download the model
RUN wget "https://huggingface.co/facebook/seamless-m4t-large/resolve/main/multitask_unity_large.pt" /assets/multitask_unity_large.pt
COPY ./assets /build/assets

# Install Python Packages
COPY ./requirements.txt /build/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /build/requirements.txt

# Copy Artifacts
COPY ./src /build


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
