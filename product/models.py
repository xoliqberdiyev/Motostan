from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel


class ProductBrand(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self) -> models.CharField:
        return self.name

    class Meta:
        verbose_name = _('product brand')
        verbose_name_plural = _('product brands')


class ProductCategory(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self) -> models.CharField:
        return self.name

    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')


class Colors(BaseModel):
    rgba_name = models.CharField(max_length=250)
    name = models.CharField(max_length=250)

    def __str__(self) -> models.CharField:
        return self.name

    class Meta:
        verbose_name = _("color")
        verbose_name_plural = _("colors")


class TechnicalInfoName(BaseModel):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='tech_names')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("technical information name")
        verbose_name_plural = _("technical information names")


class InfoName(BaseModel):
    tech_info = models.ForeignKey(TechnicalInfoName, on_delete=models.CASCADE, related_name='info_names')
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("info name")
        verbose_name_plural = _("info names")


class ProductInfo(BaseModel):
    tech_info = models.ForeignKey(TechnicalInfoName, on_delete=models.CASCADE, related_name='product_infos')
    info_name = models.ForeignKey(InfoName, on_delete=models.CASCADE, related_name='product_infos')

    def __str__(self):
        return f"{self.tech_info} - {self.info_name}"

    class Meta:
        verbose_name = _("product info")
        verbose_name_plural = _("product infos")


class Product(BaseModel):
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=250)
    price = models.PositiveBigIntegerField(default=0)
    colors = models.ManyToManyField(Colors, null=True, blank=True, related_name='products')
    is_discount = models.BooleanField(default=False)
    discount_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    infos = models.ManyToManyField(ProductInfo, null=True, blank=True, related_name='products')
    image = models.ImageField(upload_to='product/images/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class DiscountedProduct(BaseModel):
    image_uz = models.ImageField(upload_to='discounted-product/image_uz')
    image_ru = models.ImageField(upload_to='discounted-product/image_ru')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounted_products')

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = _("discounted product")
        verbose_name_plural = _("discounted products")
