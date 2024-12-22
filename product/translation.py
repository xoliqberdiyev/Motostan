from modeltranslation.translator import TranslationOptions, register

from product import models


@register(models.ProductBrand)
class ProductBrandTranslation(TranslationOptions):
    fields = ['name']


@register(models.MainCategory)
class MainCategoryTranslation(TranslationOptions):
    fields = ['name']
    

@register(models.SubCategory)
class SubCategoryTranslation(TranslationOptions):
    fields = ['name']


@register(models.ProductCategory)
class ProductCategoryTranslation(TranslationOptions):
    fields = ['name']


@register(models.Product)
class ProductCategoryTranslation(TranslationOptions):
    fields = ['name']