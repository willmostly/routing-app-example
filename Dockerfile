FROM python:3.11

WORKDIR /data

COPY getrouting /data/getrouting
COPY requirements.txt /data/

RUN pip install -r /data/requirements.txt
EXPOSE 9000
CMD ["gunicorn", "-w", "1", "--bind", "0.0.0.0:9000", "getrouting:app"]
