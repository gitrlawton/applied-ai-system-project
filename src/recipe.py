"""
Algorithm Recipe — Music Recommender Simulation
================================================

This file defines:
  1. WEIGHTS        — the point values assigned to each feature
  2. TEMPO_MIN/MAX  — normalization bounds for tempo_bpm
  3. Three taste profiles that use these weights

SCORING FORMULA (one song)
---------------------------
score = WEIGHTS["genre"]        * (song.genre == user.genre)
      + WEIGHTS["mood"]         * (song.mood == user.mood)
      + WEIGHTS["energy"]       * (1 - |song.energy       - user.target_energy|)
      + WEIGHTS["valence"]      * (1 - |song.valence      - user.target_valence|)
      + WEIGHTS["acousticness"] * (1 - |song.acousticness - user.target_acousticness|)
      + WEIGHTS["tempo_bpm"]    * (1 - |norm(song.bpm)    - norm(user.target_tempo_bpm)|)
      + WEIGHTS["danceability"] * (1 - |song.danceability - user.target_danceability|)

  Categorical features (genre, mood) score their full weight on a match, 0 on a miss.
  Numeric features score on a 0-1 closeness scale: perfect match = full weight, maximum
  difference = 0. Tempo is normalized to 0-1 before differencing using TEMPO_MIN/MAX.

RANKING RULE
------------
Score every song in the catalog. Sort descending. Return the top k.

MAX POSSIBLE SCORE
------------------
Sum of all weights = 3.0 + 2.0 + 2.5 + 2.0 + 1.5 + 1.0 + 1.0 = 13.0


WHY THESE WEIGHTS
-----------------
The "common starting point" of genre=2.0, mood=1.0 preserves the right 2:1 ratio
between genre and mood, but with a 20-song catalog spanning 10 distinct genres the
categorical features need more pull — otherwise the five numeric features (max 8.0
combined) can overpower a genre mismatch and float a metal track into a lofi session.

genre = 3.0
  Our catalog has 10 genres. A genre mismatch almost always signals a fundamental
  incompatibility in production style, instrumentation, and tempo range. Raising
  genre to 3.0 ensures a wrong-genre song can never outscore a right-genre song
  purely on numeric similarity. It is the hardest filter in the system.

mood = 2.0  (not 1.0)
  Mood is partially redundant with energy and valence — "intense" songs trend high
  energy, "chill" songs trend low. But mood also captures things the numbers miss:
  "focused" and "chill" have overlapping energy ranges yet feel different. 2.0 gives
  mood enough weight to act as a tiebreaker between numeric near-matches without
  letting it override genre.

energy = 2.5
  The single most important numeric axis. It cleanly separates the catalog into
  workout territory (0.90+), everyday listening (0.60-0.85), and background/study
  (below 0.45). Given its range across our 20 songs (0.18 to 0.98), a 0.5-unit
  miss costs 1.25 points — enough to matter.

valence = 2.0
  Emotional positivity is real and distinct from energy. "Broken Hallelujah" (soul,
  sad, valence 0.28) and "Spacewalk Thoughts" (ambient, chill, valence 0.65) have
  similar energy but feel completely different. Valence carries that.

acousticness = 1.5
  Texture preference — organic vs. electronic — is real but secondary. A user who
  wants lofi will tolerate mild electronic production; they will not tolerate a metal
  guitar tone. So acousticness earns fewer points than energy or valence.

tempo_bpm = 1.0
  Useful secondary signal but context-dependent. 90 BPM jazz and 90 BPM hip-hop
  feel different because genre already handles that distinction. Lowest numeric weight.

danceability = 1.0
  Most correlated with energy in this catalog (Gym Hero: 0.93/0.88, Library Rain:
  0.35/0.58). Earns the same low weight as tempo to avoid double-counting intensity.
"""

# ── Weights ───────────────────────────────────────────────────────────────────

WEIGHTS = {
    "genre":        3.0,   # categorical — match or no match
    "mood":         2.0,   # categorical — match or no match
    "energy":       2.5,   # numeric closeness, 0-1 scale
    "valence":      2.0,   # numeric closeness, 0-1 scale
    "acousticness": 1.5,   # numeric closeness, 0-1 scale
    "tempo_bpm":    1.0,   # numeric closeness, normalized before use
    "danceability": 1.0,   # numeric closeness, 0-1 scale
}

MAX_SCORE = sum(WEIGHTS.values())   # 13.0

# Tempo normalization bounds — set from the full catalog range (54–180 BPM)
TEMPO_MIN = 54
TEMPO_MAX = 180

# ── Taste Profiles ────────────────────────────────────────────────────────────

# Profile A: Late-night study session
# Expected top results: lofi, classical, ambient — low energy, high acousticness.
# Expected low results: metal, EDM, rock — mismatches on every axis.
late_night_study = {
    "genre":               "lofi",
    "mood":                "focused",
    "target_energy":       0.38,
    "target_valence":      0.58,
    "target_acousticness": 0.80,
    "target_tempo_bpm":    78,
    "target_danceability": 0.58,
}

# Profile B: Gym / workout
# Expected top results: metal, EDM, rock — extreme energy, fast tempo, low acousticness.
# Expected low results: classical, lofi, ambient — wrong genre, wrong energy, wrong texture.
gym_session = {
    "genre":               "rock",
    "mood":                "intense",
    "target_energy":       0.95,
    "target_valence":      0.50,
    "target_acousticness": 0.05,
    "target_tempo_bpm":    155,
    "target_danceability": 0.70,
}

# Profile C: Upbeat pop / feel-good
# Expected top results: pop, indie pop — high valence, mid-high energy, moderate acousticness.
# Expected low results: metal, ambient, classical — wrong genre, wrong energy, wrong vibe.
pop_happy = {
    "genre":               "pop",
    "mood":                "happy",
    "target_energy":       0.80,
    "target_valence":      0.82,
    "target_acousticness": 0.20,
    "target_tempo_bpm":    120,
    "target_danceability": 0.80,
}

# Profile D: Sunday morning wind-down
# Expected top results: folk, classical, reggae — very acoustic, low tempo, peaceful.
# Expected low results: EDM, synthwave, hip-hop — electronic texture breaks every axis.
sunday_morning = {
    "genre":               "folk",
    "mood":                "peaceful",
    "target_energy":       0.27,
    "target_valence":      0.72,
    "target_acousticness": 0.90,
    "target_tempo_bpm":    70,
    "target_danceability": 0.38,
}
