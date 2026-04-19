"""
AI Profile Builder — Natural Language to Music Profile
=======================================================

Converts a plain-English description of music preferences into a structured
MusicProfile dict using a Groq-hosted LLM (Llama 3) with structured output.

The LLM is constrained via with_structured_output(MusicProfile) so Pydantic
validates field types and ranges before the result is returned. SYSTEM_PROMPT
is built dynamically from VALID_GENRES and VALID_MOODS so it stays in sync
with the catalog automatically when build_catalog.py is re-run.

Public API:
    build_profile(description: str) -> dict
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from src.guardrails import MusicProfile, VALID_GENRES, VALID_MOODS

load_dotenv()

# Built at import time from the live catalog sets so genre/mood lists never
# go out of sync with spotify_data.csv.
SYSTEM_PROMPT = f"""You are a music preference interpreter. Convert the user's \
description into a structured music preference profile.
Use only genres from this list: {", ".join(sorted(VALID_GENRES))}.
Use only moods from this list: {", ".join(sorted(VALID_MOODS))}.
All float fields must be between 0.0 and 1.0.
target_tempo_bpm must be between 54 and 180.
target_release_decade must be one of: 1960, 1970, 1980, 1990, 2000, 2010, 2020.
preferred_popularity must be between 0 and 100."""

# Module-level internals — not part of the public API.
_llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))
_structured_llm = _llm.with_structured_output(MusicProfile)


def build_profile(description: str) -> dict:
    """Convert a natural language music description into a structured profile dict.

    Invokes the Groq LLM with structured output constrained to MusicProfile.
    Pydantic enforces field types and ge/le bounds before this function returns,
    so the caller is guaranteed a valid 12-field profile.

    Args:
        description: Plain-English description of music preferences,
                     e.g. "chill music for late night studying".

    Returns:
        A plain dict with all 12 MusicProfile fields populated and in range.
    """
    result = _structured_llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=description),
    ])
    return result.model_dump()
