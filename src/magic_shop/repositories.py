from __future__ import annotations

"""RO: Acces la date prin repository pattern.
EN: Data access via repository pattern.
"""

from pathlib import Path
from typing import Iterable

from .db import get_connection
from .models import Artifact


class ArtifactRepository:
    """RO: CRUD pentru artefacte in SQLite.
    EN: CRUD for artifacts in SQLite.
    """
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def list_all(self) -> list[Artifact]:
        """RO: Listeaza tot inventarul ordonat.
        EN: List all inventory items ordered by name.
        """
        with get_connection(self.db_path) as conn:
            rows = conn.execute("SELECT * FROM artifacts ORDER BY name").fetchall()
        return [Artifact(**dict(row)) for row in rows]

    def add(self, artifact: Artifact) -> Artifact:
        """RO: Adauga un artefact si returneaza varianta cu id.
        EN: Add an artifact and return it with id.
        """
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                "INSERT INTO artifacts(name, rarity, price, stock) VALUES(?,?,?,?)",
                (artifact.name, artifact.rarity, artifact.price, artifact.stock),
            )
            conn.commit()
            return Artifact(cur.lastrowid, artifact.name, artifact.rarity, artifact.price, artifact.stock)

    def update(self, artifact: Artifact) -> None:
        """RO: Actualizeaza un artefact existent.
        EN: Update an existing artifact.
        """
        if artifact.id is None:
            raise ValueError("Artifact must have id for update")
        with get_connection(self.db_path) as conn:
            conn.execute(
                "UPDATE artifacts SET name=?, rarity=?, price=?, stock=? WHERE id=?",
                (artifact.name, artifact.rarity, artifact.price, artifact.stock, artifact.id),
            )
            conn.commit()

    def delete(self, artifact_id: int) -> None:
        """RO: Sterge un artefact dupa id.
        EN: Delete an artifact by id.
        """
        with get_connection(self.db_path) as conn:
            conn.execute("DELETE FROM artifacts WHERE id=?", (artifact_id,))
            conn.commit()

    def set_stock(self, artifact_id: int, new_stock: int) -> None:
        """RO: Seteaza stocul direct (folosit de servicii).
        EN: Set stock directly (used by services).
        """
        with get_connection(self.db_path) as conn:
            conn.execute("UPDATE artifacts SET stock=? WHERE id=?", (new_stock, artifact_id))
            conn.commit()

    def by_name(self, name: str) -> Artifact | None:
        """RO: Cauta un artefact dupa nume.
        EN: Find an artifact by name.
        """
        with get_connection(self.db_path) as conn:
            row = conn.execute("SELECT * FROM artifacts WHERE name=?", (name,)).fetchone()
        if row:
            return Artifact(**dict(row))
        return None

    def bulk_add(self, artifacts: Iterable[Artifact]) -> None:
        """RO: Inserare bulk, ignorand duplicatele.
        EN: Bulk insert, ignoring duplicates.
        """
        with get_connection(self.db_path) as conn:
            conn.executemany(
                "INSERT OR IGNORE INTO artifacts(name, rarity, price, stock) VALUES(?,?,?,?)",
                [(a.name, a.rarity, a.price, a.stock) for a in artifacts],
            )
            conn.commit()
