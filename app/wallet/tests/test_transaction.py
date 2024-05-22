import pytest

from .factories import TransactionFactory, WalletFactory


@pytest.mark.django_db
def test_transaction_filter_by_wallet(client):
    wallet = WalletFactory()
    TransactionFactory.create_batch(5, wallet=wallet)
    TransactionFactory.create_batch(20)
    response = client.get(f"/api/v1/wallet/transactions/?filter[wallet]={wallet.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 5


@pytest.mark.django_db
def test_transaction_filter_by_txid(client):
    TransactionFactory(txid="unique_txid")
    TransactionFactory.create_batch(20)
    response = client.get("/api/v1/wallet/transactions/?filter[txid]=unique_txid")
    assert response.status_code == 200
    data = response.json()
    assert data["data"][0]["attributes"]["txid"] == "unique_txid"
    assert len(data["data"]) == 1


@pytest.mark.django_db
def test_transaction_pagination(client):
    TransactionFactory.create_batch(30)
    response = client.get("/api/v1/wallet/transactions/?page[size]=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 10
    assert data["meta"]["pagination"]["page"] == 1
    assert data["meta"]["pagination"]["pages"] == 3


@pytest.mark.django_db
def test_transaction_detail(client):
    transaction = TransactionFactory()
    response = client.get(f"/api/v1/wallet/transactions/{transaction.id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == str(transaction.id)
    assert data["data"]["attributes"]["txid"] == transaction.txid
