FROM python:latest

WORKDIR /app

COPY . /app

ENV BROKER_URL \
    QUEUE

RUN pip install pika

CMD ["python", "./clien.py", "-func", "consume", "-q", $QUEUE]