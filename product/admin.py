from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from product import models

admin.site.register(models.DiscountedProduct)
admin.site.register(models.ProductInfo)
admin.site.register(models.ProductCategory, TranslationAdmin)
admin.site.register(models.ProductBrand, TranslationAdmin)
admin.site.register(models.Colors)


class InfoNameInline(admin.StackedInline):
    model = models.InfoName
    extra = 0


class MediaInline(admin.StackedInline):
    model = models.ProductMedia
    extra = 0


@admin.register(models.Product)
class ProductAdmin(TranslationAdmin):
    inlines = [MediaInline]


@admin.register(models.TechnicalInfoName)
class TechInfoAdmin(admin.ModelAdmin):
    inlines = [InfoNameInline]