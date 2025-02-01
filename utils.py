import os
import django
from django.db.models import Q
from django.db import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

import requests
from django.core.exceptions import ObjectDoesNotExist

from product import models
from django.db import transaction
from django.db.models import Count



r = requests.get('https://dicloud.uz:38871/hayat_moto/hs/products1/get_products',auth=('Administrator','Odilsoft!'))
def get_product_data():
    if r.status_code == 200:
        raw_text = r.text.strip().split(';')  
        products = []

        for line in raw_text:
            if line.strip():
                product = {}
                for item in line.split(', '):
                    if ': ' in item:
                        key, value = item.split(': ', 1)
                        product[key.strip()] = value.strip()
                products.append(product)
        return products


def get_or_create_category1(category1, main_category):
    try:
        category, created = models.Category.objects.get_or_create(
            name=category1, 
            product_category=main_category
        )
    except IntegrityError:  # Agar allaqachon mavjud bo'lsa, yana bir bor olib kelamiz
        category = models.Category.objects.get(name=category1)
        created = False
    return category


def get_or_create_category2(category2, main_category):
    try:
        category, created = models.ProductCategory.objects.get_or_create(
            name=category2, 
            sub_category=main_category
        )
    except IntegrityError:  # Agar allaqachon mavjud bo'lsa, yana bir bor olib kelamiz
        category = models.ProductCategory.objects.get(name=category2)
        created = False
    return category


def get_or_create_category3(category3, main_category):
    try:
        category, created = models.SubCategory.objects.get_or_create(
            name=category3, 
            main_category=main_category
        )
    except IntegrityError:  # Agar allaqachon mavjud bo'lsa, yana bir bor olib kelamiz
        category = models.SubCategory.objects.get(name=category3)
        created = False
    return category


def get_or_create_category4(category4):
    try:
        category, created = models.MainCategory.objects.get_or_create(
            name=category4, 
        )
    except IntegrityError:  # Agar allaqachon mavjud bo'lsa, yana bir bor olib kelamiz
        category = models.SubCategory.objects.get(name=category4)
        created = False
    return category


def create_or_update_products(data):
    django_products = models.Product.objects.all()
    django_names = {product.name for product in django_products}
    product_names = {product.get('Наименование для печати') for product in data}

    django_main_categories = models.MainCategory.objects.all()
    django_main_category_names = {category.name for category in django_main_categories}
    main_categories_names = {category.get('Родитель4') for category in data}

    django_sub_categories = models.SubCategory.objects.all()
    django_sub_category_names = {category.name for category in django_sub_categories}
    sub_categories_names = {category.get('Родитель3') for category in data}

    django_product_categories = models.ProductCategory.objects.all()
    django_product_category_names = {category.name for category in django_product_categories}
    product_categories_names = {category.get('Родитель2') for category in data}

    django_categories = models.Category.objects.all()
    django_category_names = {category.name for category in django_categories}
    categories_names = {category.get('Родитель3') for category in data}


    product_to_delete = django_names - product_names
    main_category_to_delete = django_main_category_names - main_categories_names
    sub_category_to_delete = django_sub_category_names - sub_categories_names
    product_category_to_delete = django_product_category_names - product_categories_names
    category_to_delete = django_category_names - categories_names

    if product_to_delete:
        models.Product.objects.filter(name__in=product_to_delete).delete()
        print(f'{product_to_delete} deleted')

    if main_category_to_delete:
        models.MainCategory.objects.filter(name__in=main_category_to_delete).delete()
        models.MainCategory.objects.filter(name__isnull=True).delete()

    if sub_categories_names:
        models.SubCategory.objects.filter(name__in=sub_category_to_delete).delete()
        models.SubCategory.objects.filter(name__isnull=True).delete()

    if product_categories_names:
        models.ProductCategory.objects.filter(name__in=product_category_to_delete).delete()
        models.ProductCategory.objects.filter(name__isnull=True).delete()

    if category_to_delete:
        models.Category.objects.filter(name__in=category_to_delete).delete()
        models.Category.objects.filter(name__isnull=True).delete()
    for product in data:
        name = product.get('Наименование для печати')
        if name == None or name == '':
            continue 
        article = product.get('Артикул')
        description = product.get('Описание')
        price = int(float(product.get('Цена').replace(',', '.'))) if product.get('Цена') else 0
        price_type = product.get('Вид цены')

        # categories
        category4 = get_or_create_category4(product.get('Родитель4')) if product.get('Родитель4') != "" else None 
        category3 = get_or_create_category3(product.get('Родитель3'), category4) if product.get('Родитель3') != ""  else None 
        category2 = get_or_create_category2(product.get('Родитель2'), category3) if product.get('Родитель2') != ""  else None 
        category1 = get_or_create_category1(product.get('Родитель1'), category2) if product.get('Родитель1') != "" else None
        
        # create or update product 
        product, created = models.Product.objects.update_or_create(
            name=name,
            defaults={
                "item": article,
                "description": description,
                "price": price,
                "price_type": price_type,
                "main_category": category4,
                "sub_category": category3,
                'category': category2,
                'category_sub_category': category1
            }
        )
        print(product)


create_or_update_products(get_product_data())