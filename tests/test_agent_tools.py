import pytest
from src.guardrails import validate_music_profile
from src.recommender import load_songs, recommend_songs
from src.recipe import late_night_study, pop_happy

# "piano"/"focused" are confirmed-valid catalog values (audited in Phase 1A).
_VALID_MUSIC_PROFILE = {
    "genre": "piano", "mood": "focused",
    "target_energy": 0.38, "target_valence": 0.58,
    "target_acousticness": 0.80, "target_tempo_bpm": 78,
    "target_danceability": 0.58, "preferred_popularity": 62,
    "target_release_decade": 2020, "target_liveness": 0.05,
    "target_instrumentalness": 0.80, "target_speechiness": 0.03,
}


def test_validate_music_profile_passes_valid_input():
    assert validate_music_profile(_VALID_MUSIC_PROFILE) == _VALID_MUSIC_PROFILE


def test_validate_music_profile_rejects_out_of_range():
    music_profile = {**_VALID_MUSIC_PROFILE, "target_energy": 1.8}
    # Match on "target_energy" to avoid em-dash in "0.0–1.0" being misread as a regex range.
    with pytest.raises(ValueError, match="target_energy"):
        validate_music_profile(music_profile)


def test_validate_music_profile_rejects_unknown_genre():
    music_profile = {**_VALID_MUSIC_PROFILE, "genre": "bossa nova"}
    with pytest.raises(ValueError, match="not in catalog"):
        validate_music_profile(music_profile)


def test_recommendations_return_five_results():
    songs = load_songs("data/spotify_data.csv")
    results = recommend_songs(late_night_study, songs, k=5)
    assert len(results) == 5


def test_top_result_has_required_keys():
    songs = load_songs("data/spotify_data.csv")
    results = recommend_songs(pop_happy, songs, k=5)
    song, score, explanation = results[0]
    assert "title" in song
    assert "genre" in song
    assert score > 0
