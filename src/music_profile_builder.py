"""
Music Profile Builder — Natural Language to Music Profile
=========================================================

Converts a plain-English description of music preferences into a structured
MusicProfile dict using a Groq-hosted LLM (Llama 3) with a JSON prompt.

The LLM is instructed to return a JSON object with all 12 fields. Types are
coerced explicitly after parsing so numeric fields are always float/int
regardless of whether the model returns them as strings or numbers.
SYSTEM_PROMPT is built dynamically from VALID_GENRES and VALID_MOODS so it
stays in sync with the catalog automatically when build_catalog.py is re-run.

Public API:
    build_music_profile(description: str) -> dict
"""

import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from src.guardrails import VALID_GENRES, VALID_MOODS

load_dotenv()

SYSTEM_PROMPT = f"""You are a music preference interpreter. Convert the user's \
description into a structured music preference profile.

Return ONLY a JSON object with exactly these 12 fields — no other text:

{{
  "genre":                  one of: {', '.join(sorted(VALID_GENRES))},
  "mood":                   one of: {', '.join(sorted(VALID_MOODS))},
  "target_energy":          float 0.0–1.0,
  "target_valence":         float 0.0–1.0,
  "target_acousticness":    float 0.0–1.0,
  "target_danceability":    float 0.0–1.0,
  "target_liveness":        float 0.0–1.0,
  "target_instrumentalness":float 0.0–1.0,
  "target_speechiness":     float 0.0–1.0,
  "target_tempo_bpm":       float 54–180,
  "target_release_decade":  integer, one of: 1960 1970 1980 1990 2000 2010 2020,
  "preferred_popularity":   integer 0–100
}}"""

_FLOAT_FIELDS = [
    "target_energy", "target_valence", "target_acousticness",
    "target_danceability", "target_liveness", "target_instrumentalness",
    "target_speechiness", "target_tempo_bpm",
]
_INT_FIELDS = ["target_release_decade", "preferred_popularity"]

_llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))


def build_music_profile(description: str) -> dict:
    """Convert a natural language music description into a structured profile dict.

    Args:
        description: Plain-English description of music preferences,
                     e.g. "chill music for late night studying".

    Returns:
        A plain dict with all 12 MusicProfile fields populated and in range.
    """
    response = _llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=description),
    ])
    raw = json.loads(response.content)
    for f in _FLOAT_FIELDS:
        raw[f] = float(raw[f])
    for f in _INT_FIELDS:
        raw[f] = int(raw[f])
    return raw
