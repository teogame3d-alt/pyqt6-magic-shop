from pathlib import Path

from magic_shop.db import init_db
from magic_shop.repositories import ArtifactRepository
from magic_shop.models import Artifact


def test_crud(tmp_path: Path) -> None:
    db = tmp_path / "shop.db"
    init_db(db)
    repo = ArtifactRepository(db)
    art = repo.add(Artifact(None, "Test", "C", 1, 2))
    assert art.id is not None
    fetched = repo.by_name("Test")
    assert fetched is not None
    repo.delete(art.id)
    assert repo.by_name("Test") is None
