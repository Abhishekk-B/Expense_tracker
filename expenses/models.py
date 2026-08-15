import uuid
from django.db import models
from accounts.models import User
from categories.models import Category

class Expense(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="expenses"
    )

    title = models.CharField(max_length=200)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    expense_date = models.DateField()

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-expense_date"]

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"