from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from expenses.models import Expense


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        expenses = Expense.objects.filter(user=request.user)

        stats = expenses.aggregate(
            total_expense=Sum("amount"),
            expense_count=Count("id"),
            average_expense=Avg("amount")
        )

        highest = expenses.order_by("-amount").first()

        category_breakdown = (
            expenses
            .values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        monthly = (
            expenses
            .annotate(month=TruncMonth("expense_date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

        return Response({
            **stats,
            "highest_expense": (
                {
                    "title": highest.title,
                    "amount": highest.amount
                }
                if highest else None
            ),
            "category_breakdown": category_breakdown,
            "monthly_spending": monthly,
        })