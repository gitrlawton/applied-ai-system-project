import logging
import pandas as pd
from pathlib import Path
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

_catalog = pd.read_csv(Path("data/spotify_data.csv"))
VALID_GENRES = set(_catalog["genre"].dropna().unique())
VALID_MOODS  = set(_catalog["mood"].dropna().unique())


class MusicProfile(BaseModel):
    genre:                   str   = Field(description="Must match a genre in the catalog")
    mood:                    str   = Field(description="Must match a mood in the catalog")
    target_energy:           float = Field(ge=0.0, le=1.0)
    target_valence:          float = Field(ge=0.0, le=1.0)
    target_acousticness:     float = Field(ge=0.0, le=1.0)
    target_danceability:     float = Field(ge=0.0, le=1.0)
    target_liveness:         float = Field(ge=0.0, le=1.0)
    target_instrumentalness: float = Field(ge=0.0, le=1.0)
    target_speechiness:      float = Field(ge=0.0, le=1.0)
    target_tempo_bpm:        float = Field(ge=54.0, le=180.0)
    target_release_decade:   int   = Field(ge=1960, le=2020)
    preferred_popularity:    int   = Field(ge=0, le=100)


CONTRADICTIONS = [
    (
        {"genre": "classical"},
        {"mood": "euphoric"},
        "classical + euphoric: classical songs are focused/peaceful, not euphoric",
    ),
    (
        {"mood": "peaceful"},
        {"target_energy": lambda e: e > 0.7},
        "peaceful mood with high energy target (> 0.7)",
    ),
    (
        {"mood": "intense"},
        {"target_energy": lambda e: e < 0.3},
        "intense mood with very low energy target (< 0.3)",
    ),
]


def _matches(cond: dict, profile: dict) -> bool:
    for k, v in cond.items():
        val = profile.get(k, 0)
        if callable(v):
            if not v(val):
                return False
        else:
            if val != v:
                return False
    return True


def validate_profile(profile: dict) -> dict:
    errors   = []
    warnings = []

    required = [
        "genre", "mood", "target_energy", "target_valence",
        "target_acousticness", "target_tempo_bpm", "target_danceability",
        "preferred_popularity", "target_release_decade", "target_liveness",
        "target_instrumentalness", "target_speechiness",
    ]
    for key in required:
        if key not in profile:
            errors.append(f"Missing required field: {key}")

    if profile.get("genre") not in VALID_GENRES:
        errors.append(f"genre '{profile.get('genre')}' not in catalog")
    if profile.get("mood") not in VALID_MOODS:
        errors.append(f"mood '{profile.get('mood')}' not in catalog")

    float_fields = [
        "target_energy", "target_valence", "target_acousticness",
        "target_danceability", "target_liveness",
        "target_instrumentalness", "target_speechiness",
    ]
    for field in float_fields:
        val = profile.get(field)
        if val is not None and not (0.0 <= val <= 1.0):
            errors.append(f"{field} must be 0.0–1.0, got {val}")

    if not (54 <= profile.get("target_tempo_bpm", 54) <= 180):
        errors.append("target_tempo_bpm must be 54–180")
    if not (1960 <= profile.get("target_release_decade", 1960) <= 2020):
        errors.append("target_release_decade must be 1960–2020")
    if not (0 <= profile.get("preferred_popularity", 0) <= 100):
        errors.append("preferred_popularity must be 0–100")

    for cond_a, cond_b, message in CONTRADICTIONS:
        if _matches(cond_a, profile) and _matches(cond_b, profile):
            warnings.append(f"Contradictory combination: {message}")

    for w in warnings:
        logger.warning(w)
    if errors:
        raise ValueError(f"Profile validation failed: {'; '.join(errors)}")

    return profile
