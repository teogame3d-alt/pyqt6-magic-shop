# PyQt6 Magic Shop

A clean PyQt6 desktop app that simulates a small inventory system for a fantasy artifact shop.
The focus is professional: SQLite persistence, tested service layer, and a simple UI.

[![CI](https://github.com/teogame3d-alt/pyqt6-magic-shop/actions/workflows/ci.yml/badge.svg)](https://github.com/teogame3d-alt/pyqt6-magic-shop/actions/workflows/ci.yml)

![UI](docs/images/ui_overview.png)

## Problem
Small desktop workflows often need reliable, offline CRUD with clear business rules.

## Solution
A PyQt6 UI backed by SQLite with a service layer that enforces business logic and tests.

## Tech
Python, PyQt6, SQLite, pytest, GitHub Actions.

## Impact
- Demonstrates clean architecture (UI, services, repositories)
- Reliable persistence and deterministic business rules
- Tests protect core operations

## Engineering Focus
- Layered design with clear responsibilities
- Offline-first persistence with predictable schema bootstrap
- Service-layer validation covered by automated tests

## Features
- PyQt6 desktop UI (table + dialogs + actions)
- SQLite persistence with automatic schema creation
- Service layer with business rules (buy/restock/price adjustments)
- Arcade mini-game mode integrated in UI (click challenge + score-based rewards)
- Unit tests for database + service logic
- Clean structure: `src/`, `tests/`, `data/`, `docs/`

## Quick Start
```bash
python -m venv .venv
.venv\Scripts\python -m pip install -U pip
.venv\Scripts\python -m pip install -e .[dev]
.venv\Scripts\python -m magic_shop
```

## Demo Flow
1. Launch the app and review the seeded inventory.
2. Execute a buy/restock flow and observe the data update.
3. Open `Arcade` mode, play the challenge, then apply earned reward units to stock.

## Version Notes
- `v1.1.0`: Added integrated arcade challenge in the toolbar and score-to-stock reward flow.

## Tests
```bash
.venv\Scripts\python -m pytest
```

## Design Decisions
See `docs/DECISIONS.md`.

## Data
- `data/magic_shop.db` is created at runtime and is not tracked.
- `data/seed.json` contains synthetic seed items used on first launch.

