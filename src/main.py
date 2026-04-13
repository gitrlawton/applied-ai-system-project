"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs
from .recipe import (
    MAX_SCORE,
    pop_happy, late_night_study, gym_session, sunday_morning,
    energy_sad_clash, impossible_combo, lofi_numbers_metal_label,
    flat_midpoint, lone_wolf_genre,
)
from .strategies import genre_first, mood_first, energy_focused, era_locked

# ── Local user profiles ───────────────────────────────────────────────────────

high_energy_pop = {
    "genre":                    "pop",
    "mood":                     "happy",
    "target_energy":            0.88,
    "target_valence":           0.85,
    "target_acousticness":      0.12,
    "target_tempo_bpm":         126,
    "target_danceability":      0.85,
    "preferred_popularity":     85,
    "target_release_decade":    2020,
    "target_liveness":          0.08,
    "target_instrumentalness":  0.03,
    "target_speechiness":       0.05,
}

chill_lofi = {
    "genre":                    "lofi",
    "mood":                     "chill",
    "target_energy":            0.38,
    "target_valence":           0.58,
    "target_acousticness":      0.80,
    "target_tempo_bpm":         75,
    "target_danceability":      0.58,
    "preferred_popularity":     65,
    "target_release_decade":    2020,
    "target_liveness":          0.05,
    "target_instrumentalness":  0.84,
    "target_speechiness":       0.03,
}

deep_intense_rock = {
    "genre":                    "rock",
    "mood":                     "intense",
    "target_energy":            0.92,
    "target_valence":           0.45,
    "target_acousticness":      0.08,
    "target_tempo_bpm":         150,
    "target_danceability":      0.65,
    "preferred_popularity":     60,
    "target_release_decade":    2000,
    "target_liveness":          0.18,
    "target_instrumentalness":  0.06,
    "target_speechiness":       0.06,
}

# ── Active ranking strategy ───────────────────────────────────────────────────
# Swap to mood_first, energy_focused, era_locked, or None (default weights)

STRATEGY = genre_first

# ── All profiles to run ───────────────────────────────────────────────────────

PROFILES = [
    ("Edge Case: Energy-Sad Clash",       energy_sad_clash),
    ("Edge Case: Impossible Combo",       impossible_combo),
    ("Edge Case: Lofi Numbers Metal Label", lofi_numbers_metal_label),
    ("Edge Case: Flat Midpoint",          flat_midpoint),
    ("Edge Case: Lone Wolf Genre",        lone_wolf_genre),
]

# ─────────────────────────────────────────────────────────────────────────────


def print_results(label: str, user_prefs: dict, recommendations: list, strategy=None) -> None:
    import textwrap
    try:
        from tabulate import tabulate as _tabulate
    except ImportError:
        _tabulate = None

    W = 68
    max_score = strategy.max_score if strategy is not None else MAX_SCORE

    # ── Header ─────────────────────────────────────────────────────────────
    print()
    print("=" * W)
    print(f"  {label}")
    print(f"  Strategy : {strategy.name if strategy else 'Default'}")
    print(f"  Profile  : genre={user_prefs['genre']!r}"
          f"  |  mood={user_prefs['mood']!r}"
          f"  |  energy={user_prefs['target_energy']}")
    print("=" * W)
    print()

    # ── Summary table ───────────────────────────────────────────────────────
    headers = ["#", "Title", "Artist", "Genre / Mood", "Score"]
    rows = [
        [
            rank,
            song["title"],
            song["artist"],
            f"{song['genre']} / {song['mood']}",
            f"{score:.2f} / {max_score:.1f}",
        ]
        for rank, (song, score, _) in enumerate(recommendations, start=1)
    ]

    if _tabulate:
        table_str = _tabulate(
            rows, headers=headers, tablefmt="simple",
            colalign=("right", "left", "left", "left", "right"),
        )
        for line in table_str.splitlines():
            print("  " + line)
    else:
        # Pure ASCII fallback
        col_w = [max(len(str(r[i])) for r in ([headers] + rows)) for i in range(5)]
        print("  " + "  ".join(f"{headers[i]:<{col_w[i]}}" for i in range(5)))
        print("  " + "  ".join("-" * col_w[i] for i in range(5)))
        for row in rows:
            print("  " + "  ".join(f"{str(row[i]):<{col_w[i]}}" for i in range(5)))

    # ── Score Breakdown ─────────────────────────────────────────────────────
    print()
    print("  " + "-" * (W - 2))
    print("  Score Breakdown")
    print("  " + "-" * (W - 2))

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        parts = explanation.split(", ")
        regular = [p for p in parts if "diversity penalty" not in p]
        diversity_notes = [p for p in parts if "diversity penalty" in p]

        print(f"\n  {rank}. {song['title']}  [{song['artist']}]")
        wrapped = textwrap.fill(
            ", ".join(regular),
            width=W,
            initial_indent="     ",
            subsequent_indent="     ",
        )
        print(wrapped)
        if diversity_notes:
            print(f"     * {', '.join(diversity_notes)}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    k = 5

    for label, user_prefs in PROFILES:
        recommendations = recommend_songs(user_prefs, songs, k=k, strategy=STRATEGY)
        print_results(label, user_prefs, recommendations, strategy=STRATEGY)


if __name__ == "__main__":
    main()
