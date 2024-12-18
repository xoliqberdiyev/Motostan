from django.contrib import admin

from product import models

admin.site.register(models.Product)
admin.site.register(models.DiscountedProduct)
admin.site.register(models.ProductInfo)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductBrand)
admin.site.register(models.TechnicalInfoName)
admin.site.register(models.InfoName)
admin.site.register(models.Colors)
