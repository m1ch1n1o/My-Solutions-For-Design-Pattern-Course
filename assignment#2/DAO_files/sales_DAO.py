import sqlite3
from typing import Protocol


class SalesDatabaseProtocol(Protocol):
    def insert_sales_record(self, name: str, sales: int) -> None:
        pass

    def get_sales_record(self) -> dict[str, int]:
        pass

    def close_connection(self) -> None:
        pass


class SalesDatabase(SalesDatabaseProtocol):
    def __init__(self) -> None:
        self.conn = sqlite3.connect("identifier.sqlite")
        self.cur = self.conn.cursor()

    def insert_sales_record(self, name: str, sales: int) -> None:
        sql = "INSERT INTO sales_report (name, sales) VALUES (?, ?)"
        self.cur.execute(sql, (name, sales))
        self.conn.commit()

    def get_sales_record(self) -> dict[str, int]:
        sales_report = {}
        try:
            sql = "SELECT name, sales FROM sales_report"
            self.cur.execute(sql)
            rows = self.cur.fetchall()

            for row in rows:
                name, sales = row
                sales_report[name] = sales

            return sales_report
        except Exception as e:
            print(f"Error occurred while fetching sales report: {str(e)}")
            return sales_report

    def close_connection(self) -> None:
        self.conn.close()


class InMemorySalesDatabase(SalesDatabaseProtocol):
    def __init__(self) -> None:
        self.sales_data: dict[str, int] = {}

    def insert_sales_record(self, name: str, sales: int) -> None:
        if name in self.sales_data:
            self.sales_data[name] += sales  # Increment sales count if product exists
        else:
            self.sales_data[name] = sales

    def get_sales_record(self) -> dict[str, int]:
        return self.sales_data.copy()
