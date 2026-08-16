from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):

    def validate_receipt(self, value):
        if value:
            # Maximum 2 MB
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError(
                    "Receipt size cannot exceed 2 MB."
                )

            # Allowed extensions
            allowed = [".jpg", ".jpeg", ".png"]
            extension = value.name.lower().split(".")[-1]

            if f".{extension}" not in allowed:
                raise serializers.ValidationError(
                    "Only JPG and PNG images are allowed."
                )

        return value

    class Meta:
        model = Expense
        fields = "__all__"
        read_only_fields = ["user"]