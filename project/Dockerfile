FROM python:2.7

ADD . /app
RUN apt-get update
RUN apt-get install -y python python-pip
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r /app/requirements.txt

EXPOSE 8000
WORKDIR /app

USER nobody

