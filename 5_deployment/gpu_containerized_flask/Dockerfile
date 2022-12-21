FROM nvidia/cuda:11.0.3-runtime-ubuntu20.04

EXPOSE 8080
ENV PORT=8080



RUN apt update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .

# Install pip requirements
RUN apt update
RUN pip3 install -r requirements.txt



CMD exec gunicorn --bind :$PORT  --workers 1 --threads 8 --timeout 0 main:app

