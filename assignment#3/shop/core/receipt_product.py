from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class ReceiptProduct:
    quantity: int
    price: float
    total: float

    id: UUID = field(default_factory=uuid4)
