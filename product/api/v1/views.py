from django.db.models.expressions import Value
from django.db.models.fields import CharField
from django.db.models.functions.text import Concat
from rest_framework import generics, status, views
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django_filters.rest_framework import DjangoFilterBackend

from product.api.v1 import serializers, filters
from product import models, pagination


class DiscountedProductApiView(views.APIView):
    """
    Bu apida homepagedagi "Chegirmadagi mahsulotlar" listini get qilib olasizlar,
    apidan keladigan reponse: id, image_uz, image_ru, product(productning id)
    """
    def get(self, request):
        query = models.DiscountedProduct.objects.all()
        serializer = serializers.DiscountedProductSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopProductApiView(views.APIView):
    """
    Bu apida homepagedagi "Xit mahsulotlar" listini get qilib olasizlar,
    faqat is_discount = True bolganlarni 5 tasi chiqadi,
    apidan keladigan response: id, image, name_uz, name_ru, price, discount_percentage, discounted_price
    """
    def get(self, request):
        products = models.Product.objects.filter(is_top=True).exclude(image='')[:5]
        serializer = serializers.ProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductBrandApiView(views.APIView):
    """
    Bu apida brandlar listini olishingiz mumkin,
    apidan keladigan response: id, name_uz, name_ru
    """
    def get(self, request):
        brands = models.ProductBrand.objects.all()
        serializer = serializers.ProductBrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductColorApiView(views.APIView):
    """
    Bu apida rangalar listini olishingiz mumkin,
    apidan keladigan respone: id, rgba_name, name
    """
    def get(self, request):
        colors = models.Colors.objects.all()
        serializer = serializers.ProductColorSerializer(colors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductInfoByCategoryApiView(views.APIView):
    """
    Bu apida categoryga tegishli bolagan technical informations larni olishingiz mumkin, filterlash uchun.
    apidan keladigan response: id, name, infos{}
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category_id', openapi.IN_PATH,
                description='category id kiritilishi kerak',
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, category_id):
        try:
            category = models.ProductCategory.objects.get(id=category_id)
        except models.ProductCategory.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_400_BAD_REQUEST)
        tech_infos = models.TechnicalInfoName.objects.filter(category=category)
        serializer = serializers.TechInfoSerializer(tech_infos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductByCategoryApiView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ProductFilter
    pagination_class = pagination.CustomPagination
    serializer_class = serializers.ProductsSerializer


    def get_queryset(self):
        products = models.Product.objects.filter(category__id=self.kwargs.get('category_id')).exclude(image='')
        return products

class MainProductByCategoryApiView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ProductFilter
    pagination_class = pagination.CustomPagination
    serializer_class = serializers.ProductsSerializer


    def get_queryset(self):
        products = models.Product.objects.filter(main_category__id=self.kwargs.get('category_id')).exclude(image='')
        return products


class SubProductByCategoryApiView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ProductFilter
    pagination_class = pagination.CustomPagination
    serializer_class = serializers.ProductsSerializer


    def get_queryset(self):
        products = models.Product.objects.filter(sub_category__id=self.kwargs.get('category_id')).exclude(image='')
        return products


class SubSubProductByCategoryApiView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ProductFilter
    pagination_class = pagination.CustomPagination
    serializer_class = serializers.ProductsSerializer


    def get_queryset(self):
        products = models.Product.objects.filter(category_sub_category__id=self.kwargs.get('category_id')).exclude(image='')
        return products


class ProductDetailApiView(views.APIView):
    def get(self, request, id):
        try:
            product = models.Product.objects.get(id=id)
        except models.Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MainCategoryApiView(views.APIView):
    def get(self, request):
        main_category = models.MainCategory.objects.all()
        serializer = serializers.MainCategorySerializer(main_category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesListApiView(views.APIView):
    def get(self, request):
        categories = models.MainCategory.objects.all()
        serializer = serializers.CategoriesListSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchApiView(generics.GenericAPIView):
    serializer_class = serializers.SearchSerializer

    def post(self, request):
        serializer = serializers.SearchSerializer(data=request.data)
        serializer.is_valid()
        query =serializer.validated_data.get('search', '')
        products = models.Product.objects.annotate(
            search_field=Concat('name', Value(''), output_field=CharField())
        ).filter(search_field__icontains=query)[:5].exclude(image='')

        main_category = models.MainCategory.objects.annotate(
            search_field=Concat('name', Value(''), output_field=CharField())
        ).filter(search_field__icontains=query)[:5]

        sub_category = models.SubCategory.objects.annotate(
            search_field=Concat('name', Value(''), output_field=CharField())
        ).filter(search_field__icontains=query)[:5]

        sub_sub_category = models.ProductCategory.objects.annotate(
            search_field=Concat('name', Value(''), output_field=CharField())
        ).filter(search_field__icontains=query)[:5]

        category = models.Category.objects.annotate(
            search_field=Concat('name', Value(''), output_field=CharField())
        ).filter(search_field__icontains=query)[:5]
        item = models.Product.objects.annotate(
            search_field=Concat('item', Value(''), output_field=CharField())
        ).filter(search_field__icontains=query)[:5].exclude(image='')
        return Response({
            'products': serializers.ProductsSerializer(products, many=True).data,
            'main_categories': serializers.MainCategorySearchSerializer(main_category, many=True).data,
            'sub_categories': serializers.SubCategorySearchSerializer(sub_category, many=True).data,
            'sub_sub_categories': serializers.ProductCategorySearchSerializer(sub_sub_category, many=True).data,
            'categories': serializers.CategorySearchSerializer(category, many=True).data,
            "item": serializers.ProductsSerializer(item, many=True).data,
        })