"""Pure game-related helpers for the arcade mode."""

from __future__ import annotations


def reward_from_score(score: int) -> int:
    """Convert arcade score into stock reward units."""
    if score <= 0:
        return 0
    return score // 60
