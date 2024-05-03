from typing import Any

from models.discount import Discount
from models.item import ItemInterface


class Receipt:
    customer_id = 0

    def __init__(self, items: list[ItemInterface] | None = None) -> None:
        self.customer_id = Receipt.customer_id
        Receipt.customer_id += 1
        self.items = items if items is not None else []

    def add_item(self, item: ItemInterface) -> None:
        Discount.apply_discount_to_item(item, Receipt.customer_id)
        self.items.append(item)

    @staticmethod
    def _set_customer_id(num: int) -> None:
        Receipt.customer_id = num

    def calculate_total(self) -> Any:
        total_cost = sum(item.total_price() for item in self.items)
        return round(total_cost, 2)

    def generate_receipt(self) -> str:
        receipt_info = "Receipt:\n"
        receipt_info += "Product        | Units | Price | Total\n"
        receipt_info += "-------------------------------------\n"

        for item in self.items:
            receipt_info += (
                f"{item.name.ljust(15)}|"
                f" {str(item.quantity()).ljust(6)}|"
                f" ${str(round(item.price_per_unit, 2)).ljust(6)}|"
                f" ${str(round(item.total_price(), 2)).ljust(6)}\n"
            )

        receipt_info += "-------------------------------------\n"
        receipt_info += f"Total: ${round(self.calculate_total(), 2):.2f}\n"

        print(receipt_info)
        return receipt_info
