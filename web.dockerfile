FROM python:3.7-alpine

MAINTAINER nguyenkhacthanh244@gmail.com

WORKDIR /app

RUN apk update && apk add --no-cache gcc musl-dev libffi-dev openssl-dev

ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD app ./app

ADD wsgi.py logging.ini ./

EXPOSE 80

ENTRYPOINT gunicorn wsgi:application --bind "0.0.0.0:80" --worker-class gevent

CMD /bin/sh
