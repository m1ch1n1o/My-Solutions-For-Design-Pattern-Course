from DAO_files.items_DAO import InMemoryItemDatabase
from models.item import ItemBuilder


def test_init() -> None:
    in_memory_db = InMemoryItemDatabase()
    assert in_memory_db.get_items() == []


def test_update() -> None:
    in_memory_db = InMemoryItemDatabase()
    item = ItemBuilder().with_name("TestItem").and_price(10.0).and_pack_size(3).build()
    in_memory_db.insert_item(item)

    items = in_memory_db.get_items()
    assert len(items) == 1
    assert items[0].name == "TestItem"
    assert items[0].price_per_unit == 10.0
    assert items[0].pack_size == 3
