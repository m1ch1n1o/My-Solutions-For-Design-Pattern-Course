from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class SalesRepository(Protocol):
    def read(self) -> Sales:
        pass

    def update(self, sales: Sales) -> None:
        pass


@dataclass
class Sales:
    n_receipts: int = 0
    revenue: float = 0.0
