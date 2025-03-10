import os 
from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models import Count
from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponse


from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from product import models

class ProductMedia(admin.TabularInline):
    model = models.ProductMedia
    extra = 1

class ProductInfo(admin.TabularInline):
    model = models.ProductInfo
    extra = 0

@admin.register(models.Product)
class ProductModelAdmin(admin.ModelAdmin):
    change_list_template = "admin/custom_changelist.html"
    search_fields = ['name', 'item']
    list_display = ["name","item", 'image']
    list_filter = ['main_category']
    list_editable = ['image']
    inlines = [ProductMedia, ProductInfo]


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('admin/product/product/', self.update_data, name='update_data'),
        ]
        return custom_urls + urls

    def update_data(self, request):
        file_path = "/var/www/backend/moto"  
        os.system(f"cd {file_path}") 
        os.system(f'source venv/bin/activate')
        os.system(f'python utils.py')
        pwd = os.system("pwd")
        ls = os.system('ls')
        print(ls)
        print(pwd)
        messages.success(request, "Ma'lumotlar muvaffaqiyatli yangilandi!")
        return redirect("admin:product_product_changelist")  



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