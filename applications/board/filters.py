from django_filters import rest_framework as filters

from applications.board.models import Post


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')  # icontains -- регистр не имеет значения
    price_from = filters.NumberFilter(field_name='price', lookup_expr= 'gte')  # price >=
    price_to = filters.NumberFilter(field_name='price', lookup_expr='lte') # <=
    class Meta:
        model = Post
        # fields = ['category','price',]
        fields = ['name','price_from','price_to','category', ]