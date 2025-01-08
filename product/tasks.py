from celery import shared_task
from product import models
from product import utils


@shared_task
def sync_product_data():
    products = utils.get_product_data()
    poducts = utils.fill_data_to_database(products)
    # for product in poducts:
    #     print(f'f{product} is createed')
    # utils.create_or_update_sub_category(products)
    # utils.create_or_update_sub_sub_category(products)
    # utils.create_or_update_sub_sub_sub_category(products)
    # utils.create_or_update_products(products)
    print('Product Category is added')