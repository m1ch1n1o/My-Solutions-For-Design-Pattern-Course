from typing import Any
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from shop.runner.setup import init_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(init_app())


def receipt(status: str = "open", total: float = 0) -> dict[str, Any]:
    return {"status": status, "products": [], "total": total}


def test_should_not_read_unknown(client: TestClient) -> None:
    unknown_id = uuid4()

    response = client.get(f"/receipts/{unknown_id}")

    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Receipt with id<{unknown_id}> does not exist."}
    }


def test_should_create(client: TestClient) -> None:
    receipt_data = receipt()

    response = client.post("/receipts", json=receipt_data)

    assert response.status_code == 201
    assert "receipt" in response.json()
    assert "id" in response.json()["receipt"]


def test_should_persist(client: TestClient) -> None:
    receipt_data = receipt()

    response = client.post("/receipts", json=receipt_data)
    receipt_id = response.json()["receipt"]["id"]

    response = client.get(f"/receipts/{receipt_id}")

    assert response.status_code == 200
    assert response.json()["receipt"]["id"] == receipt_id
    assert response.json()["receipt"]["status"] == "open"
    assert response.json()["receipt"]["total"] == 0
    assert response.json()["receipt"]["products"] == []


def test_should_delete(client: TestClient) -> None:
    receipt_data = receipt()

    response = client.post("/receipts", json=receipt_data)
    receipt_id = response.json()["receipt"]["id"]

    response = client.delete(f"/receipts/{receipt_id}")

    assert response.status_code == 200
    assert response.json() == {}


def test_should_not_delete_closed(client: TestClient) -> None:
    receipt_data = receipt()

    response = client.post("/receipts", json=receipt_data)
    receipt_id = response.json()["receipt"]["id"]
    close_payload = {"status": "closed"}
    client.patch(f"/receipts/{receipt_id}", json=close_payload)
    response = client.delete(f"/receipts/{receipt_id}")

    assert response.status_code == 403
    assert response.json() == {
        "error": {"message": f"Receipt with id<{receipt_id}> is closed."}
    }


def test_should_not_delete_unknown(client: TestClient) -> None:
    unknown_id = uuid4()

    response = client.delete(f"/receipts/{unknown_id}")

    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Receipt with id<{unknown_id}> does not exist."}
    }


def test_should_close(client: TestClient) -> None:
    receipt_data = receipt()

    response = client.post("/receipts", json=receipt_data)
    receipt_id = response.json()["receipt"]["id"]

    close_payload = {"status": "closed"}
    response = client.patch(f"/receipts/{receipt_id}", json=close_payload)

    assert response.status_code == 200
    assert response.json() == {}


def test_should_not_close(client: TestClient) -> None:
    close_payload = {"status": "closed"}
    random_id = uuid4()
    response = client.patch(f"/receipts/{random_id}", json=close_payload)

    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Receipt with id<{random_id}> does not exist."}
    }


def test_add_product_to_receipt_with_unit_id(client: TestClient) -> None:
    unit_data = {"name": "TestUnit"}
    response_unit = client.post("/units", json=unit_data)
    unit_id = response_unit.json()["unit"]["id"]

    product_data = {
        "unit_id": unit_id,
        "name": "TestProduct",
        "barcode": "TestBarcode",
        "price": 10.0,
    }
    response_product = client.post("/products", json=product_data)
    product_id = response_product.json()["product"]["id"]

    response_receipt = client.post("/receipts")
    receipt_id = response_receipt.json()["receipt"]["id"]

    add_product_data = {"id": product_id, "quantity": 2}
    response_add_product = client.post(
        f"/receipts/{receipt_id}/products", json=add_product_data
    )

    assert response_add_product.status_code == 200


def uuid_to_str(data: dict[str, Any]) -> Any:
    for key, value in data.items():
        if isinstance(value, UUID):
            data[key] = str(value)
    return data


def test_add_non_existing_product_to_receipt(client: TestClient) -> None:
    response_receipt = client.post("/receipts")
    receipt_id = response_receipt.json()["receipt"]["id"]

    non_existing_product_id = uuid4()
    add_product_data = {"id": non_existing_product_id, "quantity": 2}
    serialized_data = uuid_to_str(add_product_data)
    response_add_product = client.post(
        f"/receipts/{receipt_id}/products", json=serialized_data
    )

    assert response_add_product.status_code == 404

    assert response_add_product.json() == {
        "error": {
            "message": f"Product with id<{non_existing_product_id}> does not exist."
        }
    }


def test_add_product_to_unknown_receipt(client: TestClient) -> None:
    # Create a unit
    unit_data = {"name": "TestUnit"}
    response_unit = client.post("/units", json=unit_data)
    assert response_unit.status_code == 201
    unit_id = response_unit.json()["unit"]["id"]

    # Create a product associated with the unit
    product_data = {
        "unit_id": unit_id,
        "name": "TestProduct",
        "barcode": "TestBarcode",
        "price": 10.0,
    }
    response_product = client.post("/products", json=product_data)
    assert response_product.status_code == 201

    # Try to add the product to an unknown receipt
    unknown_receipt_id = uuid4()
    product_to_add = {"id": response_product.json()["product"]["id"], "quantity": 5}

    response_add_product = client.post(
        f"/receipts/{unknown_receipt_id}/products", json=product_to_add
    )

    assert response_add_product.status_code == 404
    assert response_add_product.json() == {
        "error": {"message": f"Receipt with id<{unknown_receipt_id}> does not exist."}
    }
