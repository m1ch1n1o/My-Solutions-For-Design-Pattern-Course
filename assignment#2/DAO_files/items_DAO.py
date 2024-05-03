import sqlite3
from typing import Protocol

from models.item import ItemBuilder, ItemInterface


class ItemDatabaseProtocol(Protocol):
    def insert_item(self, item: ItemInterface) -> None:
        pass

    def get_items(self) -> list[ItemInterface]:
        pass

    def close_connection(self) -> None:
        pass


class ItemDatabase(ItemDatabaseProtocol):
    def __init__(self) -> None:
        self.conn = sqlite3.connect("identifier.sqlite")
        self.cur = self.conn.cursor()

    def insert_item(self, item: ItemInterface) -> None:
        item_data = item.item_data()
        select_command = """
            SELECT id FROM items WHERE name = ? AND pack_size = ?
        """

        self.cur.execute(select_command, (item_data[0], item_data[2]))
        existing_item = self.cur.fetchone()

        if not existing_item:
            # Item does not exist, perform the insert
            sql_command = (
                "INSERT INTO items "
                "(name, "
                "price, "
                "pack_size, "
                "discount_strategy, "
                "discount_amount, d"
                "iscount_pack) VALUES (?, ?, ?, ?, ?, ?)"
            )

            self.cur.execute(sql_command, item_data)
            self.conn.commit()

    def get_items(self) -> list[ItemInterface]:
        items = []

        try:
            self.cur.execute("SELECT * FROM items")
            rows = self.cur.fetchall()

            for row in rows:
                (
                    item_id,
                    name,
                    price,
                    pack_size,
                    discount_strategy,
                    discount_amount,
                    discount_pack,
                ) = row
                item = (
                    ItemBuilder()
                    .with_name(name)
                    .and_price(price)
                    .and_pack_size(pack_size)
                    .and_discount(discount_strategy)
                    .and_discount_amount(discount_amount)
                    .and_pack_discount(discount_pack)
                    .build()
                )
                items.append(item)

        except sqlite3.Error as e:
            print(f"Error retrieving items: {e}")

        return items

    def close_connection(self) -> None:
        self.conn.close()


class InMemoryItemDatabase(ItemDatabaseProtocol):
    def __init__(self) -> None:
        self.item_data_list: list[ItemInterface] = []  # Initialize as an empty list

    def insert_item(self, item: ItemInterface) -> None:
        self.item_data_list.append(item)

    def get_items(self) -> list[ItemInterface]:
        return self.item_data_list

    def close_connection(self) -> None:
        pass
