from __future__ import annotations

from pathlib import Path

from PyQt6.QtWidgets import QApplication

from .db import init_db
from .repositories import ArtifactRepository
from .services import ShopService
from .ui.main_window import MainWindow


def main() -> None:
    base_dir = Path(__file__).resolve().parents[2]
    db_path = base_dir / "data" / "magic_shop.db"
    seed_path = base_dir / "data" / "seed.json"
    init_db(db_path, seed_path)

    app = QApplication([])
    service = ShopService(ArtifactRepository(db_path))
    win = MainWindow(service)
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
