from django.urls import include, path
from rest_framework.routers import DefaultRouter

from countries.views import CountryViewSet

router = DefaultRouter()
router.register("countries", CountryViewSet, basename="countries")

urlpatterns = [
    path(r"", include(router.urls)),
]
