"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs
from .recipe import pop_happy, late_night_study, gym_session, sunday_morning


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Swap to late_night_study, gym_session, or sunday_morning to test other profiles
    user_prefs = pop_happy
    k = 5

    recommendations = recommend_songs(user_prefs, songs, k=k)

    W = 60
    heavy = "=" * W
    light = "-" * W

    print()
    print(heavy)
    print(f"  Music Recommender  |  Top {k} Results")
    print(heavy)
    print(f"  Profile : genre={user_prefs['genre']!r}"
          f"  |  mood={user_prefs['mood']!r}"
          f"  |  energy={user_prefs['target_energy']}")
    print(light)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons = explanation.split(", ")
        print()
        print(f"  #{rank}")
        print(f"       Song Title        : {song['title']}")
        print(f"       Artist            : {song['artist']}  |  {song['genre']} / {song['mood']}")
        print(f"       Score             : {score:.2f} / 13.0")
        print(f"       Reasons for Score :")
        for reason in reasons:
            print(f"           {reason}")
        print()
        print(light)


if __name__ == "__main__":
    main()
