# pull official base image
FROM python:3.10.5-buster

# set work directory
WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -U gunicorn
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
EXPOSE 8000