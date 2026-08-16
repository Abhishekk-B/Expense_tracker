import uuid
from django.db import models
from accounts.models import User
from categories.models import Category
import os


def receipt_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    return f"receipts/{uuid.uuid4()}.{ext}"

def delete_old_receipt(instance):
        if not instance.pk:
            return

        try:
            old = Expense.objects.get(pk=instance.pk)
        except Expense.DoesNotExist:
            return

        if old.receipt and old.receipt != instance.receipt:
            if os.path.isfile(old.receipt.path):
                os.remove(old.receipt.path)
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
    receipt = models.ImageField(
        upload_to=receipt_upload_path,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-expense_date"]

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"
                
    def save(self, *args, **kwargs):
        delete_old_receipt(self)
        super().save(*args, **kwargs)