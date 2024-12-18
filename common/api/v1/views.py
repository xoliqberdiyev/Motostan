from rest_framework import views, status
from rest_framework.response import Response

from common.api.v1 import serializers
from common import models


class AboutUsApiView(views.APIView):
    def get(self, request):
        query = models.AboutUs.objects.all()
        serializer = serializers.AboutUsSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdvertisementApiView(views.APIView):
    def get(self, request):
        query = models.Advertisement.objects.all()
        serializer = serializers.AdvertisementSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BannerApiView(views.APIView):
    def get(self, request):
        query = models.Banner.objects.all()
        serializer = serializers.BannerSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
