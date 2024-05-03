import sqlite3
from typing import Protocol


class RevenueDatabaseProtocol(Protocol):
    def update_revenue_report(self, payment_type: str, revenue: float) -> None:
        pass

    def get_revenue_record(self) -> dict[str, float]:
        pass

    def close_connection(self) -> None:
        pass


class RevenueDatabase(RevenueDatabaseProtocol):
    def __init__(self) -> None:
        self.conn = sqlite3.connect("identifier.sqlite")
        self.cur = self.conn.cursor()
        self.conn.commit()

    def update_revenue_report(self, payment_type: str, revenue: float) -> None:
        self.cur.execute(
            "SELECT * FROM revenue_report " "WHERE payment_type = ?", (payment_type,)
        )
        row = self.cur.fetchone()

        if row is None:
            self.cur.execute(
                "INSERT INTO revenue_report (payment_type, revenue) " "VALUES (?, ?)",
                (payment_type, revenue),
            )
        else:
            self.cur.execute(
                "UPDATE revenue_report SET revenue = revenue + ? "
                "WHERE payment_type = ?",
                (revenue, payment_type),
            )

        self.conn.commit()

    def get_revenue_record(self) -> dict[str, float]:
        self.cur.execute("SELECT * FROM revenue_report")
        rows = self.cur.fetchall()

        revenue_record = {}
        for row in rows:
            payment_type, revenue = row
            revenue_record[payment_type] = revenue

        return revenue_record

    def close_connection(self) -> None:
        self.conn.close()


class InMemoryRevenueDatabase(RevenueDatabaseProtocol):
    def __init__(self) -> None:
        self.revenue_data = {"Cash": 0.0, "Card": 0.0}

    def update_revenue_report(self, payment_type: str, revenue: float) -> None:
        if payment_type in self.revenue_data:
            self.revenue_data[payment_type] += revenue

    def get_revenue_record(self) -> dict[str, float]:
        return self.revenue_data.copy()

    def close_connection(self) -> None:
        pass
