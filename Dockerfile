# base image
FROM python:3.11
# setup environment variable
ENV DockerHOME=/home/app/sms_svc

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME
COPY requirements.txt .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# copy whole project to your docker home directory.
COPY sender $DockerHOME
COPY app.py $DockerHOME
COPY config.py $DockerHOME

# run this command to install all dependencies
RUN pip install -r requirements.txt
# port where the gRPC server app runs
EXPOSE 50051
# start server
CMD python app.py
