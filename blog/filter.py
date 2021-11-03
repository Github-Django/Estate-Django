import django_filters
from .models import *


class ProductFilter(django_filters.FilterSet):
    Choices_1 = {
        ('ارزان ترین', 'ارزان ترین'),
        ('گران ترین', 'گران ترین')

    }
    Choices_2 = {
        ('جدید ترین', 'جدیدترین'),
        ('قدیمی ترین', 'قدیمی ترین')

    }

    price_1 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    price_2 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    price = django_filters.ChoiceFilter(choices=Choices_1, method='price_filter')
    area_1 = django_filters.NumberFilter(field_name='area', lookup_expr='gte')
    area_2 = django_filters.NumberFilter(field_name='area', lookup_expr='lte')
    create = django_filters.ChoiceFilter(choices=Choices_1, method='create_filter')

    def price_filter(self, queryset, name, value):
        data = 'unit_price' if value == 'ارزان ترین' else '-unit_price'
        return queryset.order_by(data)
    def create_filter(self, queryset, name, value):
        data = 'created' if value == 'قدیمی ترین' else '-created'
        return queryset.order_by(data)
