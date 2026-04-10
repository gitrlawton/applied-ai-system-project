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

    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

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

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user preference profile.

    Returns a (score, reasons) tuple where:
      - score  is the total numeric score (0.0 – 13.0)
      - reasons is a list of human-readable strings, one per feature,
        explaining each feature's contribution to the score.

    Scoring formula (from src/recipe.py):
      categorical features  → full weight on exact match, 0 on miss
      numeric features      → weight × (1 − |song_value − user_target|)
      tempo is normalised   → norm(bpm) = (bpm − TEMPO_MIN) / (TEMPO_MAX − TEMPO_MIN)
    """
    try:
        from src.recipe import WEIGHTS, TEMPO_MIN, TEMPO_MAX
    except ImportError:
        from recipe import WEIGHTS, TEMPO_MIN, TEMPO_MAX  # when run directly from src/

    score = 0.0
    reasons: List[str] = []

    # ── Categorical features ──────────────────────────────────────────────────

    if song["genre"] == user_prefs["genre"]:
        pts = WEIGHTS["genre"]
        reasons.append(f"genre match (+{pts:.1f})")
    else:
        pts = 0.0
        reasons.append(f"genre mismatch (+0.0)")
    score += pts

    if song["mood"] == user_prefs["mood"]:
        pts = WEIGHTS["mood"]
        reasons.append(f"mood match (+{pts:.1f})")
    else:
        pts = 0.0
        reasons.append(f"mood mismatch (+0.0)")
    score += pts

    # ── Numeric features ──────────────────────────────────────────────────────

    pts = WEIGHTS["energy"] * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    score += pts
    reasons.append(f"energy (+{pts:.2f})")

    pts = WEIGHTS["valence"] * (1 - abs(song["valence"] - user_prefs["target_valence"]))
    score += pts
    reasons.append(f"valence (+{pts:.2f})")

    pts = WEIGHTS["acousticness"] * (1 - abs(song["acousticness"] - user_prefs["target_acousticness"]))
    score += pts
    reasons.append(f"acousticness (+{pts:.2f})")

    norm_song_tempo = (song["tempo_bpm"] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    norm_user_tempo = (user_prefs["target_tempo_bpm"] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    pts = WEIGHTS["tempo_bpm"] * (1 - abs(norm_song_tempo - norm_user_tempo))
    score += pts
    reasons.append(f"tempo (+{pts:.2f})")

    pts = WEIGHTS["danceability"] * (1 - abs(song["danceability"] - user_prefs["target_danceability"]))
    score += pts
    reasons.append(f"danceability (+{pts:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, sorts by score descending, and returns the top k.
    Required by src/main.py

    Return format: list of (song_dict, score, explanation_string)
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
