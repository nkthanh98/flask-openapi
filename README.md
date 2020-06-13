[![GithubCI](https://github.com/magiskboy/flask-webservice/workflows/Test/badge.svg)](https://github.com/magiskboy/flask-webservice/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/magiskboy/flask-webservice/branch/master/graph/badge.svg)](https://codecov.io/gh/magiskboy/flask-webservice)


# flask-webservice
Seed of Flask project with OpenAPIv3 documentation


### Dependencies

Project base on [Flask](https://flask.palletsprojects.com) framework - asynchronous web framework

Using [SQLAlchemy](https://www.sqlalchemy.org/) as ORMs framework


### Install and Start
```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ FLASK_ENV=development FLASK_APP=wsgi:application flask run --host 127.0.0.1 --port 5000
```
