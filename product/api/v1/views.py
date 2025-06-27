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
            ).order_by('created_at').distinct()
        serializer = serializers.CategoriesListSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchApiView(generics.GenericAPIView):
    serializer_class = serializers.SearchSerializer

    def post(self, request):
        serializer = serializers.SearchSerializer(data=request.data)
        serializer.is_valid()
        query =serializer.validated_data.get('search', '')
        # products = models.Product.objects.annotate(
        #     search_field=Concat('name', Value(''), output_field=CharField())
        # ).filter(search_field__icontains=query)
        # # products = document.ProductDocument.search().query('match', name=query)
        #
        # main_category = models.MainCategory.objects.annotate(
        #     search_field=Concat('name', Value(''), output_field=CharField())
        # ).filter(search_field__icontains=query)[:5]
        #
        # sub_category = models.SubCategory.objects.annotate(
        #     search_field=Concat('name', Value(''), output_field=CharField())
        # ).filter(search_field__icontains=query)[:5]
        #
        # sub_sub_category = models.ProductCategory.objects.annotate(
        #     search_field=Concat('name', Value(''), output_field=CharField())
        # ).filter(search_field__icontains=query)[:5]
        #
        # category = models.Category.objects.annotate(
        #     search_field=Concat('name', Value(''), output_field=CharField())
        # ).filter(search_field__icontains=query)[:5]
        #
        # fifth_category = models.FifthCategroy.objects.annotate(
        #     search_field=Concat('name', Value(''), output_field=CharField())
        # ).filter(search_field__icontains=query)[:5]

        item = models.Product.objects.annotate(
            search_field=Concat('item', Value(''), output_field=CharField())
        ).filter(search_field__startswith=query)
        # item = document.ProductDocument.search().query('match', item=query)

        return Response({
            # 'products': serializers.ProductsSerializer(products, many=True).data,
            "item": serializers.ProductsSerializer(item, many=True).data,
        })
    