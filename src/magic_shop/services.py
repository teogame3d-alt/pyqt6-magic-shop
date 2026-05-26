from __future__ import annotations

"""RO: Logica de business a magazinului (validari + reguli).
EN: Shop business logic (validation + rules).
"""

from dataclasses import replace

from .models import Artifact
from .repositories import ArtifactRepository


class ShopService:
    """RO: Serviciu care orchestreaza operatiile de inventar.
    EN: Service that orchestrates inventory operations.
    """
    def __init__(self, repo: ArtifactRepository) -> None:
        self.repo = repo

    def list_inventory(self) -> list[Artifact]:
        """RO: Lista completa a inventarului.
        EN: Full inventory list.
        """
        return self.repo.list_all()

    def add_artifact(self, name: str, rarity: str, price: int, stock: int) -> Artifact:
        """RO: Valideaza si adauga un artefact nou.
        EN: Validate and add a new artifact.
        """
        if price <= 0 or stock < 0:
            raise ValueError("Invalid price or stock")
        return self.repo.add(Artifact(None, name.strip(), rarity.strip(), price, stock))

    def update_artifact(self, artifact_id: int, name: str, rarity: str, price: int, stock: int) -> None:
        """RO: Valideaza si actualizeaza un artefact.
        EN: Validate and update an artifact.
        """
        if price <= 0 or stock < 0:
            raise ValueError("Invalid price or stock")
        self.repo.update(Artifact(artifact_id, name.strip(), rarity.strip(), price, stock))

    def delete_artifact(self, artifact_id: int) -> None:
        """RO: Sterge un artefact.
        EN: Delete an artifact.
        """
        self.repo.delete(artifact_id)

    def buy(self, artifact_id: int, qty: int) -> None:
        """RO: Cumparare cu verificare de stoc.
        EN: Purchase with stock checks.
        """
        items = {a.id: a for a in self.repo.list_all()}
        art = items.get(artifact_id)
        if art is None:
            raise ValueError("Artifact not found")
        if qty <= 0:
            raise ValueError("Invalid quantity")
        if art.stock < qty:
            raise ValueError("Not enough stock")
        self.repo.set_stock(artifact_id, art.stock - qty)

    def restock(self, artifact_id: int, qty: int) -> None:
        """RO: Reaprovizionare cu validare.
        EN: Restock with validation.
        """
        items = {a.id: a for a in self.repo.list_all()}
        art = items.get(artifact_id)
        if art is None:
            raise ValueError("Artifact not found")
        if qty <= 0:
            raise ValueError("Invalid quantity")
        self.repo.set_stock(artifact_id, art.stock + qty)

    def adjust_price(self, artifact_id: int, delta: int) -> None:
        """RO: Ajusteaza pretul (fara a cobori sub 1).
        EN: Adjust price (never below 1).
        """
        items = {a.id: a for a in self.repo.list_all()}
        art = items.get(artifact_id)
        if art is None:
            raise ValueError("Artifact not found")
        new_price = max(1, art.price + delta)
        self.repo.update(replace(art, price=new_price))
