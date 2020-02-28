FROM python:3.6.0-alpine

MAINTAINER Paul Gass<paulm.gass@gmail.com>

LABEL name="Flask GraphQL"

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk --update add py-pip     && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /usr/src/app/

EXPOSE 15000

CMD flask run --host=0.0.0.0 --port=15000
