import unittest

from models.item import BatchItem, Item
from models.receipt import Receipt


class TestReceiptAndDiscounts(unittest.TestCase):
    def setUp(self) -> None:
        self.item1 = Item(name="Milk", price_per_unit=5.00, units=3)
        self.item2 = Item(
            name="Milk",
            price_per_unit=5.00,
            units=3,
            discount_strategy="ItemDiscount",
            discount_amount=10,
        )
        self.item3 = Item(
            name="Milk", price_per_unit=100.00, units=1, discount_strategy="NoDiscount"
        )
        self.item4 = Item(name="Water", price_per_unit=1.00, units=5)
        self.batch_item1 = BatchItem(
            name="Mineral Water",
            price_per_unit=10.00,
            units=5,
            pack_size=6,
            discount_strategy="BatchDiscount",
            discount_amount=10,
            discount_pack=6,
        )
        self.batch_item2 = BatchItem(
            name="Mineral Water",
            price_per_unit=10.00,
            units=5,
            pack_size=6,
            discount_strategy="BatchDiscount",
            discount_amount=10,
            discount_pack=5,
        )

    def test_receipt_initial_customer_id(self) -> None:
        Receipt._set_customer_id(0)
        assert Receipt.customer_id == 0
        Receipt()
        assert Receipt.customer_id == 1

    def test_receipt_add_item(self) -> None:
        Receipt._set_customer_id(0)
        receipt = Receipt()
        receipt.add_item(self.item1)
        assert len(receipt.items) == 1
        assert receipt.items[0] == self.item1

    def test_calculate_total(self) -> None:
        Receipt._set_customer_id(0)
        receipt = Receipt()
        receipt.add_item(self.item1)
        receipt.add_item(self.item4)
        expected_total = self.item1.total_price() + self.item4.total_price()
        assert receipt.calculate_total() == expected_total

    def test_no_discount(self) -> None:
        Receipt._set_customer_id(0)  # it is needed so prime discount does not apply
        receipt = Receipt()
        receipt.add_item(self.item1)
        assert receipt.calculate_total() == 15

    def test_item_discount(self) -> None:
        Receipt._set_customer_id(0)
        receipt = Receipt()
        receipt.add_item(self.item2)
        assert receipt.calculate_total() == 13.5

    def test_batch_discount_matching_pack_size(self) -> None:
        Receipt._set_customer_id(0)
        receipt = Receipt()
        receipt.add_item(self.batch_item1)
        assert receipt.calculate_total() == 45

    def test_batch_discount_non_matching_pack_size(self) -> None:
        Receipt._set_customer_id(0)
        receipt = Receipt()
        receipt.add_item(self.batch_item2)
        assert receipt.calculate_total() == 50

    def test_customer_number_discount_prime(self) -> None:
        receipt = Receipt()
        Receipt._set_customer_id(2)
        receipt.add_item(self.item3)
        assert receipt.calculate_total() == 83

    def test_customer_number_discount_non_prime(self) -> None:
        receipt = Receipt()
        Receipt._set_customer_id(4)
        receipt.add_item(self.item3)
        assert receipt.calculate_total() == 100


if __name__ == "__main__":
    unittest.main()
