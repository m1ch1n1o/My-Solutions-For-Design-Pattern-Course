import unittest
from unittest.mock import patch

from DAO_files.revenue_DAO import InMemoryRevenueDatabase
from DAO_files.sales_DAO import InMemorySalesDatabase
from models.cashier import Cashier, PayWithCash
from models.item import ItemBuilder


class TestCashier(unittest.TestCase):
    def setUp(self) -> None:
        self.revenue_db = InMemoryRevenueDatabase()
        self.sales_db = InMemorySalesDatabase()
        self.cashier = Cashier(self.revenue_db, self.sales_db)

    def test_open_receipt(self) -> None:
        self.assertIsNone(self.cashier.current_receipt)
        self.cashier.open_receipt()
        self.assertIsNotNone(self.cashier.current_receipt)

    def test_add_item_to_receipt(self) -> None:
        item = ItemBuilder().with_name("Test Item").and_price(10).and_units(3).build()
        self.cashier.open_receipt()
        self.cashier.add_item_to_receipt(item)
        self.assertEqual(len(self.cashier.sales_report), 1)
        self.assertEqual(self.cashier.sales_report[item.name], item.units)

    def test_add_items_to_receipt(self) -> None:
        items = [
            ItemBuilder().with_name("Item 1").and_price(5).and_units(2).build(),
            ItemBuilder().with_name("Item 2").and_price(8).and_units(5).build(),
        ]
        self.cashier.open_receipt()
        self.cashier.add_items_to_receipt(items)
        self.assertEqual(len(self.cashier.sales_report), 2)

    def test_close_receipt_with_cash_payment(self) -> None:
        item = ItemBuilder().with_name("Test Item").and_price(10).and_units(3).build()
        self.cashier.open_receipt()
        self.cashier.add_item_to_receipt(item)
        self.cashier.close_receipt(PayWithCash())
        self.assertEqual(self.cashier.revenue_report["Cash"], item.total_price())

    def test_generate_x_report(self) -> None:
        with patch("typer.prompt") as mock_prompt:
            mock_prompt.side_effect = ["y"]
            self.cashier.sales_report = {"Item 1": 5, "Item 2": 10}
            self.cashier.revenue_report = {"Cash": 100.0, "Card": 150.0}
            self.assertIsNotNone(self.cashier.generate_x_report())

    def test_generate_z_report(self) -> None:
        with patch("typer.prompt") as mock_prompt:
            mock_prompt.side_effect = ["y"]
            self.cashier.sales_report = {"Item 1": 5, "Item 2": 10}
            self.cashier.revenue_report = {"Cash": 100.0, "Card": 150.0}
            assert self.cashier.sales_report == {"Item 1": 5, "Item 2": 10}
            assert self.cashier.revenue_report == {"Cash": 100.0, "Card": 150.0}

            count = self.cashier.generate_z_report(0)
            self.assertEqual(count, 1)

            assert self.cashier.sales_report == {}
            assert self.cashier.revenue_report == {}


if __name__ == "__main__":
    unittest.main()
