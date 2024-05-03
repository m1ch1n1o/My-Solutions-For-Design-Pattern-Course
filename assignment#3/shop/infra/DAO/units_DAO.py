import os
import sqlite3
from typing import List
from uuid import UUID

from shop.core.errors import DoesNotExistError, ExistsError
from shop.core.units import Unit


class UnitDAO:
    def __init__(
        self,
        db_file: str = os.path.abspath("../identifier.sqlite"),
    ):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()

    def create(self, unit: Unit) -> None:
        try:
            self.cursor.execute(
                "INSERT INTO units (id, name) VALUES (?, ?)", (str(unit.id), unit.name)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ExistsError(unit.name)

    def read(self, unit_id: UUID) -> Unit:
        self.cursor.execute("SELECT id, name FROM units WHERE id = ?", (str(unit_id),))
        row = self.cursor.fetchone()
        if row:
            unit_id, name = row
            return Unit(id=unit_id, name=name)
        else:
            raise DoesNotExistError(unit_id)

    def read_all(self) -> List[Unit]:
        self.cursor.execute("SELECT id, name FROM units")
        rows = self.cursor.fetchall()
        units = []
        for row in rows:
            unit_id, name = row
            units.append(Unit(id=unit_id, name=name))
        return units

    def __del__(self) -> None:
        self.conn.close()
