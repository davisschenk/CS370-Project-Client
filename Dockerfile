FROM python:3.10.0-slim-buster

WORKDIR /client

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY influx_client.py influx_client.py

CMD python3 influx_client.py
