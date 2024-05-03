from DAO_files.sales_DAO import InMemorySalesDatabase


def test_init() -> None:
    in_memory_db = InMemorySalesDatabase()
    assert in_memory_db.get_sales_record() == {}


def test_update() -> None:
    in_memory_db = InMemorySalesDatabase()
    in_memory_db.insert_sales_record("Laptop", 20)
    assert in_memory_db.get_sales_record() == {"Laptop": 20}
    in_memory_db.insert_sales_record("PC", 10)
    assert in_memory_db.get_sales_record() == {"Laptop": 20, "PC": 10}
