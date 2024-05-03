from typing import Any

from starlette.testclient import TestClient

from shop.core.sales import Sales
from shop.infra.in_memory import SalesInMemory
from shop.runner.setup import init_app


def test_sales_in_memory_update() -> None:
    sales_in_memory = SalesInMemory()
    assert sales_in_memory.read().n_receipts == 0

    sales = Sales(revenue=100.0, n_receipts=1)
    sales_in_memory.update(sales)

    updated_sales = sales_in_memory.read()
    assert updated_sales.revenue == 100.0
    assert updated_sales.n_receipts == 1


def test_sales_in_memory_read() -> None:
    sales_in_memory = SalesInMemory()
    sales = sales_in_memory.read()

    assert sales.revenue == 0.0
    assert sales.n_receipts == 0


def test_sales_in_memory_update_multiple_times() -> None:
    sales_in_memory = SalesInMemory()

    sales_1 = Sales(revenue=100.0, n_receipts=1)
    sales_in_memory.update(sales_1)

    sales_2 = Sales(revenue=50.0, n_receipts=1)
    sales_in_memory.update(sales_2)

    updated_sales = sales_in_memory.read()
    assert updated_sales.revenue == 150.0
    assert updated_sales.n_receipts == 2


client = TestClient(init_app())


def test_sales_update_after_receipt_completion() -> None:
    unit_data = {"name": "TestUnit"}
    response = client.post("/units", json=unit_data)
    assert response.status_code == 201

    unit_id = response.json()["unit"]["id"]
    product_data = {
        "unit_id": unit_id,
        "name": "TestProduct",
        "barcode": "TestBarcode",
        "price": 10.0,
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 201

    product_id = response.json()["product"]["id"]
    add_product_data = {"id": product_id, "quantity": 2}

    receipt_data: dict[Any, Any] = {}
    response = client.post("/receipts", json=receipt_data)
    assert response.status_code == 201

    receipt_id = response.json()["receipt"]["id"]

    response = client.post(f"/receipts/{receipt_id}/products", json=add_product_data)
    assert response.status_code == 200

    close_payload = {"status": "closed"}
    response = client.patch(f"/receipts/{receipt_id}", json=close_payload)
    assert response.status_code == 200

    response = client.get("/sales")
    assert response.status_code == 200

    assert response.json() == {"sales": {"n_receipts": 1, "revenue": 20.0}}
