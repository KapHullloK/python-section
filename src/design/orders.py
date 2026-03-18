from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Order:
    """There is no need to describe anything here."""
    amount: int


class IDiscount(ABC):
    @abstractmethod
    def calculate_discount(self, order: Order) -> int:
        pass


class FixedDiscount(IDiscount):
    def __init__(self, fixed_amount: int):
        self.fixed_amount = fixed_amount

    def calculate_discount(self, order: Order) -> int:
        return self.fixed_amount


class PercentDiscount(IDiscount):
    def __init__(self, percent: float):
        self.percent = percent

    def calculate_discount(self, order: Order) -> int:
        return int(order.amount / 100 * self.percent)


class LoyaltyDiscount(IDiscount):
    def __init__(self, loyalty_percent: float = 0.01):
        self.loyalty_percent = loyalty_percent

    def calculate_discount(self, order: Order) -> int:
        return int(order.amount * self.loyalty_percent)


class DiscountManager:
    def __init__(self, discounts: list[IDiscount] = None):
        if discounts is None:
            discounts = []
        self.discounts: list[IDiscount] = discounts

    def add_discount(self, discount: IDiscount) -> None:
        self.discounts.append(discount)

    def apply_discounts(self, order: Order) -> Order:
        total_discount = sum(discount.calculate_discount(order) for discount in self.discounts)
        return Order(
            amount=max(1, order.amount - total_discount)
        )
