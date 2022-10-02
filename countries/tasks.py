import json

import requests
from celery import shared_task
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon

from countries.models import Country


def get_countries_json():
    def _get_resource_url():

        response = requests.get(settings.COUNTRIES_DATA_PACKAGE_URL)
        response.raise_for_status()

        for resource in response.json()["resources"]:
            if resource.get("datahub").get("type") == "original":
                return resource.get("path")

    resource_url = _get_resource_url()
    response = requests.get(resource_url)
    response.raise_for_status()

    return response.json()


@shared_task(retry_kwargs={"max_retries": 2, "countdown": 5})
def refresh_countries():

    try:
        countries_json = get_countries_json()
    except Exception as e:
        print(e)

    for feature in countries_json["features"]:
        geom_str = json.dumps(feature["geometry"])
        geom = GEOSGeometry(geom_str, srid=4326)

        try:
            if isinstance(geom, MultiPolygon):
                pass
            elif isinstance(geom, Polygon):
                geom = MultiPolygon([geom])
            else:
                raise TypeError(
                    "{} not acceptable for this model".format(geom.geom_type)
                )

            Country.objects.update_or_create(
                name=feature["properties"]["ADMIN"], geom=geom
            )

        except TypeError as e:
            print(e)
