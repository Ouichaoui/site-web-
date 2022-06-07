import django_filters
from .models import *
from django_filters import DateFilter,TimeFilter


class Productfilter(django_filters.FilterSet) :
    name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')


    class Meta:
        model = Product
        fields = ['name','brand','catalog','price']

    def author_sort_books(self, queryset, name, value):
        return queryset