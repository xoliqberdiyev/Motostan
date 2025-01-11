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
    discounted_price = serializers.SerializerMethodField(method_name='get_discounted_price')

    class Meta:
        model = models.Product
        fields = [
            'id', 'image', 'name', 'name', 'price', 'discount_percentage', 'discounted_price', 'item'
        ]

    def get_discounted_price(self, obj):
        return (obj.price / 100) * obj.discount_percentage if obj.is_discount == True and obj.discount_percentage else 0


class CategorySubCategorySerializer(serializers.ModelSerializer):
    category_number = serializers.SerializerMethodField(method_name='get_category_number')

    class Meta:
        model = models.Category
        fields = ['id', 'name', "image", 'category_number']

    def get_category_number(self, obj):
        return 4

class ProductCategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField(method_name='get_sub_category')
    category_number = serializers.SerializerMethodField(method_name='get_category_number')

    class Meta:
        model = models.ProductCategory
        fields = [
            'id', 'name','category_number', "image",'sub_category',
        ]

    def get_sub_category(self, obj):
        categories = models.Category.objects.filter(product_category=obj)
        return CategorySubCategorySerializer(categories, many=True).data

    def get_category_number(self, obj):
        return 3

class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductBrand
        fields = [
            'id', 'name', 'name'
        ]


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Colors
        fields = [
            'id', 'rgba_name', 'name'
        ]


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InfoName
        fields = [
            'id', 'name'
        ]


class TechInfoSerializer(serializers.ModelSerializer):
    infos = serializers.SerializerMethodField(method_name='get_infos')

    class Meta:
        model = models.TechnicalInfoName
        fields = [
            'id', 'name', 'infos'
        ]

    def get_infos(self, obj):
        infos = models.InfoName.objects.filter(tech_info__id=obj.id)
        return InfoSerializer(infos, many=True).data


class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Colors
        fields = [
            'id', 'rgba_name', 'name'
        ]


class ProductMediasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductMedia
        fields = [
            'id', 'media'
        ]


class ProductTecInfoSerializer(serializers.ModelSerializer):
    tech_info_id = serializers.IntegerField(source='tech_info.id')
    tech_info = serializers.CharField(source='tech_info.name')
    info_name_id = serializers.IntegerField(source='info_name.id')
    info_name = serializers.CharField(source='info_name.name')

    class Meta:
        model = models.ProductInfo
        fields = ['tech_info_id', 'tech_info', 'info_name_id', 'info_name']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(method_name='get_category_name')
    category_id = serializers.SerializerMethodField(method_name='get_category_id')
    brand_name = serializers.SerializerMethodField(method_name='get_brand_name')
    brand_id = serializers.SerializerMethodField(method_name='get_brand_id')
    discount_price = serializers.SerializerMethodField(method_name='get_discount_price')
    medias = serializers.SerializerMethodField(method_name='get_medias')
    colors = serializers.SerializerMethodField(method_name='get_colors')
    infos = serializers.SerializerMethodField(method_name='get_infos')

    class Meta:
        model = models.Product
        fields = [
            'id', 'category_name', 'category_id', 'brand_name', 'brand_id', 'name', 'name', 'price', 'image',
            'discount_percentage', 'is_discount', 'discount_price', 'medias', 'colors', 'infos',
        ]

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_category_id(self, obj):
        return obj.category.id if obj.category else None

    def get_brand_name(self, obj):
        return obj.brand if obj.brand else None

    def get_brand_id(self, obj):
        return obj.brand.id if obj.brand else None

    def get_discount_price(self, obj):
        return obj.price - ((obj.price / 100) * obj.discount_percentage) if obj.is_discount == True and obj.discount_percentage and obj.price > 0 else 0

    def get_colors(self, obj):
        return ColorsSerializer(obj.colors, many=True).data

    def get_medias(self, obj):
        return ProductMediasSerializer(models.ProductMedia.objects.filter(product=obj), many=True).data

    def get_infos(self, obj):
        infos = obj.infos.all()
        return ProductTecInfoSerializer(infos, many=True).data


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
    serializers.SerializerMethodField(method_name='get_category_number')

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
        products = models.Product.objects.filter(main_category=obj)
        return ProductsSerializer(products, many=True).data


class SubCategoryListSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField(method_name='get_categories')
    category_number = serializers.SerializerMethodField(method_name='get_category_number')

    class Meta:
        model = models.SubCategory
        fields = ['id', 'name','category_number', 'categories', "image"]

    def get_categories(self, obj):
        categories = models.ProductCategory.objects.filter(sub_category=obj)
        return ProductCategorySerializer(categories, many=True).data

    def get_category_number(self, obj):
        return 2

class CategoriesListSerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField(method_name='get_sub_categories')
    category_number = serializers.SerializerMethodField(method_name='get_category_number')

    class Meta:
        model = models.MainCategory
        fields = ['id', 'name','category_number', 'sub_categories', "image"]

    def get_sub_categories(self, obj):
        sub_categories = models.SubCategory.objects.filter(main_category=obj)
        return SubCategoryListSerializer(sub_categories, many=True).data

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