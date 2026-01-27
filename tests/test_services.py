from pathlib import Path

from magic_shop.db import init_db
from magic_shop.repositories import ArtifactRepository
from magic_shop.services import ShopService


def test_buy_and_restock(tmp_path: Path) -> None:
    db = tmp_path / "shop.db"
    init_db(db)
    service = ShopService(ArtifactRepository(db))
    art = service.add_artifact("X", "Rare", 100, 5)
    service.buy(art.id, 2)
    after_buy = service.list_inventory()[0]
    assert after_buy.stock == 3
    service.restock(art.id, 4)
    after_restock = service.list_inventory()[0]
    assert after_restock.stock == 7
