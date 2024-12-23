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


class MainCategory(BaseModel):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("main category")
        verbose_name_plural = _("main categories")
    

class SubCategory(BaseModel):
    name = models.CharField(max_length=250)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name="sub_categories")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("sub category")
        verbose_name_plural = _("sub categories")
    

class ProductCategory(BaseModel):
    name = models.CharField(max_length=250)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="product_categories")

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
    image = models.ImageField(upload_to='product/images/')
    name = models.CharField(max_length=250)
    price = models.PositiveBigIntegerField(default=0)
    discount_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_discount = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='products')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    colors = models.ManyToManyField(Colors, blank=True, related_name='products')
    infos = models.ManyToManyField(ProductInfo, blank=True, related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def clean(self):
        if self.sub_category.main_category != self.main_category:
            raise ValueError("")
        if self.category.sub_category != self.sub_category:
            raise ValueError("")

        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ProductMedia(BaseModel):
    media = models.ImageField(upload_to='product-media/medias/')
    product = models.ForeignKey(Product, related_name='medias', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("product media")
        verbose_name_plural = _("product medias")


class DiscountedProduct(BaseModel):
    image_uz = models.ImageField(upload_to='discounted-product/image_uz')
    image_ru = models.ImageField(upload_to='discounted-product/image_ru')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounted_products')

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = _("discounted product")
        verbose_name_plural = _("discounted products")
