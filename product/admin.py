from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models import Count

from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from product import models

class ProductMedia(admin.TabularInline):
    model = models.ProductMedia
    extra = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'item']
    list_display = ["name","item", 'image']
    list_filter = ['main_category']
    list_editable = ['image']
    inlines = [ProductMedia]


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
    list_display = ["name",]
    inlines =  [SubCategory]

    # def products_count(self, main_category):
    #     url = (
    #         reverse("admin:product_product_changelist")
    #         + '?'
    #         + urlencode({
    #             "main_category__id": str(main_category.id)
    #         })    
    #     ) 
    #     return format_html('<a href="{}">{} products</a>',url, main_category.products_count)
    
    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         products_count=Count('products')
    #     )

@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name",]
    

    # def products_count(self, category):
    #     url = (
    #         reverse("admin:product_product_changelist")
    #         + '?'
    #         + urlencode({
    #             "category_id": str(category.id)
    #         })    
    #     ) 
    #     return format_html('<a href="{}">{} products</a>',url, category.products_count)
    
    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         products_count=Count('products')
    #     )

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(models.FifthCategroy)
class FifthCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    pass