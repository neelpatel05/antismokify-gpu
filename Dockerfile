  
# This is a Dockerfile used to build the enviornment for antismokify
# In order to run Docker in the GPU you will need to install Nvidia-Docker: https://github.com/NVIDIA/nvidia-docker

FROM nvidia/cuda:9.0-cudnn7-devel

# Install face recognition dependencies

RUN apt update -y; apt install -y \
git \
cmake \
libsm6 \
libxext6 \
libxrender-dev \
libopenblas-dev \
liblapack-dev \
python3 \
python3-pip 

RUN pip3 install scikit-build

# Install compilers

RUN apt install -y software-properties-common && \
add-apt-repository ppa:ubuntu-toolchain-r/test && \
apt update -y; apt install -y gcc-6 g++-6 && \
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 50 && \
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-6 50 

# Install dlib 

RUN git clone -b 'v19.16' --single-branch https://github.com/davisking/dlib.git && \
mkdir -p /dlib/build && \
cmake -H/dlib -B/dlib/build -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1 && \
cmake --build /dlib/build && \
cd /dlib; python3 /dlib/setup.py install && \
pip3 install face_recognition

# Install requirements.txt

RUN pip3 install \
Flask==1.0.2 \
opencv-python==4.0.0.21 \
pymongo==3.7.2 \
keras==2.1.2 \
tensorflow-gpu==1.10.0 \
numpy==1.14.1 \ 
face_recognition==1.2.3 \
h5py 

RUN apt-get  ffmpeg & \
apt-get autoremove -y && \
apt-get clean
