###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.6-slim as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update -qq \
    && apt-get install --no-install-recommends --yes \
    build-essential ffmpeg libsm6 libxext6

# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . .
RUN flake8 --exclude=.git,.venv,env,.tox,dist,doc,*egg,build,.vscode,*migrations/*.py,*/local_settings.py .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.9.6-slim

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update -qq \
    && apt-get install --no-install-recommends --yes \
    build-essential  ffmpeg libsm6 libxext6 libssl-dev ca-certificates libasound2

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app