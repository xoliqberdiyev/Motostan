from django.contrib import admin
from django.utils.safestring import mark_safe

from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from product import models

admin.site.register(models.DiscountedProduct)
admin.site.register(models.ProductInfo)
admin.site.register(models.ProductBrand, TranslationAdmin)
admin.site.register(models.Colors)
admin.site.register(models.Category)


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


class CategoryInline(TranslationStackedInline):
    model = models.ProductCategory
    extra = 0

    
class SubCategory(TranslationStackedInline):
    model = models.SubCategory
    extra = 0
    fields = ['link', 'name']
    readonly_fields = ['link']
    
    def link(self, instance):
        url = f"/admin/product/subcategory/{instance.id}/change/"
        return mark_safe(f'<a target="_blank" href="{url}">Kirish</a>')

    

@admin.register(models.SubCategory)
class SubCategoryAdmin(TranslationAdmin):
    inlines = [CategoryInline]

    
@admin.register(models.MainCategory)
class MainCategoryAdmin(TranslationAdmin):
    inlines =  [SubCategory]