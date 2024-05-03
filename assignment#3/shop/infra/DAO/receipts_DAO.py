import os
import sqlite3
from uuid import UUID

from shop.core.errors import ClosedError, DoesNotExistError
from shop.core.products import Product
from shop.core.receipt_product import ReceiptProduct
from shop.core.receipts import Receipt


class ReceiptDAO:
    def __init__(
        self,
        db_file: str = os.path.abspath("../identifier.sqlite"),
    ):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()

    def create(self, receipt: Receipt) -> None:
        self.cursor.execute(
            "INSERT INTO receipts (id, status, total) VALUES (?, ?, ?)",
            (str(receipt.id), receipt.status, receipt.total),
        )
        self.conn.commit()

    def add_product(
        self, receipt: Receipt, product: Product, product_quantity: int
    ) -> None:
        receipt_product = ReceiptProduct(
            product_quantity, product.price, product_quantity * product.price
        )
        try:
            self.cursor.execute(
                """
                INSERT INTO receipt_products (
                    receipt_id,
                    product_id,
                    quantity,
                    price,
                    total
                )
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    str(receipt.id),
                    str(product.id),
                    receipt_product.quantity,
                    receipt_product.price,
                    receipt_product.total,
                ),
            )

            receipt.total += receipt_product.total
            self.cursor.execute(
                "UPDATE receipts SET total = ? WHERE id = ?",
                (receipt.total, str(receipt.id)),
            )

            self.conn.commit()
        except Exception:
            raise DoesNotExistError(receipt.id)

    def read(self, receipt_id: UUID) -> Receipt:
        self.cursor.execute("SELECT * FROM receipts WHERE id = ?", (str(receipt_id),))
        receipt_data = self.cursor.fetchone()
        if receipt_data:
            self.cursor.execute(
                "SELECT * FROM receipt_products WHERE receipt_id = ?",
                (str(receipt_id),),
            )
            receipt_products_data = self.cursor.fetchall()
            receipt_products = []
            for receipt_product_data in receipt_products_data:
                receipt_products.append(
                    ReceiptProduct(
                        receipt_product_data[2],
                        receipt_product_data[3],
                        receipt_product_data[4],
                    )
                )
            return Receipt(
                id=UUID(receipt_data[0]),
                products=receipt_products,
                status=receipt_data[1],
                total=receipt_data[2],
            )
        else:
            raise DoesNotExistError(receipt_id)

    def close(self, receipt_id: UUID, receipt_status: str) -> None:
        self.cursor.execute("SELECT * FROM receipts WHERE id = ?", (str(receipt_id),))
        receipt = self.cursor.fetchone()
        if receipt is None:
            raise DoesNotExistError(receipt_id)
        else:
            # sales_dao = SalesDAO()
            # sales_dao.update(Sales(n_receipts=1, revenue=receipt[2]))
            self.cursor.execute(
                "UPDATE receipts SET status = ? WHERE id = ?",
                (receipt_status, str(receipt_id)),
            )
            self.conn.commit()

    def delete(self, receipt_id: UUID) -> None:
        self.cursor.execute(
            "SELECT status FROM receipts WHERE id = ?", (str(receipt_id),)
        )
        receipt_status = self.cursor.fetchone()

        if receipt_status is None:
            raise DoesNotExistError(receipt_id)
        elif receipt_status[0] == "closed":
            raise ClosedError(receipt_id)
        else:
            self.cursor.execute("DELETE FROM receipts WHERE id = ?", (str(receipt_id),))
            self.conn.commit()

    def __del__(self) -> None:
        self.conn.close()
