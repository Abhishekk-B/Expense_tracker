from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ExpenseFilter
from rest_framework.parsers import MultiPartParser, FormParser


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()      # ← Add this line

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    search_fields = [
        "title",
        "notes",
        ]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ExpenseFilter
    
    ordering_fields = [
        "amount",
        "expense_date",
        "created_at",
    ]
    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_queryset(self):
        return Expense.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)