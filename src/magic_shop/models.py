from __future__ import annotations

"""RO: Modele de baza pentru domeniul Magic Shop.
EN: Core domain models for Magic Shop.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Artifact:
    """RO: Model pentru un artefact de inventar.
    EN: Inventory artifact model.
    """
    id: int | None
    name: str
    rarity: str
    price: int
    stock: int
