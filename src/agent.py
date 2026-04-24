"""
Agent — Recster Agentic Workflow
=================================

Orchestrates music recommendations via a five-step LangGraph agent loop:

  1. parse_intent        — extract genre and mood from the user's description
  2. build_music_profile — convert the description into a full 12-field profile
  3. get_recommendations — score and rank the catalog against the profile
  4. evaluate_results    — check whether the top result matches stated intent
  5. refine_music_profile      — adjust genre/mood if evaluation fails, then re-rank

All inter-tool data flows through module-level caches (_last_intent,
_last_music_profile, _last_recommendations). Every tool takes only
`description: str` so the LLM never needs to pass complex data between tools —
eliminating hallucination of inter-tool arguments entirely. Threading events
coordinate tools that the LLM batches in parallel.

Public API:
    agent           — LangGraph agent; call agent.invoke({"messages": [("user", "...")]})
    reset_agent_state() — clear all caches and events; call before each agent.invoke in Flask
"""

import os
import json
import difflib
import threading
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage

from src.guardrails import validate_music_profile, VALID_GENRES, VALID_MOODS
from src.music_profile_builder import build_music_profile as _build_music_profile
from src.recommender import load_songs, recommend_songs

load_dotenv()

# temperature=0 keeps tool call ordering deterministic.
_llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"), temperature=0)

# All inter-tool data flows through these module-level caches.
# Threading events let tools that run in parallel wait on each other safely.
_last_intent: dict = {}
_last_music_profile: dict = {}
_last_recommendations: list = []

_intent_ready = threading.Event()
_music_profile_ready = threading.Event()
_recommendations_ready = threading.Event()


def reset_agent_state() -> None:
    """Clear all inter-tool caches and reset threading events.

    Must be called at the start of every Flask request to prevent state from
    one request bleeding into the next.
    """
    global _last_intent, _last_music_profile, _last_recommendations
    _last_intent = {}
    _last_music_profile = {}
    _last_recommendations.clear()
    _intent_ready.clear()
    _music_profile_ready.clear()
    _recommendations_ready.clear()


def _nearest_valid(value: str, valid_set: set) -> str:
    """Return the closest match from valid_set, or the first element as fallback."""
    matches = difflib.get_close_matches(value, valid_set, n=1, cutoff=0.6)
    return matches[0] if matches else sorted(valid_set)[0]


_INTENT_SYSTEM_PROMPT = (
    'Extract the music genre and mood the user wants. '
    'Respond with JSON only, no other text: {"genre": "...", "mood": "..."}'
)


@tool
def parse_intent(description: str) -> dict:
    """Extract the user's intended genre and mood from their plain-English description."""
    global _last_intent
    _intent_ready.clear()
    response = _llm.invoke([
        SystemMessage(content=_INTENT_SYSTEM_PROMPT),
        HumanMessage(content=description),
    ])
    try:
        intent = json.loads(response.content)
    except (json.JSONDecodeError, KeyError):
        intent = {"genre": "pop", "mood": "happy"}
    _last_intent = intent
    _intent_ready.set()
    return intent


@tool
def build_music_profile(description: str) -> dict:
    """Convert a natural language music description into a structured 12-field preference profile."""
    global _last_music_profile
    _music_profile_ready.clear()
    _recommendations_ready.clear()
    profile = _build_music_profile(description)
    if profile.get("genre") not in VALID_GENRES:
        profile["genre"] = _nearest_valid(profile["genre"], VALID_GENRES)
    if profile.get("mood") not in VALID_MOODS:
        profile["mood"] = _nearest_valid(profile["mood"], VALID_MOODS)
    validate_music_profile(profile)
    _last_music_profile = profile
    _music_profile_ready.set()
    return profile


@tool
def get_recommendations(description: str) -> list:
    """Score and rank all songs against the music profile for this description. Returns top 5."""
    global _last_recommendations
    if not _last_music_profile:
        _music_profile_ready.wait(timeout=60)
    if not _last_music_profile:
        return [{"error": "Profile not available. Call build_music_profile first."}]
    _recommendations_ready.clear()
    songs = load_songs("data/spotify_data.csv")
    results = recommend_songs(_last_music_profile, songs, k=5)
    _last_recommendations = [
        {
            "title": s["title"],
            "artist": s["artist"],
            "genre": s["genre"],
            "mood": s["mood"],
            "score": round(sc, 2),
        }
        for s, sc, _ in results
    ]
    _recommendations_ready.set()
    return _last_recommendations


@tool
def evaluate_results(description: str) -> dict:
    """Check whether the top recommendation matches the profile's target genre and mood."""
    if not _last_recommendations:
        _recommendations_ready.wait(timeout=60)
    if not _last_recommendations:
        return {"passed": False, "error": "No recommendations available."}
    if not _last_music_profile:
        _music_profile_ready.wait(timeout=60)
    top = _last_recommendations[0]
    target_genre = _last_music_profile.get("genre", "")
    target_mood = _last_music_profile.get("mood", "")
    passed = (top["genre"] == target_genre) or (top["mood"] == target_mood)
    return {
        "passed": passed,
        "top_song": top["title"],
        "top_genre": top["genre"],
        "top_mood": top["mood"],
    }


@tool
def refine_music_profile(description: str) -> dict:
    """Adjust the music profile's genre and mood to better match the user's stated intent."""
    global _last_music_profile
    if not _last_music_profile:
        _music_profile_ready.wait(timeout=60)
    if not _last_music_profile:
        return {"error": "No profile available. Call build_music_profile first."}
    if not _last_intent:
        _intent_ready.wait(timeout=60)
    music_profile = dict(_last_music_profile)
    music_profile["genre"] = _nearest_valid(_last_intent.get("genre", ""), VALID_GENRES)
    music_profile["mood"] = _nearest_valid(_last_intent.get("mood", ""), VALID_MOODS)
    try:
        validate_music_profile(music_profile)
    except ValueError as e:
        return {"error": str(e)}
    _last_music_profile = music_profile
    _recommendations_ready.clear()
    _last_recommendations.clear()
    return music_profile


_system_prompt = """You are Recster, a music recommendation agent.
Follow these steps in order, one at a time:

1. Call parse_intent with the user's description.
2. Call build_music_profile with the user's description.
3. Call get_recommendations with the user's description.
4. Call evaluate_results with the user's description.
5. If evaluate_results returns passed=false, call refine_music_profile with the description,
   then call get_recommendations again, then call evaluate_results again.
6. Return the final recommendations to the user.

All tools take only the description string. Never pass profile dicts or result lists between tools."""

_tools = [parse_intent, build_music_profile, get_recommendations, evaluate_results, refine_music_profile]

agent = create_react_agent(_llm, _tools, prompt=_system_prompt)
