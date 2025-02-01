import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()


from product import models
import utils


def sync_product_data():
    products = utils.get_product_data()
    utils.fill_data_to_database(products)
    print('Product Category is added')


sync_product_data()