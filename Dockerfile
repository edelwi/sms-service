# base image
FROM python:3.11
ENV DockerHOME=/home/app/sms_svc

# set work directory
RUN mkdir -p $DockerHOME
RUN mkdir -p $DockerHOME/sender

# where your code lives
WORKDIR $DockerHOME
COPY requirements.txt .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# run this command to install all dependencies
RUN pip install -r requirements.txt

# copy whole project to your docker home directory.

COPY app.py $DockerHOME
COPY config.py $DockerHOME
COPY sender $DockerHOME/sender


# port where the gRPC server app runs
EXPOSE 50051
# start server
CMD python app.py
