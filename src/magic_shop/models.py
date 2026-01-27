from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Artifact:
    id: int | None
    name: str
    rarity: str
    price: int
    stock: int
