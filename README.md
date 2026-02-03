# PyQt6 Magic Shop

A clean PyQt6 desktop app that simulates a small inventory system for a fantasy artifact shop.
The focus is professional: SQLite persistence, tested service layer, and a simple UI that an
employer can run immediately.

![UI](docs/images/ui_overview.png)

## Features
- PyQt6 desktop UI (table + dialogs + actions)
- SQLite persistence with automatic schema creation
- Service layer with business rules (buy/restock/price adjustments)
- Unit tests for database + service logic
- Clean structure: `src/`, `tests/`, `data/`, `docs/`

## Quick Start
```bash
python -m venv .venv
.venv\Scripts\python -m pip install -U pip
.venv\Scripts\python -m pip install -e .[dev]
.venv\Scripts\python -m magic_shop
```

## Tests
```bash
.venv\Scripts\python -m pytest
```

## Data
The first launch initializes the database and loads seed data from `data/seed.json`.

## Design Decisions
See `docs/DECISIONS.md`.

## Hiring Checklist
- Clean architecture: UI, services, repositories
- SQLite persistence with schema
- Business rules covered by tests
- Reproducible data seeding

## Data
- \\data/magic_shop.db\\ is created at runtime and is not tracked.
- \\data/seed.json\\ contains synthetic seed items used on first launch.

