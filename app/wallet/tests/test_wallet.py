from django.db.models import F
from django.db.utils import IntegrityError

import pytest
from wallet.models import Wallet

from .factories import WalletFactory


@pytest.mark.django_db
def test_wallet_list(client):
    WalletFactory.create_batch(3)
    response = client.get("/api/v1/wallet/wallets/")
    assert response.status_code == 200
    assert response.json()["meta"]["pagination"]["count"] == 3


@pytest.mark.django_db
def test_wallet_filter(client):
    wallets = WalletFactory.create_batch(3)
    wallet = wallets[0]
    response = client.get(f"/api/v1/wallet/wallets/?filter[id]={wallet.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["meta"]["pagination"]["count"] == 1
    assert data["data"][0]["id"] == str(wallet.id)


@pytest.mark.django_db
def test_wallet_pagination(client):
    WalletFactory.create_batch(20)
    response = client.get("/api/v1/wallet/wallets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 10
    assert data["meta"]["pagination"]["count"] == 20
    assert data["meta"]["pagination"]["page"] == 1
    assert data["meta"]["pagination"]["pages"] == 2
    response = client.get("/api/v1/wallet/wallets/?page[number]=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 10
    assert data["meta"]["pagination"]["count"] == 20
    assert data["meta"]["pagination"]["page"] == 2
    assert data["meta"]["pagination"]["pages"] == 2


@pytest.mark.django_db
def test_wallet_detail(client):
    wallet = WalletFactory()
    response = client.get(f"/api/v1/wallet/wallets/{wallet.id}/", HTTP_ACCEPT="application/vnd.api+json")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == str(wallet.id)


@pytest.mark.django_db
def test_wallet_negative_balance_constraint():
    try:
        Wallet.objects.create(label="Test Wallet", balance=-10.00)
        pytest.fail("IntegrityError was not raised for a negative balance")
    except IntegrityError as e:
        assert "balance_gte_0" in str(e)


@pytest.mark.django_db
def test_update_wallet_to_negative_balance():
    """Test that updating a Wallet to a negative balance is prevented by constraints."""
    # Create a wallet with a positive balance initially
    wallet = WalletFactory(balance=100.00)

    try:
        Wallet.objects.filter(id=wallet.id).update(balance=F("balance") - 200.00)
    except IntegrityError as e:
        assert "balance_gte_0" in str(e)
