from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from common import models


@admin.register(models.AboutUs)
class AboutUsAdmin(TranslationAdmin):
    list_display = ['id', 'title',]


@admin.register(models.Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_uz', 'image_ru']


@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_uz', 'image_ru']
