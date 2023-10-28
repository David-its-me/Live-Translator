# Live-Translator
A Translation application, that can simultanously translate speech input into another language. Developed for sunday services.

The Project conist of several services:

## MicophoneToStream
Converts Microphone input to a Stream of smaller .wav segments.

## TranslationService
The translation is done in a separate service, to be able to adapt to higher loads, with multiple container instances.

The Service is accessible over a REST API, over which the translation of .wav files is initiated.

### Installation
Bevore building, we recommend to download the language model manually. Otherwise the Docker container would download, when a container runs the first time from an already builded container image. This might be anoying during development.After Download the model must be placed in the _assets/_ folder. Make sure that the file is named exactly _multitask_unity_large.pt_ or _multitask_unity_medium.pt_ For more information please refer to the repository https://github.com/facebookresearch/seamless_communication

| Model Name         | #params | checkpoint                                                                              | metrics                                                                              |
| ------------------ | ------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| SeamlessM4T-Large  | 2.3B    | [🤗 Model card](https://huggingface.co/facebook/seamless-m4t-large) - [download](https://huggingface.co/facebook/seamless-m4t-large/resolve/main/multitask_unity_large.pt)   | [metrics](https://dl.fbaipublicfiles.com/seamlessM4T/metrics/seamlessM4T_large.zip)  |
| SeamlessM4T-Medium | 1.2B    | [🤗 Model card](https://huggingface.co/facebook/seamless-m4t-medium) - [download](https://huggingface.co/facebook/seamless-m4t-medium/resolve/main/multitask_unity_medium.pt) | [metrics](https://dl.fbaipublicfiles.com/seamlessM4T/metrics/seamlessM4T_medium.zip) |


Now having downloaded the model file we build an run the translation service.The translation service runs in a Docker container. 
Bevor you go ahead, please make sure that docker is installed on your system. For more information please refer to the official webpage: https://docs.docker.com/.

Run the following command, to build the application. You can give your docker image a `<image-tag>`, which is used to distinguish docker images.
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




