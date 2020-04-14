FROM python:3.7-alpine

MAINTAINER nguyenkhacthanh244@gmail.com

WORKDIR /app

RUN apk update && apk add --no-cache gcc musl-dev libffi-dev openssl-dev

COPY requirements.txt requirements-test.txt ./

RUN pip install --no-cache-dir -r requirements-test.txt

COPY . ./

ENTRYPOINT pytest && PYTHONPATH=$(pwd) pylint-fail-under --fail_under 9.5 app

CMD /bin/sh
