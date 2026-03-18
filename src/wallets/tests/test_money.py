import math

import pytest

from src.wallets.currency import CurrencyType
from src.wallets.exceptions import NegativeValueException, NotComparisonException
from src.wallets.money import Money, Wallet


class TestMoney:
    @pytest.fixture
    def money1(self):
        return Money(value=1, currency=CurrencyType.RUB)

    @pytest.fixture
    def money2(self):
        return Money(value=2, currency=CurrencyType.RUB)

    @pytest.fixture
    def money3(self):
        return Money(value=3, currency=CurrencyType.RUB)

    def test_add(self, money1, money2, money3):
        assert money1 + money2 == money3

    def test_sub(self, money1, money2, money3):
        assert money3 - money2 == money1

    def test_other_currency(self, money1, money2, money3):
        with pytest.raises(NotComparisonException):
            Money(value=1, currency=CurrencyType.RUB) + Money(value=1, currency=CurrencyType.USD)


class TestWallet:
    @pytest.fixture
    def money(self):
        return Money(value=500, currency=CurrencyType.RUB)

    @pytest.fixture
    def wallet(self, money):
        return Wallet(money)

    def test_get__exists(self, wallet, money):
        assert wallet[CurrencyType.RUB] == money

    def test_get__empty(self, wallet):
        assert wallet[CurrencyType.USD] == Money(value=0, currency=CurrencyType.USD)

    def test_del__exists(self, wallet):
        del wallet[CurrencyType.RUB]
        assert CurrencyType.RUB not in wallet.currencies

    def test_del__empty(self, wallet):
        del wallet[CurrencyType.USD]
        assert CurrencyType.USD not in wallet.currencies

    def test_len_currencies(self, wallet):
        assert len(wallet) == 1

    def test_contains(self, wallet):
        assert CurrencyType.RUB in wallet
        assert CurrencyType.USD not in wallet

    def test_add(self, wallet):
        wallet.add(Money(value=100, currency=CurrencyType.RUB)).add(Money(value=200, currency=CurrencyType.RUB))
        assert wallet[CurrencyType.RUB] == Money(value=800, currency=CurrencyType.RUB)

    def test_sub(self, wallet):
        wallet.sub(Money(value=100, currency=CurrencyType.RUB)).sub(Money(value=200, currency=CurrencyType.RUB))
        assert wallet[CurrencyType.RUB] == Money(value=200, currency=CurrencyType.RUB)

    def test_sub__negative(self, wallet):
        with pytest.raises(NegativeValueException):
            wallet.sub(Money(value=math.inf, currency=CurrencyType.RUB))
