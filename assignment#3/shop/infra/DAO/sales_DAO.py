import os
import sqlite3

from shop.core.sales import Sales


class SalesDAO:
    def __init__(
        self,
        db_file: str = os.path.abspath("../identifier.sqlite"),
    ):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT COUNT(*) FROM sales")
        sales_count = self.cursor.fetchone()[0]

        if sales_count == 0:
            self.cursor.execute(
                "INSERT INTO sales (n_receipts, revenue) VALUES (0, 0.0)"
            )
            self.conn.commit()

    def read(self) -> Sales:
        self.cursor.execute("SELECT * FROM sales")
        sales_data = self.cursor.fetchone()
        return Sales(n_receipts=sales_data[0], revenue=sales_data[1])

    def update(self, sales: Sales) -> None:
        cur_sales = self.read()
        self.cursor.execute(
            "UPDATE sales SET n_receipts = ?, revenue = ?",
            (
                cur_sales.n_receipts + sales.n_receipts,
                cur_sales.revenue + sales.revenue,
            ),
        )
        self.conn.commit()

    def __del__(self) -> None:
        self.conn.close()
