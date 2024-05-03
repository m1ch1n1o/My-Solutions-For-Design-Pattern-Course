from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from models.item import BatchItem, ItemInterface


# Define Discount protocol
class Discount(ABC):
    @staticmethod
    def apply_discount_to_item(item: ItemInterface, customer_id: int) -> None:
        (
            NoDiscount(
                ItemDiscount(BatchDiscount(CustomerNumberDiscount(customer_id)))
            ).execute(item)
        )

    @abstractmethod
    def apply_discount(self, item: ItemInterface) -> Any:
        pass

    @abstractmethod
    def execute(self, item: ItemInterface) -> None:
        pass


# Define Discount implementations
@dataclass
class NoDiscount(Discount):
    following: Discount

    def execute(self, item: ItemInterface) -> None:
        if item.discount_strategy == "NoDiscount":
            self.apply_discount(item)

        self.following.execute(item)

    def apply_discount(self, item: ItemInterface) -> Any:
        return item.total_price()


@dataclass
class ItemDiscount(Discount):
    following: Discount
    discount_percentage: float = 0

    def apply_discount(self, item: ItemInterface) -> Any:
        item.price_per_unit -= item.price_per_unit * (self.discount_percentage / 100)
        item.price_per_unit = round(item.price_per_unit, 2)
        return round(item.total_price(), 2)

    def execute(self, item: ItemInterface) -> None:
        if item.discount_strategy == "ItemDiscount":
            self.discount_percentage = item.discount_amount
            self.apply_discount(item)

        self.following.execute(item)


@dataclass
class BatchDiscount(Discount):
    following: Discount
    pack_size: int = 0
    discount_percentage: float = 0

    def apply_discount(self, item: ItemInterface) -> Any:
        if isinstance(item, BatchItem) and item.pack_size == self.pack_size:
            item.price_per_unit -= item.price_per_unit * (
                self.discount_percentage / 100
            )
            item.price_per_unit = round(item.price_per_unit, 2)
            return round(item.total_price(), 2)
        return round(item.total_price(), 2)

    def execute(self, item: ItemInterface) -> None:
        if item.discount_strategy == "BatchDiscount":
            self.pack_size = item.discount_pack
            self.discount_percentage = item.discount_amount
            self.apply_discount(item)

        self.following.execute(item)


@dataclass
class CustomerNumberDiscount(Discount):
    customer_id: int
    discount_percentage: float = 17.00

    def apply_discount(self, item: ItemInterface) -> Any:
        if is_prime_number(self.customer_id):
            item.price_per_unit -= item.price_per_unit * (
                self.discount_percentage / 100
            )
            return round(item.total_price(), 2)
        return round(item.total_price(), 2)

    def execute(self, item: ItemInterface) -> None:
        self.apply_discount(item)


# Helper methods:
def is_prime_number(num: int) -> bool:
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
