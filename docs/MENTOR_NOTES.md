# Mentor Notes

## Why this project exists
I wanted a realistic desktop app that proves architecture discipline beyond CRUD: service layer, repository layer, tests, and UI iteration.

## Technical decisions
- Chose layered architecture to separate UI from business and storage logic.
- Kept SQLite for offline reliability and reproducible local setup.
- Added Arcade Mode in v1.1 to show event-driven UI design and product iteration.

## Build vs polish
- Build phase: CRUD flows, validation rules, persistence, tests, CI.
- Polish phase: better action feedback, screenshot refresh, release notes quality.

## What I learned
- UX feedback (selection, errors, confirmations) is critical for perceived quality.
- Small interactive features can showcase engineering maturity when they stay testable.
