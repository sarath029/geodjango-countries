from enum import unique

from django.contrib.gis.db import models


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    geom = models.MultiPolygonField(srid=4326)
