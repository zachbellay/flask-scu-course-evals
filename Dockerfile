FROM python:3.9.6-slim-buster

COPY . /src
WORKDIR /src

VOLUME /src/db

ENV APP_CONFIG=config.ProductionConfig
ENV WHITELIST_ENABLED=False

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 --certfile ./prod-pems/fullchain1.pem --keyfile ./prod-pems/privkey1.pem  wsgi --access-logfile - --error-logfile -