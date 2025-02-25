from django.contrib import admin
from django.utils.safestring import mark_safe

from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from product import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ["name","item", 'image']
    list_filter = ['main_category']


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
    list_display = ["id", "name", 'main_category']
    list_filter = ['main_category']

    
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

@admin.register(models.FifthCategroy)
class FifthCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    pass