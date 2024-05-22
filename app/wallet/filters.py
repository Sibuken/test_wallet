from django_filters import FilterSet

from .models import Transaction, Wallet


class TransactionFilter(FilterSet):
    class Meta:
        model = Transaction
        fields = {
            "wallet": ["exact"],
            "txid": ["exact"],
        }


class WalletFilter(FilterSet):
    class Meta:
        model = Wallet
        fields = {
            "id": ["exact"],
        }
