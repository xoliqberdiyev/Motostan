from rest_framework import serializers

from common import models


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AboutUs
        fields = [
            'id', 'title_uz', 'title_ru', 'media', 'description_uz', 'description_ru'
        ]


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Advertisement
        fields = [
            'id', 'image_uz', 'image_ru'
        ]


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = [
            'id', 'image_uz', 'image_ru'
        ]