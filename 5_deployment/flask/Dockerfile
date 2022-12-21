FROM python:3.8

EXPOSE 3000
#ENV PORT=8080

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1



ARG default_PORT=3000
ENV PORT=$default_PORT


ARG default_SERVER='stg'
ENV _SERVER=$default_SERVER

ARG default_MY_VAR='tharhtetsan'
ENV _MY_VAR=$default_MY_VAR

WORKDIR /app
COPY . /app

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

CMD python3 main.py
#CMD exec gunicorn --bind :$PORT  --workers 1 --threads 8 --timeout 0 main:app
