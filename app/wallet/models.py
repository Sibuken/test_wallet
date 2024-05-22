from django.db import models
from django.db.models import CheckConstraint, Q


# Create your models here.


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        constraints = [CheckConstraint(check=Q(balance__gte=0), name="balance_gte_0")]


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name="transactions", on_delete=models.CASCADE)
    txid = models.CharField(max_length=255, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=30, decimal_places=18)
