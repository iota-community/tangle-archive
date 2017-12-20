FROM python:2.7

MAINTAINER Umair Sarfraz "aquadestructor@icloud.com"

ADD . /permanode
WORKDIR /permanode

RUN pip install --upgrade pip
RUN pip install -r /permanode/requirements.txt
