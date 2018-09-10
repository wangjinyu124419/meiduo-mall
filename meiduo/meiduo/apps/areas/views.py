from django.shortcuts import render
from rest_framework.viewsets import  ReadOnlyModelViewSet
from . import serializer
# Create your views here.
from .models import Area
from rest_framework_extensions.cache.mixins import CacheResponseMixin
class AreasView(CacheResponseMixin,ReadOnlyModelViewSet):

    pagination_class = None
    # queryset = Area.objects.all()
    def get_queryset(self):
        if self.action=='list':
            return Area.objects.filter(parent=None)
        else:

            return Area.objects.all()

    # serializer_class = AreaSerializer
    def get_serializer_class(self):
        if self.action=='list':
            return serializer.AreaSerializer
        else:
            return serializer.SubAreaSerializer

