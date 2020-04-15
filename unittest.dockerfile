FROM python:3.7-alpine

MAINTAINER nguyenkhacthanh244@gmail.com

WORKDIR /app

RUN apk update && apk add --no-cache gcc musl-dev libffi-dev openssl-dev curl bash

COPY requirements.txt requirements-test.txt ./

RUN pip install --no-cache-dir -r requirements-test.txt

COPY . ./

ENTRYPOINT python -m pytest &&\
           PYTHONPATH=$(pwd) python linter.py --fail-under 9.5 app &&\
           bash -c "bash <(curl -s https://codecov.io/bash)"

CMD /bin/sh
