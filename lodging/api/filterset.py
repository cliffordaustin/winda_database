from django_filters import rest_framework as filters
from rest_framework import fields
from lodging.models import Stays, TYPE_OF_STAY, PRICING_TYPE


# class BookFilter(filters.FilterSet):
#     min_price = filters.NumberFilter(field_name="", lookup_expr="gte")
#     max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
#     book_category = filters.ChoiceFilter(
#         field_name="categories", lookup_expr="icontains", choices=BOOK_CATEGORY
#     )
#     book_condition = filters.ChoiceFilter(
#         field_name="condition", choices=BOOK_CONDITION
#     )

#     class Meta:
#         model = Book
#         fields = [
#             "min_price",
#             "max_price",
#             "book_category",
#             "book_condition",
#         ]