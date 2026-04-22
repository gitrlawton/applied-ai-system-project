from src.recommender import load_songs, recommend_songs
from src.recipe import (late_night_study, gym_session, pop_happy,
                        energy_sad_clash, impossible_combo,
                        lofi_numbers_metal_label, flat_midpoint, lone_wolf_genre,
                        MAX_SCORE)

MUSIC_PROFILES = {
    "Late Night Study":         late_night_study,
    "Gym Session":              gym_session,
    "Pop Happy":                pop_happy,
    "Energy-Sad Clash":         energy_sad_clash,
    "Impossible Combo":         impossible_combo,
    "Lofi Numbers Metal Label": lofi_numbers_metal_label,
    "Flat Midpoint":            flat_midpoint,
    "Lone Wolf Genre":          lone_wolf_genre,
}

# Populated from a discovery dry-run against spotify_data.csv.
EXPECTED = {
    "Late Night Study":         "Kansas City Shout - 2003 Remaster",
    "Gym Session":              "Tall Cool One - 2006 Remaster",
    "Pop Happy":                "Zero",
    "Energy-Sad Clash":         "Troubles",
    "Impossible Combo":         "The 12th Hour",
    "Lofi Numbers Metal Label": "Shed Some Light",
    "Flat Midpoint":            "Sensual Overload",
    "Lone Wolf Genre":          "Born To Lose",
}


def run():
    songs = load_songs("data/spotify_data.csv")
    passed = 0
    rows = []

    for music_profile_name, music_profile in MUSIC_PROFILES.items():
        top_song, top_score, _ = recommend_songs(music_profile, songs, k=5)[0]
        expected_title = EXPECTED[music_profile_name]
        actual_title = top_song["title"]
        confidence = round(top_score / MAX_SCORE, 2)
        ok = actual_title == expected_title
        passed += int(ok)
        rows.append({
            "music_profile_name": music_profile_name,
            "expected_title":     expected_title,
            "actual_title":       actual_title,
            "result":             "✓" if ok else "✗",
            "confidence":         confidence,
        })

    print(f"\n{'Profile':<30} {'Expected':<40} {'Actual':<40} {'':6} {'Confidence'}")
    print("-" * 125)
    for row in rows:
        print(f"{row['music_profile_name']:<30} {row['expected_title']:<40} {row['actual_title']:<40} {row['result']:<6} {row['confidence']}")

    avg_confidence = round(sum(row["confidence"] for row in rows) / len(rows), 2)
    print(f"\nResults: {passed}/{len(MUSIC_PROFILES)} passed | avg confidence: {avg_confidence}")
    return passed, len(MUSIC_PROFILES)


if __name__ == "__main__":
    passed, total = run()
    exit(0 if passed >= 6 else 1)
