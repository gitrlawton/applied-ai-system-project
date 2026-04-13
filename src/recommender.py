from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int
    release_decade: int
    liveness: float
    instrumentalness: float
    speechiness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    int_fields = {"id", "popularity", "release_decade"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness",
                    "liveness", "instrumentalness", "speechiness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict, weights: Dict = None) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user preference profile.

    Returns a (score, reasons) tuple where:
      - score  is the total numeric score
      - reasons is a list of human-readable strings, one per feature,
        explaining each feature's contribution to the score.

    Scoring formula (from src/recipe.py):
      categorical features  → full weight on exact match, 0 on miss
      numeric features      → weight × (1 − |song_value − user_target|)
      tempo is normalised   → norm(bpm) = (bpm − TEMPO_MIN) / (TEMPO_MAX − TEMPO_MIN)

    Pass a custom weights dict (e.g. from a RankingStrategy) to override defaults.
    """
    try:
        from src.recipe import WEIGHTS as _DEFAULT_WEIGHTS, TEMPO_MIN, TEMPO_MAX, DECADE_MIN, DECADE_MAX
    except ImportError:
        from recipe import WEIGHTS as _DEFAULT_WEIGHTS, TEMPO_MIN, TEMPO_MAX, DECADE_MIN, DECADE_MAX

    W = weights if weights is not None else _DEFAULT_WEIGHTS

    score = 0.0
    reasons: List[str] = []

    # ── Categorical features ──────────────────────────────────────────────────

    if song["genre"] == user_prefs["genre"]:
        pts = W["genre"]
        reasons.append(f"genre match (+{pts:.1f})")
    else:
        pts = 0.0
        reasons.append(f"genre mismatch (+0.0)")
    score += pts

    if song["mood"] == user_prefs["mood"]:
        pts = W["mood"]
        reasons.append(f"mood match (+{pts:.1f})")
    else:
        pts = 0.0
        reasons.append(f"mood mismatch (+0.0)")
    score += pts

    # ── Numeric features ──────────────────────────────────────────────────────

    pts = W["energy"] * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    score += pts
    reasons.append(f"energy (+{pts:.2f})")

    pts = W["valence"] * (1 - abs(song["valence"] - user_prefs["target_valence"]))
    score += pts
    reasons.append(f"valence (+{pts:.2f})")

    pts = W["acousticness"] * (1 - abs(song["acousticness"] - user_prefs["target_acousticness"]))
    score += pts
    reasons.append(f"acousticness (+{pts:.2f})")

    norm_song_tempo = (song["tempo_bpm"] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    norm_user_tempo = (user_prefs["target_tempo_bpm"] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    pts = W["tempo_bpm"] * (1 - abs(norm_song_tempo - norm_user_tempo))
    score += pts
    reasons.append(f"tempo (+{pts:.2f})")

    pts = W["danceability"] * (1 - abs(song["danceability"] - user_prefs["target_danceability"]))
    score += pts
    reasons.append(f"danceability (+{pts:.2f})")

    # ── New features ──────────────────────────────────────────────────────────

    # Popularity: normalize 0-100 to 0-1 before differencing
    pts = W["popularity"] * (1 - abs(song["popularity"] / 100 - user_prefs["preferred_popularity"] / 100))
    score += pts
    reasons.append(f"popularity (+{pts:.2f})")

    # Release decade: normalize 1960-2020 to 0-1 before differencing
    norm_song_decade = (song["release_decade"] - DECADE_MIN) / (DECADE_MAX - DECADE_MIN)
    norm_user_decade = (user_prefs["target_release_decade"] - DECADE_MIN) / (DECADE_MAX - DECADE_MIN)
    pts = W["release_decade"] * (1 - abs(norm_song_decade - norm_user_decade))
    score += pts
    reasons.append(f"release decade (+{pts:.2f})")

    # Liveness: 0=studio-polished, 1=raw live recording
    pts = W["liveness"] * (1 - abs(song["liveness"] - user_prefs["target_liveness"]))
    score += pts
    reasons.append(f"liveness (+{pts:.2f})")

    # Instrumentalness: 0=fully vocal, 1=fully instrumental
    pts = W["instrumentalness"] * (1 - abs(song["instrumentalness"] - user_prefs["target_instrumentalness"]))
    score += pts
    reasons.append(f"instrumentalness (+{pts:.2f})")

    # Speechiness: 0=no spoken word, 1=all speech (rap, podcast-style)
    pts = W["speechiness"] * (1 - abs(song["speechiness"] - user_prefs["target_speechiness"]))
    score += pts
    reasons.append(f"speechiness (+{pts:.2f})")

    return score, reasons


def _diverse_select(scored: List[Tuple], k: int, artist_penalty: float, genre_penalty: float) -> List[Tuple]:
    """
    Greedy diversity-aware selection.

    On each pass, applies a score multiplier to any remaining song whose artist
    or genre is already represented in the selected list, then picks the song
    with the highest penalized score.

    The original (unpenalized) score is preserved in the output so the quality
    signal stays readable.  A note is appended to the explanation whenever a
    song's position was affected by the diversity penalty.
    """
    selected = []
    selected_artists: set = set()
    selected_genres: set = set()
    remaining = list(scored)

    while len(selected) < k and remaining:
        best_idx = 0
        best_penalized = -1.0

        for i, (song, score, _) in enumerate(remaining):
            penalized = score
            if song["artist"] in selected_artists:
                penalized *= artist_penalty
            if song["genre"] in selected_genres:
                penalized *= genre_penalty
            if penalized > best_penalized:
                best_penalized = penalized
                best_idx = i

        song, score, explanation = remaining.pop(best_idx)

        # Append a note when this song's position was affected by a penalty
        penalty_notes = []
        if song["artist"] in selected_artists:
            penalty_notes.append(f"artist repeat (x{artist_penalty:.2f})")
        if song["genre"] in selected_genres:
            penalty_notes.append(f"genre repeat (x{genre_penalty:.2f})")
        if penalty_notes:
            explanation += ", diversity penalty: " + " + ".join(penalty_notes)

        selected.append((song, score, explanation))
        selected_artists.add(song["artist"])
        selected_genres.add(song["genre"])

    return selected


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, strategy=None, diversity: bool = True) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, sorts by score descending, and returns the top k.
    Required by src/main.py

    Pass a RankingStrategy to override default feature weights.
    Set diversity=False to disable diversity re-ranking and return raw top-k.
    Return format: list of (song_dict, score, explanation_string)
    """
    try:
        from src.recipe import ARTIST_PENALTY, GENRE_PENALTY
    except ImportError:
        from recipe import ARTIST_PENALTY, GENRE_PENALTY

    weights = strategy.weights if strategy is not None else None
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights=weights)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)

    if not diversity:
        return scored[:k]

    return _diverse_select(scored, k, ARTIST_PENALTY, GENRE_PENALTY)
