FROM python:3.9.9

ENV PYTHONUNBUFFERED 1
RUN apt update
EXPOSE 8000

WORKDIR /my_app
ADD . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
