from rest_framework_json_api.views import ReadOnlyModelViewSet

from .filters import TransactionFilter, WalletFilter
from .models import Transaction, Wallet
from .serializers import TransactionSerializer, WalletSerializer


# Create your views here.


class WalletViewSet(ReadOnlyModelViewSet):
    queryset = Wallet.objects.all().order_by("id")
    serializer_class = WalletSerializer
    filterset_class = WalletFilter


class TransactionViewSet(ReadOnlyModelViewSet):
    queryset = Transaction.objects.all().order_by("id")
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter
