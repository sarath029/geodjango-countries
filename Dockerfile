FROM python:3.8

LABEL vendor="Pixxel Countries"

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1


ENV PYTHONUNBUFFERED 1
WORKDIR /code

RUN apt-get update && apt-get install -y gcc
RUN apt-get update ; apt-get --assume-yes install binutils libproj-dev gdal-bin
RUN pip install pipenv && pip install psycopg2

COPY Pipfile Pipfile.lock ./  

RUN pipenv install

COPY /entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY /start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY /celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY /celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat


COPY . ./
EXPOSE 8000

ENTRYPOINT ["/entrypoint"]