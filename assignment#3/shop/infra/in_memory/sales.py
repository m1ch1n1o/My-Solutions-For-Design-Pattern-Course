from dataclasses import dataclass

from shop.core.sales import Sales


@dataclass
class SalesInMemory:
    def __init__(self) -> None:
        self.sales_data = Sales(revenue=0.0, n_receipts=0)

    def read(self) -> Sales:
        return self.sales_data

    def update(self, sales: Sales) -> None:
        sales.revenue += self.sales_data.revenue
        sales.n_receipts = self.sales_data.n_receipts + 1
        self.sales_data = sales
