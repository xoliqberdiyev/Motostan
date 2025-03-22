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
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'image',)
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('admin/product/product/', self.update_data, name='update_data'),
        ]
        return custom_urls + urls

    def update_data(self, request):
        file_path = "/var/www/backend/moto"
        os.system(f"cd {file_path} && . venv/bin/activate && python3 utils.py")    
        messages.success(request, "Ma'lumotlar muvaffaqiyatli yangilandi!")
        return redirect("admin:product_product_changelist")  


@admin.register(models.ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    pass
