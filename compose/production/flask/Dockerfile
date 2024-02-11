ARG PYTHON_VERSION=3.10-slim-bullseye

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=production

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  libglib2.0-0 \
  libsm6 \
  libxext6 \
  ffmpeg \
  ghostscript

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .

ARG APP_HOME=/app

RUN pip install -r ${BUILD_ENVIRONMENT}.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

ENV TZ="Asia/Kathmandu"
RUN date

WORKDIR ${APP_HOME}

COPY ./compose/production/flask/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/production/flask/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/production/flask/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

# copy application code to WORKDIR
COPY . ${APP_HOME}

# make flask owner of the WORKDIR directory as well.
# RUN chown flask:flask ${APP_HOME}

# USER flask

# ENTRYPOINT ["/entrypoint"]
