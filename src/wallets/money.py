from dataclasses import dataclass

from src.wallets.currency import CurrencyType
from src.wallets.exceptions import NotComparisonException, NegativeValueException


@dataclass
class Money:
    value: float
    currency: CurrencyType

    def __add__(self, other: 'Money') -> 'Money':
        self._check_comparison(other)
        return Money(value=self.value + other.value, currency=self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        self._check_comparison(other)
        return Money(value=self.value - other.value, currency=self.currency)

    def _check_comparison(self, other: 'Money') -> None:
        if self.currency != other.currency:
            raise NotComparisonException(
                f"Cannot operate with different _balances: {self.currency} != {other.currency}"
            )


class Wallet:

    def __init__(self, money: Money):
        self._balances: dict[CurrencyType, Money] = {}
        self.add(money)

    def __getitem__(self, currency: CurrencyType) -> Money:
        return self._balances.get(currency, Money(value=0, currency=currency))

    def __delitem__(self, key) -> None:
        self._balances.pop(key, None)

    def __len__(self):
        return len(self._balances)

    def __contains__(self, item):
        return item in self._balances

    @property
    def currencies(self):
        return set(self._balances.keys())

    def add(self, money: Money) -> 'Wallet':
        cur_balance = self[money.currency]
        self._balances[money.currency] = cur_balance + money
        return self

    def sub(self, money: Money) -> 'Wallet':
        cur_balance = self[money.currency]
        if cur_balance.value < money.value:
            raise NegativeValueException("Cannot withdraw more than available balance")
        self._balances[money.currency] = cur_balance - money
        return self
