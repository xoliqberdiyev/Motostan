from django.contrib import admin
from django.utils.safestring import mark_safe

from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from product import models

admin.site.register(models.DiscountedProduct)
admin.site.register(models.ProductInfo)
admin.site.register(models.ProductBrand)
admin.site.register(models.Colors)


class InfoNameInline(admin.StackedInline):
    model = models.InfoName
    extra = 0


class MediaInline(admin.StackedInline):
    model = models.ProductMedia
    extra = 0


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [MediaInline]
    search_fields = ['name']
    list_display = ["id", "name"]


@admin.register(models.TechnicalInfoName)
class TechInfoAdmin(admin.ModelAdmin):
    inlines = [InfoNameInline]


class CategoryInline(admin.StackedInline):
    model = models.ProductCategory
    extra = 0

    
class SubCategory(admin.StackedInline):
    model = models.SubCategory
    extra = 0
    fields = ['link', 'name']
    readonly_fields = ['link']
    
    def link(self, instance):
        url = f"/admin/product/subcategory/{instance.id}/change/"
        return mark_safe(f'<a target="_blank" href="{url}">Kirish</a>')

    

@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
    list_display = ["id", "name"]

    
@admin.register(models.MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    inlines =  [SubCategory]

@admin.register(models.ProductCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(models.Category)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
