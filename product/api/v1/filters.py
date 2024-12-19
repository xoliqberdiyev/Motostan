from django_filters import rest_framework as filters

from product import models


class ProductFilter(filters.FilterSet):
    brand = filters.BaseInFilter(field_name='brand__id', lookup_expr='in')
    color = filters.BaseInFilter(field_name='color__id', lookup_expr='in')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min price')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max price')
    info = filters.BaseInFilter(field_name='infos__info_name__id', lookup_expr='in')
    is_discount = filters.BooleanFilter(field_name='is_discount')

    class Meta:
        model = models.Product
        fields = ['brand', 'color', 'min_price', 'max_price', 'info', 'is_discount']
