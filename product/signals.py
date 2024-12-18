from django.db.models.signals import post_save
from django.dispatch import receiver

from product import models


@receiver(post_save, sender=models.InfoName)
def create_product_info(sender, instance, created, **kwargs):
    if created:
        models.ProductInfo.objects.create(
            tech_info=instance.tech_info,
            info_name=instance,
        )
