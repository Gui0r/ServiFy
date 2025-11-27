FROM python:3.10-slim

WORKDIR /workspaces/ServiFy

RUN apt-get update && apt-get install -y \
    default-mysql-client build-essential && \
    pip install --upgrade pip

COPY ../requirements.txt /workspaces/ServiFy/requirements.txt
RUN pip install -r /workspaces/ServiFy/requirements.txt

