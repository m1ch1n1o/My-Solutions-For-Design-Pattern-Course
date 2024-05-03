from DAO_files.revenue_DAO import InMemoryRevenueDatabase


def test_init() -> None:
    in_memory_db = InMemoryRevenueDatabase()
    assert in_memory_db.get_revenue_record() == {"Cash": 0, "Card": 0}


def test_update() -> None:
    in_memory_db = InMemoryRevenueDatabase()
    in_memory_db.update_revenue_report("Cash", 20)
    assert in_memory_db.get_revenue_record() == {"Cash": 20, "Card": 0}
    in_memory_db.update_revenue_report("Card", 25.33)
    assert in_memory_db.get_revenue_record() == {"Cash": 20, "Card": 25.33}
