from DAO_files.items_DAO import InMemoryItemDatabase
from models.item import Item


def test_insert_item() -> None:
    in_memory_db = InMemoryItemDatabase()
    item = Item("Test", 10, 3)
    in_memory_db.insert_item(item)
    items = in_memory_db.get_items()
    assert [item] == items


def test_get_items() -> None:
    in_memory_db = InMemoryItemDatabase()
    dummy_items = [
        Item("Dummy1", 15.0, 4, "Discount", 5, 10),
        Item("Dummy2", 20.0, 2),
    ]
    for item_data in dummy_items:
        in_memory_db.insert_item(item_data)

    items = in_memory_db.get_items()
    assert dummy_items == items
