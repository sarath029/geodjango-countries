import django_filters
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from countries.models import Country
from countries.serializers import CountrySerializer


class CountryFilter(django_filters.FilterSet):
    class Meta:
        model = Country
        fields = {
            "name": ["exact", "contains", "startswith"],
        }


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class CountryViewSet(viewsets.ModelViewSet):

    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("name",)
    filterset_class = CountryFilter

    def get_serializer_class(self):
        return CountrySerializer

    def get_queryset(self):

        if self.action == "neighbouring_countries":
            pk = self.kwargs.get("pk")
            country = Country.objects.get(pk=pk)
            neighbouring_countries = Country.objects.filter(
                geom__touches=country.geom
            ).order_by("pk")
            return neighbouring_countries
        else:
            return Country.objects.all().order_by("pk")

    @action(detail=True, methods=["get"])
    def neighbouring_countries(self, request, pk=None, *args, **kwargs):

        countries = self.get_queryset()
        serializer = self.get_serializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
