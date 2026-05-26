from __future__ import annotations

"""RO: Entry point pentru aplicatia PyQt6 (usor de rulat in IDE).
EN: Entry point for the PyQt6 app (easy to run from IDE).
"""

from pathlib import Path

from PyQt6.QtWidgets import QApplication

from .db import init_db
from .repositories import ArtifactRepository
from .services import ShopService
from .ui.main_window import MainWindow


def main() -> None:
    """RO: Initializeaza DB, serviciile si porneste UI-ul.
    EN: Initialize DB, services, and launch the UI.
    """
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
