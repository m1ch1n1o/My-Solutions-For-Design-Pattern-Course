import typer

from DAO_files.items_DAO import ItemDatabase
from DAO_files.revenue_DAO import RevenueDatabase
from DAO_files.sales_DAO import SalesDatabase
from models.products import PRODUCT_1, PRODUCT_2, PRODUCT_3, PRODUCT_4, PRODUCT_5
from models.store import Store

app = typer.Typer()

items_db = ItemDatabase()

items_db.insert_item(PRODUCT_1)
items_db.insert_item(PRODUCT_2)
items_db.insert_item(PRODUCT_3)
items_db.insert_item(PRODUCT_4)
items_db.insert_item(PRODUCT_5)

sales_db = SalesDatabase()
revenue_db = RevenueDatabase()

common_store = Store(items_db, sales_db, revenue_db)


@app.command()
def list() -> None:
    common_store.generate_list()


@app.command()
def simulate() -> None:
    common_store.simulate()


@app.command()
def report() -> None:
    common_store.generate_report()


if __name__ == "__main__":
    app()
