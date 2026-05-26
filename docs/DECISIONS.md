# Design Decisions

- UI and logic are separated into `ui/`, `services.py`, and `repositories.py`.
- SQLite is used with an explicit schema and simple repository layer to keep code testable.
- Business rules live in the service layer for easy unit testing.
- The UI is intentionally simple but responsive and production-like.
