import factory
from factory import django as factory_django
from wallet.models import Transaction, Wallet


class WalletFactory(factory_django.DjangoModelFactory):
    class Meta:
        model = Wallet

    label = factory.Sequence(lambda n: f"Wallet {n}")
    balance = factory.Faker("pydecimal", right_digits=2, min_value=0, max_value=1000)


class TransactionFactory(factory_django.DjangoModelFactory):
    class Meta:
        model = Transaction

    wallet = factory.SubFactory(WalletFactory)
    txid = factory.Sequence(lambda n: f"tx{n}")
    amount = factory.Faker("pydecimal", left_digits=12, right_digits=18, min_value=-1000000, max_value=1000000)
