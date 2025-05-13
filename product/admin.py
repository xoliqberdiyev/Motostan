import os 

from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect

from product import models, form


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
    form = form.Productorm
    

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

    def changelist_view(self, request, extra_context=None):
        products = models.Product.objects.all()
        product_count = products.count()
        product_with_image = products.filter(image__isnull=False).exclude(image='').count()
        product_without_image = product_count - product_with_image
        extra_context = extra_context or {}
        extra_context['product_count'] = product_count
        extra_context['product_without_image'] = product_without_image
        extra_context['product_with_image'] = product_with_image

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(models.ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    pass
