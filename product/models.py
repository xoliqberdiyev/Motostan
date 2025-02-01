from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel


class ProductBrand(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product brand')
        verbose_name_plural = _('product brands')


class MainCategory(BaseModel):
    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    
    # def __str__(self):
    #     return self.name
    
    class Meta:
        verbose_name = _("main category")
        verbose_name_plural = _("main categories")
    

class SubCategory(BaseModel):
    name = models.CharField(max_length=250, unique=True)
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True, related_name="sub_categories")
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    class Meta:
        verbose_name = _("sub category")
        verbose_name_plural = _("sub categories")


class ProductCategory(BaseModel):
    name = models.CharField(max_length=250, unique=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name="product_categories")
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    # def __str__(self):
    #     return self.name

    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')


class Category(BaseModel):
    name = models.CharField(max_length=250, unique=True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name="categories")
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    # def __str__(self):
    #     return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Colors(BaseModel):
    rgba_name = models.CharField(max_length=250, blank=True, null=True)
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
    description = models.TextField(blank=True, null=True)
    quantity_left = models.CharField(blank=True, null=True, max_length=250)
    price = models.PositiveBigIntegerField(default=0)
    price_type = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, unique=True)
    item = models.CharField(max_length=250, null=True, blank=True)

    image = models.ImageField(upload_to='product/images/', null=True, blank=True)
    discount_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True
    )

    is_discount = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    brand = models.ForeignKey(ProductBrand, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)

    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    category_sub_category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='product_sub_categories', null=True, blank=True)

    colors = models.ManyToManyField(Colors, blank=True, related_name='products')
    infos = models.ManyToManyField(ProductInfo, blank=True, related_name='products')

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def clean(self):
        if self.sub_category and self.main_category and self.category and self.category_sub_category:
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
    image_ru = models.ImageField(upload_to='discounted-product/image_ru')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounted_products')

    def __str__(self):
        return f'{self.product} - {self.image_ru}'

    class Meta:
        verbose_name = _("discounted product")
        verbose_name_plural = _("discounted products")
