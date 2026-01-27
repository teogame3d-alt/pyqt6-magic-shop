from __future__ import annotations

import json
import sqlite3
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS artifacts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  rarity TEXT NOT NULL,
  price INTEGER NOT NULL,
  stock INTEGER NOT NULL
);
"""


def get_connection(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path, seed_path: Path | None = None) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
        if seed_path and seed_path.exists():
            seed_data = json.loads(seed_path.read_text(encoding="utf-8"))
            for row in seed_data:
                conn.execute(
                    "INSERT OR IGNORE INTO artifacts(name, rarity, price, stock) VALUES(?,?,?,?)",
                    (row["name"], row["rarity"], row["price"], row["stock"]),
                )
            conn.commit()
