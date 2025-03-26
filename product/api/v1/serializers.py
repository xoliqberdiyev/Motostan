from unicodedata import category

from rest_framework import serializers

from product import models


class DiscountedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiscountedProduct
        fields = [
            'id', 'image_uz', 'image_ru', 'product'
        ]


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            'id', 'image', 'name', 'name', 'price','item', 'price_type', 'main_category', 'sub_category', 'category', 'category_sub_category', 'fifth_category',
        ]


class FifthCategorySerializer(serializers.ModelSerializer):
    category_number = serializers.SerializerMethodField(method_name='get_category_number')

    class Meta:
        model = models.FifthCategroy
        fields = ['id', 'name', "image", 'category_number']

    def get_category_number(self, obj):
        return 5

class CategorySubCategorySerializer(serializers.ModelSerializer):
    category_number = serializers.SerializerMethodField(method_name='get_category_number')
    fifth_category = serializers.SerializerMethodField(method_name='get_sub_category')

    class Meta:
        model = models.Category
        fields = ['id', 'name', "image", 'category_number', 'fifth_category']

    def get_category_number(self, obj):
        return 4

    def get_sub_category(self, obj):
        return FifthCategorySerializer(obj.fifth_categroy, many=True).data if obj.fifth_categroy else None


class ProductCategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField(method_name='get_sub_category')
    category_number = serializers.SerializerMethodField(method_name='get_category_number')

    class Meta:
        model = models.ProductCategory
        fields = [
            'id', 'name','category_number', "image",'sub_category',
        ]

    def get_sub_category(self, obj):
        return CategorySubCategorySerializer(obj.categories, many=True).data

    def get_category_number(self, obj):
        return 3


class ProductMediasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductMedia
        fields = [
            'id', 'media'
        ]

class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductInfo
        fields = ['id', 'name', 'text']


class ProductSerializer(serializers.ModelSerializer):
    infos = serializers.SerializerMethodField(method_name="get_infos")
    medias = serializers.SerializerMethodField(method_name='get_medias')

    class Meta:
        model = models.Product
        fields = [
            'id', 'name', 'description','quantity_left', 'price', 'price_type', 'item', 'image', 'infos', 'medias'
        ]

    def get_medias(self, obj):
        return ProductMediasSerializer(obj.medias, many=True).data

    def get_infos(self, obj):
        return ProductInfoSerializer(obj.product_infos, many=True).data if obj.product_infos else None


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(method_name='get_products')

    class Meta:
        model = models.ProductCategory
        fields = ['id', 'name', 'products']

    def get_products(self, obj):
        products = models.Product.objects.filter(category=obj)
        return ProductsSerializer(products, many=True).data


class SubCategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(method_name='get_products')
    categories = serializers.SerializerMethodField(method_name='get_categories')

    class Meta:
        model = models.SubCategory
        fields = [
            'id', 'name', 'products', 'categories',
        ]

    def get_products(self, obj):
        products = models.Product.objects.filter(sub_category=obj)
        return ProductsSerializer(products, many=True).data

    def get_categories(self, obj):
        categories = models.ProductCategory.objects.filter(sub_category=obj)
        return CategorySerializer(categories, many=True).data


class MainCategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(method_name='get_products')
    categories = serializers.SerializerMethodField(method_name='get_categories')

    class Meta:
        model = models.MainCategory
        fields = [
            'id', 'name', 'categories', 'products',
        ]

    def get_categories(self, obj):
        categories = models.SubCategory.objects.filter(main_category=obj)
        return SubCategorySerializer(categories, many=True).data

    def get_products(self, obj):
        products = models.Product.objects.filter(main_category=obj).exclude(image='')
        return ProductsSerializer(products, many=True).data


class SubCategoryListSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField(method_name='get_categories')
    category_number = serializers.SerializerMethodField(method_name='get_category_number')

    class Meta:
        model = models.SubCategory
        fields = ['id', 'name','category_number', 'categories', "image"]

    def get_categories(self, obj):
        return ProductCategorySerializer(obj.product_categories, many=True).data

    def get_category_number(self, obj):
        return 2

class CategoriesListSerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField(method_name='get_sub_categories')
    category_number = serializers.SerializerMethodField(method_name='get_category_number')

    class Meta:
        model = models.MainCategory
        fields = ['id', 'name','category_number', 'sub_categories', "image"]

    def get_sub_categories(self, obj):
        return SubCategoryListSerializer(obj.sub_categories, many=True).data
        
    
    def get_category_number(self, obj):
        return 1

class FilterCategoryIdSerializer(serializers.SerializerMethodField):
    main_category_id = serializers.IntegerField(required=False)
    sub_category_id = serializers.IntegerField(required=False)
    sub_sub_category_id = serializers.IntegerField(required=False)
    category_id = serializers.IntegerField(required=False)


class SearchSerializer(serializers.Serializer):
    search = serializers.CharField(required=True)



class MainCategorySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MainCategory
        fields = ['id', 'name']



class SubCategorySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubCategory
        fields = ['id', 'name']



class ProductCategorySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ['id', 'name']


class CategorySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name']