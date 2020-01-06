FROM python:3.7.6-slim-buster

COPY . /src
WORKDIR /src

ENV APP_CONFIG=config.ProductionConfig
ENV WHITELIST_ENABLED=True

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 --certfile ./prod-pems/fullchain1.pem --keyfile ./prod-pems/privkey1.pem  wsgi --access-logfile - --error-logfile -