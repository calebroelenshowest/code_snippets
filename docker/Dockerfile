FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /home/user/python_scripts/

COPY requirements.txt ./
COPY influxdb-selfsigned.crt ./
COPY bridge_cert.pem ./


RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./

CMD [ "python", "main.py"]
