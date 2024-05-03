from models.item import BatchItem, Item, ItemBuilder


def test_item_total_price() -> None:
    item = Item(name="Test Item", price_per_unit=5.0, units=3)
    assert item.total_price() == 15.0
    assert item.quantity() == 3
    assert item.item_data() == ("Test Item", 5, 1, "NoDiscount", 0, 0)


def test_batch_item_total_price() -> None:
    batch_item = BatchItem(
        name="Test Batch Item", price_per_unit=10.0, units=2, pack_size=5
    )
    assert batch_item.total_price() == 20
    assert batch_item.quantity() == 10
    assert batch_item.item_data() == ("Test Batch Item", 10, 5, "NoDiscount", 0, 0)


def test_item_builder() -> None:
    item_builder = ItemBuilder().with_name("Item").and_price(3).and_units(4).build()
    assert item_builder.total_price() == 12.0
    assert item_builder.quantity() == 4
    assert item_builder.item_data() == ("Item", 3, 1, "NoDiscount", 0, 0)


def test_batch_item_builder() -> None:
    batch_item_builder = (
        ItemBuilder()
        .with_name("Batch Item")
        .and_price(7)
        .and_units(2)
        .and_pack_size(2)
        .build()
    )
    assert batch_item_builder.total_price() == 14
    assert batch_item_builder.quantity() == 4
    assert batch_item_builder.item_data() == ("Batch Item", 7, 2, "NoDiscount", 0, 0)
