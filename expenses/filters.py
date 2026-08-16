import django_filters

from .models import Expense


class ExpenseFilter(django_filters.FilterSet):

    start_date = django_filters.DateFilter(
        field_name="expense_date",
        lookup_expr="gte"
    )

    end_date = django_filters.DateFilter(
        field_name="expense_date",
        lookup_expr="lte"
    )

    category = django_filters.CharFilter(
        field_name="category__name",
        lookup_expr="iexact"
    )

    class Meta:
        model = Expense

        fields = [
            "category",
            "start_date",
            "end_date",
        ]