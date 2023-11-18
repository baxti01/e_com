FROM python:3.11
LABEL authors="baxti"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt app/

WORKDIR app/

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . .
