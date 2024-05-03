import os
import sqlite3
from typing import List
from uuid import UUID

from shop.core.errors import DoesNotExistError, ExistsError
from shop.core.products import Product


class ProductDAO:
    def __init__(
        self,
        db_file: str = os.path.abspath("../identifier.sqlite"),
    ):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()
        # with open(os.path.abspath("../databases.sql"), 'r') as sql_file:
        #     self.conn.executescript(sql_file.read())

    def create(self, product: Product) -> None:
        try:
            self.cursor.execute(
                "INSERT INTO products ("
                "id, "
                "unit_id,"
                "barcode,"
                "name,"
                "price"
                ")"
                " VALUES (?, ?, ?, ?, ?)",
                (
                    str(product.id),
                    str(product.unit_id),
                    product.barcode,
                    product.name,
                    product.price,
                ),
            )
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            self.conn.commit()
            if "FOREIGN KEY constraint failed" in str(e):
                raise DoesNotExistError(product.unit_id)
            else:
                raise ExistsError(product.barcode)

    def update_price(self, product_id: UUID, new_price: float) -> None:
        self.cursor.execute(
            "UPDATE products SET price = ? WHERE id = ?", (new_price, str(product_id))
        )
        self.conn.commit()

    def read(self, product_id: UUID) -> Product:
        self.cursor.execute(
            "SELECT id, unit_id, barcode, name, price FROM products WHERE id = ?",
            (str(product_id),),
        )
        row = self.cursor.fetchone()
        if row:
            product_id, unit_id, barcode, name, price = row
            return Product(
                id=product_id, unit_id=unit_id, barcode=barcode, name=name, price=price
            )
        else:
            raise DoesNotExistError(product_id)

    def read_all(self) -> List[Product]:
        self.cursor.execute("SELECT id, unit_id, barcode, name, price FROM products")
        rows = self.cursor.fetchall()
        products = []
        for row in rows:
            product_id, unit_id, barcode, name, price = row
            products.append(
                Product(
                    id=product_id,
                    unit_id=unit_id,
                    barcode=barcode,
                    name=name,
                    price=price,
                )
            )
        return products

    def __del__(self) -> None:
        self.conn.close()
