# antismokify-gpu

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Project Requirements
* Ubuntu 16.04/18.04, Debian Jessie/Stretch
* Nvidia GPU

## Project Setup
* Install Docker on Ubuntu (v19.03): [Guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
* Install Docker Compose on Ubuntu: [Guide](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04)
* Install nvidia-docker (v2.0.3): [Guide](https://github.com/NVIDIA/nvidia-docker/blob/master/README.md)
* Now that the tough part is over, remaining setup is easy peasy.
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

 
 
