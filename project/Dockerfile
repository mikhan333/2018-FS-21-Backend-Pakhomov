FROM ubuntu:16.04
ADD . /app
RUN apt-get update
RUN apt-get install -y python python-pip
RUN pip install -r /app/requirements.txt
EXPOSE 8000
WORKDIR /app
USER nobody
CMD ./manage.py runserver
