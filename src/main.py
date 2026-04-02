"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs
from recipe import late_night_study, gym_session, sunday_morning


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Swap to gym_session or sunday_morning to test a different profile
    user_prefs = late_night_study

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nActive profile: genre={user_prefs['genre']!r}, "
          f"mood={user_prefs['mood']!r}, "
          f"energy={user_prefs['target_energy']}\n")
    print("Top recommendations:\n")
    for rec in recommendations:
        # Each item is (song_dict, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
