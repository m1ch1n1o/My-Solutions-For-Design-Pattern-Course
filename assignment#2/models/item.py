from abc import ABC, abstractmethod
from dataclasses import dataclass

from typing_extensions import Self


class ItemInterface(ABC):
    name: str
    price_per_unit: float
    units: int
    discount_strategy: str = "NoDiscount"
    discount_amount: float = 0
    discount_pack: int = 0

    @abstractmethod
    def total_price(self) -> float:
        pass

    @abstractmethod
    def item_data(self) -> tuple[str, float, int, str, float, float]:
        pass

    @abstractmethod
    def quantity(self) -> int:
        pass


# Define Item class implementing the common interface
@dataclass
class Item(ItemInterface):
    name: str
    price_per_unit: float
    units: int
    discount_strategy: str = "NoDiscount"
    discount_amount: float = 0
    discount_pack: int = 0

    def total_price(self) -> float:
        return round(self.price_per_unit * self.units, 2)

    def item_data(self) -> tuple[str, float, int, str, float, float]:
        return (
            self.name,
            self.price_per_unit,
            1,
            self.discount_strategy,
            self.discount_amount,
            self.discount_pack,
        )

    def quantity(self) -> int:
        return self.units


# Define BatchItem class implementing the common interface
@dataclass
class BatchItem(ItemInterface):
    name: str
    price_per_unit: float
    units: int
    pack_size: int
    discount_strategy: str = "NoDiscount"
    discount_amount: float = 0
    discount_pack: int = 0

    def total_price(self) -> float:
        return round(self.price_per_unit * self.units, 2)

    def item_data(self) -> tuple[str, float, int, str, float, float]:
        return (
            self.name,
            self.price_per_unit,
            self.pack_size,
            self.discount_strategy,
            self.discount_amount,
            self.discount_pack,
        )

    def quantity(self) -> int:
        return self.units * self.pack_size


@dataclass
class ItemBuilder:
    name: str = ""
    price_per_unit: float = 1
    units: int = 1
    pack_size: int = 1
    discount_strategy: str = "NoDiscount"
    discount_amount: float = 0
    discount_pack: int = 0

    def with_name(self, value: str) -> Self:
        self.name = value
        return self

    def and_price(self, value: float) -> Self:
        self.price_per_unit = value
        return self

    def and_units(self, value: int) -> Self:
        self.units = value
        return self

    def and_pack_size(self, value: int) -> Self:
        self.pack_size = value
        return self

    def and_discount(self, value: str) -> Self:
        self.discount_strategy = value
        return self

    def and_discount_amount(self, value: int) -> Self:
        self.discount_amount = value
        return self

    def and_pack_discount(self, value: int) -> Self:
        self.discount_pack = value
        return self

    def build(self) -> ItemInterface:
        if not self.name:
            raise ValueError("Name must be set before building an item.")

        if self.pack_size != 1:
            return BatchItem(
                name=self.name,
                price_per_unit=self.price_per_unit,
                units=self.units,
                pack_size=self.pack_size,
                discount_strategy=self.discount_strategy,
                discount_amount=self.discount_amount,
                discount_pack=self.discount_pack,
            )
        else:
            return Item(
                name=self.name,
                price_per_unit=self.price_per_unit,
                units=self.units,
                discount_strategy=self.discount_strategy,
                discount_amount=self.discount_amount,
                discount_pack=self.discount_pack,
            )
