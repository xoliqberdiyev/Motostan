from celery import shared_task

from product.models import Product
from product.utils import get_product_data


@shared_task
def sync_product_data():
    data = get_product_data()
    # for product in data:
    #     print(product)
    for i in range(1,3):
        print(data[:i])
        i+=1


