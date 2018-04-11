FROM python:3.6

RUN apt-get update && \
    apt-get install -y && \
    pip install --upgrade pip && \
    pip3 install uwsgi

ENV DJANGO_ENV=dev
# ENV DJANGO_ENV=prod
ENV DOCKER_CONTAINER=1

EXPOSE 8000
EXPOSE 8001

# Will also be done in docker-compose
COPY ./mundial2018 /opt/mundial2018
RUN pip3 install -r /opt/mundial2018/requirements.txt

# Temporarily disabled
# CMD ["uwsgi", "--ini", "/opt/mundial2018/uwsgi.ini"]
