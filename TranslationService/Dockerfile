# Dockerfile, Image, Container
FROM python:3.10

ADD *.py .

#RUN sudo apt install libsndfile1
#RUN apt-get --no-install-recommends install -y libsndfile
RUN apt-get --yes install libsndfile1
#RUN apt-get --force-yes install libsndfile1
#CMD ["python", "./main.py"]

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./src /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
