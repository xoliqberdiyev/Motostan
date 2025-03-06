import os
import django
from django.db.models import Q
from django.db import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

import requests, json 
from django.core.exceptions import ObjectDoesNotExist

from product import models
from django.db import transaction
from django.db.models import Count



def get_data():
    r = requests.get('https://moto.odilsoft.uz/index.php')
    data = r.json()
    return data       

def get_or_create_category5(category5, main_category):
    if category5 == "":
        return None 
    else:
        try:
            category, created = models.FifthCategroy.objects.get_or_create(
                name=category5, 
                category=main_category
            )
        except IntegrityError: 
            category = models.FifthCategroy.objects.get(name=category5)
            created = False
        return category

def get_or_create_category4(category4, main_category):
    if category4 == "":
        return None
    else:
        try:
            category, created = models.Category.objects.get_or_create(
                name=category4, 
                product_category=main_category
            )
        except IntegrityError: 
            category = models.Category.objects.get(name=category4)
            created = False
        return category

def get_or_create_category3(category3, main_category):
    if category3 == "":
        return None
    else:
        try:
            category, created = models.ProductCategory.objects.get_or_create(
                name=category3, 
                sub_category=main_category
            )
        except IntegrityError:
            category = models.ProductCategory.objects.get(name=category3)
            created = False
        return category

def get_or_create_category2(category2, main_category):
    if category2 == "":
        return None
    else:
        try:
            category, created = models.SubCategory.objects.get_or_create(
                name=category2, 
                main_category=main_category
            )
        except IntegrityError: 
            category = models.SubCategory.objects.get(name=category2)
            created = False
        return category

def get_or_create_category1(category1):
    try:
        category, created = models.MainCategory.objects.get_or_create(
            name=category1, 
        )
    except IntegrityError:  
        category = models.SubCategory.objects.get(name=category1)
        created = False
    return category


def replace_slash_with_space(string):
    data = string.replace("/", " ") if "/" in string else string
    return data

def delete_data(data):
    main_categories = models.MainCategory.objects.all()
    main_category_names = {main_catergory.name for main_catergory in main_categories}
    main_category_1c_names = {product['category']['level1'] for product in data}
    deleted_main_category = main_category_names - main_category_1c_names
    if deleted_main_category:
        models.MainCategory.objects.filter(name__in=deleted_main_category).delete()
    
    sub_category_names = {category.name for category in models.SubCategory.objects.all()}
    sub_category_1c_names = {product['category']['level2'] for product in data}
    deleted_sub_categories = sub_category_names - sub_category_1c_names
    if deleted_sub_categories:
        models.SubCategory.objects.filter(name__in=deleted_sub_categories).delete()

    product_category_names = {category.name for category in models.ProductCategory.objects.all()}
    prodcut_category_1c_names = {product['category']['level3'] for product in data}
    deleted_product_categories = product_category_names - prodcut_category_1c_names
    if deleted_product_categories:
        models.ProductCategory.objects.filter(name__in=deleted_product_categories).delete()
    
    category_names = {category.name for category in models.Category.objects.all()}
    category_1c_names = {product['category']['level4'] for product in data}
    deleted_categories = category_names - category_1c_names
    if deleted_categories:
        models.Category.objects.filter(name__in=deleted_categories).delete()
    
    fifth_category_names = {category.name for category in models.FifthCategroy.objects.all()}
    fifth_category_1c_names = {product['category']['level5'] for product in data}
    deleted_fifth_categories = fifth_category_names - fifth_category_1c_names
    if deleted_fifth_categories:
        models.FifthCategroy.objects.filter(name__in=deleted_fifth_categories).delete()

    product_names = {product.name for product in models.Product.objects.all()}
    product_1_names = {replace_slash_with_space(product['display_name']) for product in data}

    deleted_products = product_names - product_1_names
    if deleted_products:
        models.Product.objects.filter(name__in=deleted_products).delete()

def create_or_update_products(data):
    delete_data(data)
    i = 0
    for product in data:
        name_text = product['display_name']
        main_category = product['category']['level1']
        if main_category == None or main_category == '':
            continue
        if name_text == None or name_text == '':
            continue 
        
        name = replace_slash_with_space(name_text)
        article = replace_slash_with_space(product.get('article'))
        description = replace_slash_with_space(product.get('description'))
        price = product["price"] if product['price'] != "" or product['price'] != None else 0
        if price != None:
            price = float(price)
        price_type = product['price_type']
        
        # categories
        category1 = get_or_create_category1(main_category)
        category2 = get_or_create_category2(product['category']['level2'], category1)  
        category3 = get_or_create_category3(product['category']['level3'], category2)  
        category4 = get_or_create_category4(product['category']['level4'], category3) 
        category5 = get_or_create_category5(product['category']['level5'], category4)  
        p, created = models.Product.objects.update_or_create(
            item=article,
            defaults={
                "name": name,
                "description": description,
                "price": price if price != None else 0,
                "price_type": price_type,
                "quantity_left": product["quantity"],
                "main_category": category1,
                "sub_category": category2,
                'category': category3,
                'category_sub_category': category4,
                "fifth_category": category5,
            }
        )
        if product['additional_properties'] != []:
            for key,value in product['additional_properties'].items():
                info, created = models.ProductInfo.objects.update_or_create(name=key,product=p,text=value)
        i+=1
    print(f'{i} product created')
create_or_update_products(get_data())
