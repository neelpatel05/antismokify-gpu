# antismokify-gpu

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)




Anti-Smokify is a web-app which can detect cigarette smoking scenes from a video. 


In countries like India, the media agencies have to comply to the certain rules which are imposed by the government. One such government regulation that these agencies must abide, is to show a disclaimer; “Smoking is Injurious to Health”, wherever a cigarette smoking scene is present in their media content. In order to show such disclaimer, the agencies need to invest a lot of time and labour to manually inspect and search for such scenes in the video. Given the recent advances in deep learning and availability of huge computing power, our aim is to develop an automated system which can process such large videos as input and show the relevant smoking scenes along with its timestamps so that the media agencies can directly use it to add the disclaimer in least time possible.

The platform takes video as a input and converts it into number of frames. Each frame is analysed for detection of the person in the frame. If the person in present in the frame, it is further classified by using trained CNN model as smoking and non-smoking frame. The timestamp of the smoking frame is extracted and are stored in the database. After completion of video processing the stored timestamps are emailed to the user.

The application is made using:
<br>
<img src="https://img.shields.io/static/v1.svg?label=&message=%20Flask%20&color=blue">
<img src="https://img.shields.io/static/v1.svg?label=&message=%20PyMongo%20&color=blue">
<img src="https://img.shields.io/static/v1.svg?label=&message=%20Keras%20&color=blue">
<img src="https://img.shields.io/static/v1.svg?label=&message=%20TensorFlow%20&color=blue">
<img src="https://img.shields.io/static/v1.svg?label=&message=%20Dlib%20(GPU)%20&color=blue">
<img src="https://img.shields.io/static/v1.svg?label=&message=%20FFmpeg%20&color=blue">
<img src="https://img.shields.io/static/v1.svg?label=&message=%20MongoDB%20&color=blue">
<img src="https://img.shields.io/static/v1.svg?label=&message=%20Docker%20&color=blue">
<br>
This repository provides the Docker image of the web-app with GPU support using nvidia-docker.


## Project Requirements
* Ubuntu 16.04/18.04, Debian Jessie/Stretch
* Nvidia GPU

## Project Setup
* Install Docker on Ubuntu (v19.03): [Guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
* Install Docker Compose on Ubuntu: [Guide](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04)
* Install nvidia-docker (v2.0.3): [Guide](https://github.com/NVIDIA/nvidia-docker/blob/master/README.md)
 <br><br> Now that the tough part is over, remaining setup is easy peasy.<br><br>
* Download antismokify docker image: [Link](http://www.mediafire.com/file/dgzcjcmns3xshb4/antismokify.zip/file) <br>
_The image is compressed to zip. Extract it to get tar file_
* After extracting the zip file, load the tar image using:
  ```bash
  $ docker load < antismokify.tar.gz
  ```
* Run ```docker images``` command to ensure that image has been successfully loaded.
  ```bash
  $ docker images
  REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
  antismokify         gpu                 c83a9b8fcf67        2 weeks ago         5.74GB
  ```
* Download _docker-compose.yml_ using cURL or wget:
  ```bash
  $ curl -O https://raw.githubusercontent.com/jaynilpatel/antismokify-gpu/master/docker-compose.yml
  OR
  $ wget https://raw.githubusercontent.com/jaynilpatel/antismokify-gpu/master/docker-compose.yml
  ```
* Open _docker-compose.yml_ in text editor and add your Gmail $EMAIL_ID and $PASSWORD. (Make sure to allow less secure apps from your Google Account Settings).
* Now the final step. Run ```docker-compose up```
  ```bash
  $ docker-compose up
  ```
* If you do not have Mongodb docker image, it will automatically fetch it. 

 
 
