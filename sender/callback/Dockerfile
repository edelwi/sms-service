FROM python:3.11
# setup environment variable
ENV DockerHOME=/home/app/delivery_api

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

# run this command to install all dependencies
RUN pip install -r requirements.txt


COPY ./sender $DockerHOME/sender

CMD ["uvicorn", "sender.callback.cbapp:app", "--host", "0.0.0.0", "--port", "80"]