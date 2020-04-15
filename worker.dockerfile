FROM python:3.7-alpine

MAINTAINER nguyenkhacthanh244@gmail.com

WORKDIR /app

RUN apk update && apk add --no-cache gcc musl-dev libffi-dev openssl-dev

ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD app ./app

ADD logging.ini ./

ENTRYPOINT celery -A app.jobs.manager worker -l info

CMD /bin/sh
