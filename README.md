# antismokify-gpu

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Project Requirements
* Ubuntu 16.04/18.04, Debian Jessie/Stretch
* Nvidia GPU

## Project Setup
* Install Docker on Ubuntu: [Guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
* Install nvidia-docker: [Guide](https://github.com/NVIDIA/nvidia-docker/blob/master/README.md)
* Download antismokify docker image: [Link](http://www.mediafire.com/file/dgzcjcmns3xshb4/antismokify.zip/file) <br>
_The image is compressed to zip. Extract it to get tar file_
* After extracting the zip file, load the tar image using:
  ```bash
  $ docker load < antismokify.tar.gz
  ```



