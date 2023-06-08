# Celery worker
FROM python:3.11
# setup environment variable
ENV DockerHOME=/home/app/worker

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME
RUN useradd -ms /bin/bash celery
COPY requirements.txt .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT false

# install dependencies
RUN pip install --upgrade pip

# run this command to install all dependencies
RUN pip install -r requirements.txt
# copy whole project to your docker home directory.
COPY * $DockerHOME
RUN chown -R celery:celery $DockerHOME
USER celery
#COPY app.py $DockerHOME
#COPY ../config.py $DockerHOME


# port where the gRPC server app runs
#EXPOSE 50051
# start server
#CMD python app.py
