from DAO_files.items_DAO import InMemoryItemDatabase
from models.customer import CustomerInterface, PaymentMethod, RandomCustomer
from models.item import Item


def test_init_customer_interface() -> None:
    in_memory_db = InMemoryItemDatabase()
    item = Item("Test", 10, 3)
    in_memory_db.insert_item(item)
    customer = CustomerInterface(in_memory_db)
    assert isinstance(customer.items_db, InMemoryItemDatabase)
    assert customer.items_list == in_memory_db.get_items()


def test_init_random_customer() -> None:
    in_memory_db = InMemoryItemDatabase()
    item = Item("Test", 10, 3)
    in_memory_db.insert_item(item)
    customer = RandomCustomer(in_memory_db)
    assert isinstance(customer.choose_payment_method(), PaymentMethod)


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
