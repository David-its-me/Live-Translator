# Live-Translator
A Translation application, that can simultanously translate speech input into another language. Developed for sunday services.

The Project conist of several services:

## MicophoneToStream
Converts Microphone input to a Stream of smaller .wav segments.

## TranslationService
The translation is done in a separate service, to be able to adapt to higher loads, with multiple container instances.

The Service is accessible over a REST API, over which the translation of .wav files is initiated.

### Installation
The translation service runs in a Docker Container. 

Bevor you go ahead, please make sure that docker is installed on your system. For more information please refer to the official webpage: https://docs.docker.com/.

Run the following command, to build the application. You can give your docker image a `<image-tag>`, which is used to distinguish images.
```
docker build -t <image-tag> .
```
Do not wonder if the build takes some time. There are some large libaries. Therefore also the disk size of the container will exced more than 6 GB.

After building the container image, run the container. With the -p option, it is possible to open a port on the container. Both the port used in the operating system (to access the container from outside), as well as the port used inside the container, is indicated here.
```
docker run -p 80:80 <image-tag>
```
On startup of the service, the language model 'seaminglessM4T large' is downloaded. The model is really large, so this also takes some time. 
After that finished, you can test the service, with a simple Web-GUI, that comes along with the service. If the container runs locally you can use: http://localhost:80.

The documentation of the REST-API can be accessed here: http://localhost:80/redoc.




