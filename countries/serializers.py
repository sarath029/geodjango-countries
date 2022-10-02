import json

from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Country


class CountrySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Country
        geo_field = "geom"
        fields = "__all__"

    def to_internal_value(self, data):
        if data.get("geom"):
            geom_str = json.dumps(data["geom"])
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

            except TypeError as e:
                print(e)
            data["geom"] = json.loads(geom.geojson)
        return super().to_internal_value(data)
