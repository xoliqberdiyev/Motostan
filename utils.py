import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

import requests
from django.core.exceptions import ObjectDoesNotExist

from product import models
from django.db import transaction



r = requests.get('https://dicloud.uz:38871/hayat_moto/hs/products1/get_products',auth=('Administrator','Odilsoft!'))
def get_product_data():
    if r.status_code == 200:
        raw_text = r.text.strip().split(';')  # Split by semicolon to separate products
        products = []

        for line in raw_text:
            if line.strip():
                product = {}
                for item in line.split(', '):
                    if ': ' in item:
                        key, value = item.split(': ', 1)
                        product[key.strip()] = value.strip()
                products.append(product)
        # print(product)
        return products


def fill_data_to_database(data):
    created_products = []
    for product in data:
        main_category = product.get("Родитель4")
        sub_category = product.get("Родитель3") if product.get("Родитель3") != ' ' else '..'
        category = product.get("Родитель2")
        categoty_last = product.get("Родитель1")

        product_main_category = None
        product_subcategory = None
        product_category_ = None
        product_sub_sub_category = None

        try:
            product_main_category, _ = models.MainCategory.objects.get_or_create(name=main_category)
        except models.MainCategory.MultipleObjectsReturned:
            duplicates = models.MainCategory.objects.filter(name=main_category)
            product_main_category = duplicates.first()
            duplicates.exclude(id=product_main_category.id).delete()

        try:
            product_subcategory, _ = models.SubCategory.objects.get_or_create(name=sub_category, main_category=product_main_category)
        except models.SubCategory.MultipleObjectsReturned:
            duplicates = models.SubCategory.objects.filter(name=sub_category, main_category=product_main_category)
            product_subcategory = duplicates.first()
            duplicates.exclude(id=product_subcategory.id).delete()

        try:
            product_category_, _ = models.ProductCategory.objects.get_or_create(name=category, sub_category=product_subcategory)
        except models.ProductCategory.MultipleObjectsReturned:
            duplicates = models.ProductCategory.objects.filter(name=category, sub_category=product_subcategory)
            product_category_ = duplicates.first()
            duplicates.exclude(id=product_category_.id).delete()

        try:
            product_sub_sub_category, _ = models.Category.objects.get_or_create(name=categoty_last, product_category=product_category_)
        except models.Category.MultipleObjectsReturned:
            duplicates = models.Category.objects.filter(name=categoty_last, product_category=product_category_)
            product_sub_sub_category = duplicates.first()
            duplicates.exclude(id=product_sub_sub_category.id).delete()


        try:
            price = int(product.get('Цена', 0) or 0)  # Default to 0 if 'Цена' is None or empty
        except ValueError:
            price = 0

        product, created = models.Product.objects.update_or_create(
            name=product.get('Наименование для печати'),
            category=product_category_,
            main_category=product_main_category,
            sub_category=product_subcategory,
            category_sub_category=product_sub_sub_category,
            item=product.get('Артикул'),
            quantity_left=product.get('Количество на складе') if product.get('Количество на складе') else 0,
            description=product.get('Описание') if product.get('Описание') else '',
            price_type=product.get('Вид цены') if product.get('Вид цены') else None,
            defaults={'price': price}
        )
        from django.db.models import Count



        duplicates = (
            models.Product.objects.values('name', 'category', 'main_category', 'sub_category', 'category_sub_category')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        for duplicate in duplicates:
            products = models.Product.objects.filter(
                name=duplicate['name'],
                category=duplicate['category'],
                main_category=duplicate['main_category'],
                sub_category=duplicate['sub_category'],
                category_sub_category=duplicate['category_sub_category']
            )
            products.exclude(id=products.first().id).delete()


        created_products.append(product)

    return created_products


# def create_or_update_category(products):
#     # incoming_data = {
#     #     product['Родитель4']: product for product in products
#     #     if product.get('Родитель4')
#     # }
#     # incoming_names = set(incoming_data.keys())
#     #
#     # existing_categories = models.MainCategory.objects.all()
#     # existing_names = {category.name for category in existing_categories}
#     #
#     # categories_to_create = incoming_names - existing_names
#     # categories_to_update = incoming_names & existing_names
#     #
#     # categories_to_delete = existing_names - incoming_names
#     #
#     # with transaction.atomic():
#     #     if categories_to_create:
#     #         new_categories = [
#     #             models.MainCategory(name=name)
#     #             for name in categories_to_create
#     #         ]
#     #         models.MainCategory.objects.bulk_create(new_categories, batch_size=500)
#     #
#     #     if categories_to_update:
#     #         categories_to_update_instances = []
#     #         for category in existing_categories:
#     #             if category.name in categories_to_update:
#     #                 incoming = incoming_data[category.name]
#     #                 categories_to_update_instances.append(category)
#     #         if categories_to_update_instances:
#     #             models.MainCategory.objects.bulk_update(categories_to_update_instances, ['name'],
#     #                                                     batch_size=500)
#     #
#     #     if categories_to_delete:
#     #         models.MainCategory.objects.filter(name__in=categories_to_delete).delete()
#     #
#     # incoming_data = {
#     #     product['Родитель4']: product for product in products
#     #     if product.get('Родитель4')
#     # }
#     # for data in incoming_data:
#     #     print(data)
#
#     incoming_data = {
#         product['Родитель1']: product for product in products
#         if product.get('Родитель1')
#     }
#     i = 1
#     for data in incoming_data:
#         print(data)
#         i += 1
#     print(i)
#
#
# def create_or_update_sub_category(products):
#     incoming_data = {
#         product['Родитель3']: {
#             'main_category': product['Родитель4'],
#             'sub_category': product['Родитель3'],
#         }
#         for product in products
#         if product.get('Родитель3')
#     }
#
#     incoming_subcategories = set(incoming_data.keys())
#     incoming_main_categories = set(product['Родитель4'] for product in products if product.get('Родитель4'))
#
#     existing_main_categories = {cat.name: cat for cat in
#                                 models.MainCategory.objects.filter(name__in=incoming_main_categories)}
#     existing_subcategories = {sub.name: sub for sub in
#                               models.SubCategory.objects.filter(name__in=incoming_subcategories)}
#
#     subcategories_to_create = []
#     subcategories_to_update = []
#
#     for sub_name, data in incoming_data.items():
#         main_category_name = data['main_category']
#         if main_category_name in existing_main_categories:
#             main_category_instance = existing_main_categories[main_category_name]
#             if sub_name not in existing_subcategories:
#                 subcategories_to_create.append(
#                     models.SubCategory(name=sub_name, main_category=main_category_instance)
#                 )
#             else:
#                 sub_category_instance = existing_subcategories[sub_name]
#                 sub_category_instance.main_category = main_category_instance
#                 subcategories_to_update.append(sub_category_instance)
#
#     subcategories_to_delete = set(existing_subcategories.keys()) - incoming_subcategories
#
#     with transaction.atomic():
#         if subcategories_to_create:
#             models.SubCategory.objects.bulk_create(subcategories_to_create, batch_size=500)
#
#         if subcategories_to_update:
#             models.SubCategory.objects.bulk_update(subcategories_to_update, ['main_category', 'name'], batch_size=500)
#
#         if subcategories_to_delete:
#             models.SubCategory.objects.filter(name__in=subcategories_to_delete).delete()
#
#     print('SubCategory is added')
#
#
# def create_or_update_sub_sub_category(products):
#     incoming_data = {
#         product['Родитель2']: {
#             'main_category': product['Родитель3'],
#             'sub_category': product['Родитель2'],
#         }
#         for product in products
#         if product.get('Родитель2')
#     }
#
#     incoming_subcategories = set(incoming_data.keys())
#     incoming_main_categories = set(product['Родитель3'] for product in products if product.get('Родитель3'))
#
#     existing_main_categories = {cat.name: cat for cat in
#                                 models.SubCategory.objects.filter(name__in=incoming_main_categories)}
#     existing_subcategories = {sub.name: sub for sub in
#                               models.ProductCategory.objects.filter(name__in=incoming_subcategories)}
#
#     subcategories_to_create = []
#     subcategories_to_update = []
#
#     for sub_name, data in incoming_data.items():
#         main_category_name = data['main_category']
#         if main_category_name in existing_main_categories:
#             main_category_instance = existing_main_categories[main_category_name]
#             if sub_name not in existing_subcategories:
#                 subcategories_to_create.append(
#                     models.ProductCategory(name=sub_name, sub_category=main_category_instance)
#                 )
#             else:
#                 sub_category_instance = existing_subcategories[sub_name]
#                 sub_category_instance.main_category = main_category_instance
#                 subcategories_to_update.append(sub_category_instance)
#
#     subcategories_to_delete = set(existing_subcategories.keys()) - incoming_subcategories
#
#     with transaction.atomic():
#         if subcategories_to_create:
#             models.ProductCategory.objects.bulk_create(subcategories_to_create, batch_size=500)
#
#         if subcategories_to_update:
#             models.ProductCategory.objects.bulk_update(subcategories_to_update, ['sub_category', 'name'], batch_size=500)
#
#         if subcategories_to_delete:
#             models.ProductCategory.objects.filter(name__in=subcategories_to_delete).delete()
#
#
#     print('SubSubCategory is added')
#
#
# def create_or_update_sub_sub_sub_category(products):
#     incoming_data = {
#         product['Родитель1']: {
#             'main_category': product['Родитель2'],
#             'sub_category': product['Родитель1'],
#         }
#         for product in products
#         if product.get('Родитель1')
#     }
#
#     incoming_subcategories = set(incoming_data.keys())
#     incoming_main_categories = set(product['Родитель2'] for product in products if product.get('Родитель2'))
#
#     existing_main_categories = {cat.name: cat for cat in
#                                 models.ProductCategory.objects.filter(name__in=incoming_main_categories)}
#     existing_subcategories = {sub.name: sub for sub in
#                               models.Category.objects.filter(name__in=incoming_subcategories)}
#
#     subcategories_to_create = []
#     subcategories_to_update = []
#
#     for sub_name, data in incoming_data.items():
#         main_category_name = data['main_category']
#         if main_category_name in existing_main_categories:
#             main_category_instance = existing_main_categories[main_category_name]
#             if sub_name not in existing_subcategories:
#                 subcategories_to_create.append(
#                     models.Category(name=sub_name, product_category=main_category_instance)
#                 )
#             else:
#                 sub_category_instance = existing_subcategories[sub_name]
#                 sub_category_instance.main_category = main_category_instance
#                 subcategories_to_update.append(sub_category_instance)
#
#     subcategories_to_delete = set(existing_subcategories.keys()) - incoming_subcategories
#
#     with transaction.atomic():
#         if subcategories_to_create:
#             models.Category.objects.bulk_create(subcategories_to_create, batch_size=500)
#
#         if subcategories_to_update:
#             models.Category.objects.bulk_update(subcategories_to_update, ['product_category', 'name'], batch_size=500)
#
#         if subcategories_to_delete:
#             models.Category.objects.filter(name__in=subcategories_to_delete).delete()
#
#
#     print('SubSubSubCategory is added')
#
#
# def create_or_update_products(products):
#     for product in products:
#         if product.get('Наименование для печати') is None:
#             product['Наименование для печати'] = 'Something'
#         main_category = product.get("Родитель4")
#         sub_category = product.get("Родитель3")
#         category = product.get("Родитель2")
#         category_last = product.get("Родитель1")
#
#         product_main_category = None
#         product_subcategory = None
#         product_category = None
#         product_category_last = None
#
#         if main_category:
#             product_main_category, _ = models.MainCategory.objects.get_or_create(name=main_category)
#
#         if sub_category and product_main_category:
#             product_subcategory, _ = models.SubCategory.objects.get_or_create(name=sub_category,
#                                                                               main_category=product_main_category)
#
#         if category and product_subcategory:
#             product_category, _ = models.ProductCategory.objects.get_or_create(name=category,
#                                                                                sub_category=product_subcategory)
#
#         if category_last and product_category:
#             product_category_last, _ = models.Category.objects.get_or_create(name=category_last,
#                                                                              product_category=product_category)
#
#         try:
#             price = int(product.get('Цена', 0) or 0)
#         except ValueError:
#             price = 0
#
#         models.Product.objects.update_or_create(
#             name=product.get('Наименование для печати'),
#             price=price,
#             item=product.get('Артикул'),
#             quantity_left=product.get('Количество на складе') if product.get('Количество на складе') else 0,
#             description=product.get('Описание') if product.get('Описание') else '',
#             category=product_category if product_category else product_category,
#             sub_category=product_subcategory,
#             main_category=product_main_category,
#             category_sub_category=product_category_last,
#         )
#
#
