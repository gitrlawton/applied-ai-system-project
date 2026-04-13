"""
Ranking Strategies — Music Recommender Simulation
==================================================

Each RankingStrategy holds a complete set of feature weights that controls how
songs are scored.  Swapping the active strategy changes ranking behavior without
touching any profile or scoring logic.

Usage in main.py:
    strategy = genre_first
    recommendations = recommend_songs(user_prefs, songs, k=5, strategy=strategy)

Available strategies
--------------------
    genre_first     — Genre match dominates; numeric features are tiebreakers.
    mood_first      — Mood and emotional features (valence, liveness) lead.
    energy_focused  — Pure intensity filter: energy, tempo, danceability.
    era_locked      — Decade match heavily weighted; surfaces era-specific picks.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class RankingStrategy:
    name: str
    description: str
    weights: Dict[str, float]

    @property
    def max_score(self) -> float:
        """Sum of all weights — the highest possible score under this strategy."""
        return sum(self.weights.values())


# ── Strategy 1: Genre-First ───────────────────────────────────────────────────
# Genre weight is 4× its default value.  A right-genre song will almost always
# beat a wrong-genre song regardless of how close the numeric features are.
# Use this when genre identity is the non-negotiable requirement.

genre_first = RankingStrategy(
    name="Genre-First",
    description="Genre match dominates — numeric features act as tiebreakers.",
    weights={
        "genre":            6.0,
        "mood":             2.0,
        "energy":           1.5,
        "valence":          1.5,
        "acousticness":     1.0,
        "tempo_bpm":        0.5,
        "danceability":     0.5,
        "popularity":       0.3,
        "release_decade":   0.5,
        "liveness":         0.4,
        "instrumentalness": 0.6,
        "speechiness":      0.2,
    }
)

# ── Strategy 2: Mood-First ────────────────────────────────────────────────────
# Mood, valence, and liveness are prioritized — emotional character leads.
# Use this for playlists driven by feeling rather than genre or energy level.

mood_first = RankingStrategy(
    name="Mood-First",
    description="Mood and emotional features (valence, liveness) drive ranking.",
    weights={
        "genre":            1.0,
        "mood":             6.0,
        "energy":           2.0,
        "valence":          4.0,
        "acousticness":     1.0,
        "tempo_bpm":        0.5,
        "danceability":     0.8,
        "popularity":       0.3,
        "release_decade":   0.4,
        "liveness":         2.5,
        "instrumentalness": 0.5,
        "speechiness":      0.4,
    }
)

# ── Strategy 3: Energy-Focused ────────────────────────────────────────────────
# Energy, tempo, and danceability dominate — genre is nearly irrelevant.
# A fast high-energy song wins regardless of label.  Use for workout playlists
# or any context where intensity matters more than genre identity.

energy_focused = RankingStrategy(
    name="Energy-Focused",
    description="Ranks by intensity — energy, tempo, and danceability dominate.",
    weights={
        "genre":            0.8,
        "mood":             0.8,
        "energy":           8.0,
        "valence":          1.0,
        "acousticness":     0.5,
        "tempo_bpm":        3.5,
        "danceability":     3.5,
        "popularity":       0.3,
        "release_decade":   0.3,
        "liveness":         0.5,
        "instrumentalness": 0.3,
        "speechiness":      0.2,
    }
)

# ── Strategy 4: Era-Locked ────────────────────────────────────────────────────
# Release decade is weighted at 6.0 — songs from the wrong era are strongly
# penalized.  Use for decade-specific playlists or nostalgia listeners who
# want the 90s feel even if it means a different genre or mood.

era_locked = RankingStrategy(
    name="Era-Locked",
    description="Prioritizes songs from the user's target release decade.",
    weights={
        "genre":            1.5,
        "mood":             1.5,
        "energy":           2.0,
        "valence":          1.5,
        "acousticness":     1.0,
        "tempo_bpm":        0.8,
        "danceability":     0.8,
        "popularity":       0.5,
        "release_decade":   6.0,
        "liveness":         0.8,
        "instrumentalness": 0.8,
        "speechiness":      0.3,
    }
)
