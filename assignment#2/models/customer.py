from abc import ABC, abstractmethod
from random import choice, randint

from DAO_files.items_DAO import ItemDatabaseProtocol
from models.item import ItemInterface


class PaymentMethod(ABC):
    @abstractmethod
    def pay(self) -> None:
        pass


class PayWithCash(PaymentMethod):
    def pay(self) -> None:
        print("Customer paid with Cash")


class PayWithCard(PaymentMethod):
    def pay(self) -> None:
        print("Customer paid with Card")


class CustomerInterface:
    def __init__(self, items_db: ItemDatabaseProtocol):
        self.items_db = items_db
        self.items_list = self.items_db.get_items()

    @abstractmethod
    def choose_items(self) -> list[ItemInterface]:
        pass

    @abstractmethod
    def choose_payment_method(self) -> PaymentMethod:
        pass


class RandomCustomer(CustomerInterface):
    def __init__(self, items_db: ItemDatabaseProtocol):
        super().__init__(items_db)
        self.chosen_items: list[ItemInterface] = []
        self.payment_methods = [PayWithCash(), PayWithCard()]

    def choose_items(self) -> list[ItemInterface]:
        for item in self.items_list:
            if randint(0, 1) == 1:
                quantity = randint(1, 10)
                item.units = quantity
                self.chosen_items.append(item)

        return self.chosen_items

    def choose_payment_method(self) -> PaymentMethod:
        return choice(self.payment_methods)
