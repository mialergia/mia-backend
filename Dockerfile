# https://djangoforprofessionals.com/docker/

# Dockerfile

# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY Pipfile Pipfile.lock /code/
# https://github.com/pypa/pipenv/issues/4337
RUN pip install pipenv==2018.11.26
RUN pipenv install --system
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get update && apt-get install -y gdal-bin
RUN pipenv sync --dev
# Comment
RUN echo 'we are running some # of cool things'

            

# Copy project
COPY . /code/