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
    pop_happy, late_night_study, gym_session, sunday_morning,
    energy_sad_clash, impossible_combo, lofi_numbers_metal_label,
    flat_midpoint, lone_wolf_genre,
)

# ── Local user profiles ───────────────────────────────────────────────────────

high_energy_pop = {
    "genre":               "pop",
    "mood":                "happy",
    "target_energy":       0.88,
    "target_valence":      0.85,
    "target_acousticness": 0.12,
    "target_tempo_bpm":    126,
    "target_danceability": 0.85,
}

chill_lofi = {
    "genre":               "lofi",
    "mood":                "chill",
    "target_energy":       0.38,
    "target_valence":      0.58,
    "target_acousticness": 0.80,
    "target_tempo_bpm":    75,
    "target_danceability": 0.58,
}

deep_intense_rock = {
    "genre":               "rock",
    "mood":                "intense",
    "target_energy":       0.92,
    "target_valence":      0.45,
    "target_acousticness": 0.08,
    "target_tempo_bpm":    150,
    "target_danceability": 0.65,
}

# ── All profiles to run ───────────────────────────────────────────────────────

PROFILES = [
    ("Edge Case: Energy-Sad Clash",       energy_sad_clash),
    ("Edge Case: Impossible Combo",       impossible_combo),
    ("Edge Case: Lofi Numbers Metal Label", lofi_numbers_metal_label),
    ("Edge Case: Flat Midpoint",          flat_midpoint),
    ("Edge Case: Lone Wolf Genre",        lone_wolf_genre),
]

# ─────────────────────────────────────────────────────────────────────────────


def print_results(label: str, user_prefs: dict, recommendations: list) -> None:
    W = 60
    heavy = "=" * W
    light = "-" * W

    print()
    print(heavy)
    print(f"  {label}")
    print(f"  Profile : genre={user_prefs['genre']!r}"
          f"  |  mood={user_prefs['mood']!r}"
          f"  |  energy={user_prefs['target_energy']}")
    print(heavy)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons = explanation.split(", ")
        print()
        print(f"  #{rank}")
        print(f"       Song Title        : {song['title']}")
        print(f"       Artist            : {song['artist']}  |  {song['genre']} / {song['mood']}")
        print(f"       Score             : {score:.2f} / 13.0")
        print(f"       Reasons for Score :")
        for reason in reasons:
            print(f"           {reason}")
        print()
        print(light)


def main() -> None:
    songs = load_songs("data/songs.csv")
    k = 5

    for label, user_prefs in PROFILES:
        recommendations = recommend_songs(user_prefs, songs, k=k)
        print_results(label, user_prefs, recommendations)


if __name__ == "__main__":
    main()
