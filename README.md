# Pixxel Countries

## World countries Database Project

Countries geojson is downloaded from [here](https://datahub.io/core/geo-countries#resource-geo-countries_zip) periodically and updated into PostGIS database. 
APIs are enabled to query for the data by name (exact, starts_with, contains), geospatial query can be made to get all neighbouring countries (borders touching) for a given country. 

CRUD APIs are provided to create, read, update, and delete countries.


## Tools and Framework Used 
* [GeoDjango](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/) - A world-class geographic web framework. Its goal is to make it as easy as possible to build GIS web applications and harness the power of spatially enabled data.
* [Celery](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html) - A simple, flexible, and reliable distributed system to process vast amounts of messages, while providing operations with the tools required to maintain such a system.
* [Redis](https://redis.io/) - Redis is the datastore and message broker between Celery and Django.


## Docker setup -

[Docker install instructions](https://docs.docker.com/engine/install/)

Start the project by running - 

```
docker compose up
```

This will create the following services 
* redis - Message broker for our infrastructure setup, background tasks are pushed to redis by either django bakend or celery-beat to be later consumed by celery-worker
* postgis-db - PostGIS DB to store geospatial data
* backend - GeoDjango server, this server is connected to Redis broker and PostGIS database, Two instances will be created on startup to maintain zero down time and manage traffic effectively.
(K8 can be used to manage the configurations more effectively).
* celery-worker - A worker service which continuously listens to redis for new tasks and executes them in the background silently.
* celery-beat - For periodic tasks, it checks the DB for periodic task configurations and uses a scheduler to push tasks to redis which is consumed by the worker.
* nginx - Loadbalancer/reverse proxy to distribute the load between two instances of GeoDjango backend.

Note - Migrate command will be run by default whenever the project is setup (Included in the startup command)
```
python3 manage.py migrate
```

To run any other command inside a container, Ex -
```
docker ps
docker exec -it container_name sh
pipenv shell
python3 manage.py createsuperuser
```

API signature is shared in a Postman collection - **Pixxel Countries.postman_collection.json** & the environment shared in **Pixxel Environment.postman_environment.json**
