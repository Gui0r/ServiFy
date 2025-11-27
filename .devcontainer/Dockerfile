FROM python:3.10-slim

WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    default-mysql-client build-essential && \
    pip install --upgrade pip

COPY requirements.txt /workspace/requirements.txt
RUN pip install -r requirements.txt || true
