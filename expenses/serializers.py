from rest_framework import serializers
from .models import Expense
from categories.serializers import CategorySerializer
from categories.models import Category
from datetime import date

class ExpenseSerializer(serializers.ModelSerializer):
    
    category = CategorySerializer(read_only=True)
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True
    )

    class Meta:
        model = Expense
        fields = [
            "id",
            "title",
            "amount",
            "expense_date",
            "notes",
            "category",
            "category_id",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "category",
        ]
        
    def validate_amount(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )

        return value
    
    def validate_expense_date(self, value):

        if value > date.today():
            raise serializers.ValidationError(
                "Future dates are not allowed."
            )

        return value