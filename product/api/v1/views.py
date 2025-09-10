from django.db.models.expressions import Value
from django.db.models.fields import CharField
from django.db.models.functions.text import Concat
from rest_framework import generics, status, views
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django_filters.rest_framework import DjangoFilterBackend

from product.api.v1 import serializers, filters
from product import models, pagination, document


class DiscountedProductApiView(views.APIView):
    def get(self, request):
        query = models.DiscountedProduct.objects.all()
        serializer = serializers.DiscountedProductSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductByCategoryApiView(generics.ListAPIView):
    pagination_class = pagination.CustomPagination
    serializer_class = serializers.ProductsSerializer

    def get_queryset(self):
        products = models.Product.objects.filter(category__id=self.kwargs.get('category_id'))
        return products

class ProductByFifthCategoryApiView(generics.ListAPIView):
    pagination_class = pagination.CustomPagination
    serializer_class = serializers.ProductsSerializer

    def get_queryset(self):
        products = models.Product.objects.filter(fifth_category__id=self.kwargs.get('category_id'))
        return products

class MainProductByCategoryApiView(generics.ListAPIView):
    pagination_class = pagination.CustomPagination
    serializer_class = serializers.ProductsSerializer

    def get_queryset(self):
        products = models.Product.objects.filter(main_category__id=self.kwargs.get('category_id'))
        return products


class SubProductByCategoryApiView(generics.ListAPIView):
    pagination_class = pagination.CustomPagination
    serializer_class = serializers.ProductsSerializer

    def get_queryset(self):
        products = models.Product.objects.filter(sub_category__id=self.kwargs.get('category_id'))
        return products


class SubSubProductByCategoryApiView(generics.ListAPIView):
    pagination_class = pagination.CustomPagination
    serializer_class = serializers.ProductsSerializer

    def get_queryset(self):
        products = models.Product.objects.filter(category_sub_category__id=self.kwargs.get('category_id'))
        return products


class ProductDetailApiView(views.APIView):
    def get(self, request, id):
        product = models.Product.objects.filter(id=id).prefetch_related('product_infos', 'medias').first()
        if product is None:
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
        categories = models.MainCategory.objects.prefetch_related(
            'sub_categories', 'sub_categories__product_categories', 'sub_categories__product_categories__categories', 'sub_categories__product_categories__categories__fifth_categroy',
            )\
            .filter(is_active=True).order_by('created_at').distinct()
        serializer = serializers.CategoriesListSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchApiView(generics.GenericAPIView):
    serializer_class = serializers.SearchSerializer

    def post(self, request):
        serializer = serializers.SearchSerializer(data=request.data)
        serializer.is_valid()
        query =serializer.validated_data.get('search', '')
        products = models.Product.objects.filter(name__istartswith=query)
        item = models.Product.objects.filter(item__istartswith=query)

        return Response({
            'products': serializers.ProductsSerializer(products, many=True).data,
            "item": serializers.ProductsSerializer(item, many=True).data,
        })
    