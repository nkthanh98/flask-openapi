FROM python:3.7-alpine

WORKDIR /app

RUN apk update && apk add --no-cache gcc musl-dev libffi-dev openssl-dev

ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD . .

EXPOSE 80

ENTRYPOINT gunicorn wsgi:application --bind "0.0.0.0:80" --worker-class gevent

CMD /bin/sh
