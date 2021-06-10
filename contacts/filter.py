import django_filters
from .models import Contact

class ContactFilter(django_filters.FilterSet):
    cn = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Contact
        fields = ['cn',]