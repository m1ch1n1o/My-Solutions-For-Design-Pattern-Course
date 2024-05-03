from typing import Optional, Union

import typer
from typing_extensions import Self

from DAO_files.revenue_DAO import RevenueDatabaseProtocol
from DAO_files.sales_DAO import SalesDatabaseProtocol
from models.customer import PaymentMethod, PayWithCard, PayWithCash
from models.item import ItemInterface
from models.receipt import Receipt


class Cashier:
    def __init__(
        self, revenue_db: RevenueDatabaseProtocol, sales_db: SalesDatabaseProtocol
    ):
        self.current_receipt: Optional[Receipt] = None
        self.sales_report: dict[str, int] = {}
        self.revenue_report: dict[str, float] = {}
        self.revenue_db = revenue_db
        self.sales_db = sales_db

    def open_receipt(self) -> Self:
        if self.current_receipt:
            raise ValueError(
                "Please close the current receipt before opening a new one."
            )

        self.current_receipt = Receipt()
        return self

    def add_item_to_receipt(self, item: ItemInterface) -> Self:
        if not self.current_receipt:
            raise ValueError("Please open a receipt before adding items.")

        self.current_receipt.add_item(item)

        self.sales_report[item.name] = (
            self.sales_report.get(item.name, 0) + item.quantity()
        )
        return self

    def add_items_to_receipt(self, items: list[ItemInterface]) -> Self:
        for item in items:
            self.add_item_to_receipt(item)
        return self

    def close_receipt(self, payment_method: PaymentMethod) -> Self:
        if not self.current_receipt:
            raise ValueError("No open receipt. Please open a receipt first.")

        total_cost = self.current_receipt.calculate_total()
        self.current_receipt = None

        if isinstance(payment_method, PayWithCash):
            self.revenue_report["Cash"] = (
                self.revenue_report.get("Cash", 0) + total_cost
            )
        elif isinstance(payment_method, PayWithCard):
            self.revenue_report["Card"] = (
                self.revenue_report.get("Card", 0) + total_cost
            )

        # return f"Payment Status: {payment_method.pay()}\n{receipt_info}"
        return self

    def generate_receipt(self) -> Self:
        if not self.current_receipt:
            raise ValueError("Please open a receipt before adding items.")

        self.current_receipt.generate_receipt()
        return self

    def generate_x_report(self) -> Self:
        items_sold = self.sales_report
        revenue_data = self.revenue_report

        user_input = typer.prompt("Do you want to make X report? ")
        while user_input != "y" and user_input != "n":
            user_input = typer.prompt("Please enter 'y' for yes, 'n' for no")

        if user_input == "n":
            return self

        self.print_report(items_sold, "Sales Report", ["Product", "Sales"])

        self.print_report(revenue_data, "Revenue Report", ["Payment", "Revenue"])

        return self

    @staticmethod
    def print_report(
        report_info: Union[dict[str, int], dict[str, float]],
        title: str,
        headers: list[str],
    ) -> None:
        x_report_info = ""

        # Extract report information
        report_data = []
        for item_name, count in report_info.items():
            report_data.append([item_name, str(round(count, 2))])

        # Calculate maximum lengths for each column
        max_lengths = [
            max(len(row[i]) for row in [headers] + report_data)
            for i in range(len(headers))
        ]

        # Construct Report
        x_report_info += f"{title}:\n"
        max_width = max(sum(max_lengths) + len(max_lengths) * 3, len(title))
        line = "-" * max_width

        x_report_info = f"\n{x_report_info.strip()}\n{line}\n"
        for row in [headers] + report_data:
            row_info = " | ".join(
                f"{col.ljust(max_lengths[i])}" for i, col in enumerate(row)
            )
            x_report_info += f" {row_info}\n"

        print(x_report_info)

    def generate_z_report(self, count: int) -> int:
        user_input = typer.prompt("Do you want to make Z report? ")
        while user_input != "y" and user_input != "n":
            user_input = typer.prompt("Please enter 'y' for yes, 'n' for no")

        revenue_data = self.revenue_report
        for payment_method, revenue in revenue_data.items():
            self.revenue_db.update_revenue_report(payment_method, revenue)

        sales_data = self.sales_report
        for item_name, sales in sales_data.items():
            self.sales_db.insert_sales_record(item_name, sales)

        if user_input == "n":
            return count

        self.revenue_report = {}
        self.sales_report = {}

        count += 1
        return count
