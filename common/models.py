from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Banner(BaseModel):
    image_uz = models.ImageField(upload_to='banner/image_uz/')
    image_ru = models.ImageField(upload_to='banner/image_ru/')

    class Meta:
        verbose_name = _("banner")
        verbose_name_plural = _("banners")


class AboutUs(BaseModel):
    title = models.CharField(max_length=250)
    media = models.ImageField(upload_to='about-us/media/')
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("about us")
        verbose_name_plural = _("about us")


class Advertisement(BaseModel):
    image_uz = models.ImageField(upload_to='advertisement/image_uz/')
    image_ru = models.ImageField(upload_to='advertisement/image_ru/')

    class Meta:
        verbose_name = _('advertisement')
        verbose_name_plural = _('advertisements')


class PhoneNumber(BaseModel):
    number = models.CharField(max_length=15) 

    def __str__(self):
        return self.number
    