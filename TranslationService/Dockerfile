# Dockerfile, Image, Container
FROM python:3.10

ADD *.py .


RUN apt update
RUN pip install --upgrade pip
RUN apt-get --yes install libsndfile1

WORKDIR /build
COPY ./requirements.txt /build/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /build/requirements.txt

COPY ./src /build

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
