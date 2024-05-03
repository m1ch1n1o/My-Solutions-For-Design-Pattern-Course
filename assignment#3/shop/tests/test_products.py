from dataclasses import dataclass, field
from typing import Any
from unittest.mock import ANY
from uuid import uuid4

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from shop.runner.setup import init_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(init_app())


@dataclass
class Fake:
    faker: Faker = field(default_factory=Faker)

    def unit(self) -> dict[str, Any]:
        return {
            "name": self.faker.word(),
        }

    def product(self, unit_id: str) -> dict[str, Any]:
        return {
            "unit_id": unit_id,
            "name": self.faker.word(),
            "barcode": self.faker.word(),
            "price": self.faker.pyfloat(),
        }


def test_should_not_read_unknown_product(client: TestClient) -> None:
    unknown_id = uuid4()

    response = client.get(f"/products/{unknown_id}")

    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Product with id<{unknown_id}> does not exist."}
    }


def test_should_create_product(client: TestClient) -> None:
    fake = Fake()
    unit_data = fake.unit()
    unit_id = client.post("/units", json=unit_data).json()["unit"]["id"]

    product_data = fake.product(unit_id)

    response = client.post("/products", json=product_data)

    assert response.status_code == 201
    assert response.json() == {"product": {"id": ANY, **product_data}}


def test_should_persist_product(client: TestClient) -> None:
    fake = Fake()
    unit_data = fake.unit()
    unit_id = client.post("/units", json=unit_data).json()["unit"]["id"]

    product_data = fake.product(unit_id)

    response = client.post("/products", json=product_data)
    product_id = response.json()["product"]["id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json() == {"id": product_id, **product_data}


def test_get_all_products_on_empty(client: TestClient) -> None:
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == {"products": []}


def test_get_all_products(client: TestClient) -> None:
    fake = Fake()
    unit_data = fake.unit()
    unit_id = client.post("/units", json=unit_data).json()["unit"]["id"]

    product_data = fake.product(unit_id)

    response = client.post("/products", json=product_data)
    product_id = response.json()["product"]["id"]

    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == {"products": [{"id": product_id, **product_data}]}


def test_should_not_create_duplicate_product(client: TestClient) -> None:
    fake = Fake()
    unit_data = fake.unit()
    unit_id = client.post("/units", json=unit_data).json()["unit"]["id"]

    product_data = {
        "unit_id": unit_id,
        "name": "TestProduct",
        "barcode": "TestBarcode",
        "price": 10.0,
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 201

    response_duplicate = client.post("/products", json=product_data)

    assert response_duplicate.status_code == 409

    expected_error = f"Product with barcode<{product_data['barcode']}> already exists."
    assert response_duplicate.json() == {"error": {"message": expected_error}}


def test_should_not_update_unknown_product(client: TestClient) -> None:
    unknown_id = uuid4()
    update_data = {"price": 15.0}  # Update information for the product

    response = client.patch(f"/products/{unknown_id}", json=update_data)

    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Product with id<{unknown_id}> does not exist."}
    }


def test_should_update_product_price(client: TestClient) -> None:
    fake = Fake()
    unit_data = fake.unit()
    unit_id = client.post("/units", json=unit_data).json()["unit"]["id"]

    product_data = fake.product(unit_id)

    response = client.post("/products", json=product_data)
    product_id = response.json()["product"]["id"]

    new_price = 20.0
    update_data = {"price": new_price}
    response = client.patch(f"/products/{product_id}", json=update_data)

    assert response.status_code == 200

    updated_product = client.get(f"/products/{product_id}").json()
    assert updated_product["price"] == new_price


def test_should_not_create_product_with_nonexistent_unit(client: TestClient) -> None:
    fake = Fake()
    unit_id = str(uuid4())  # Creating a random non-existing unit ID

    product_data = fake.product(unit_id)

    response = client.post("/products", json=product_data)

    assert response.status_code == 404
    assert response.json() == {
        "error": {"message": f"Unit with id<{unit_id}> does not exist."}
    }
