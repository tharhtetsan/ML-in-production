# For more information, please refer to 
#!/bin/bash
#https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch
#https://hub.docker.com/r/nvidia/cuda


#FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-devel
#FROM nvidia/cuda:11.0.3-runtime-ubuntu20.04
#FROM nvcr.io/nvidia/pytorch:20.11-py3
#FROM nvidia/cuda:11.3.0-base-ubuntu20.04
FROM nvcr.io/nvidia/pytorch:20.11-py3

RUN apt update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

#RUN apt install nvidia-cuda-toolkit -y
#RUN apt-get install nvidia-utils-410 -y






#RUN python3 -c 'import torch; print(torch.cuda.is_avaiable())






EXPOSE 5002

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN apt update
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "main:app"]
