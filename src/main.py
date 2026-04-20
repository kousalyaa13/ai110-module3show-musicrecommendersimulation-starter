"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: late-night chill session — low energy, acoustic, slightly melancholy
    user_prefs = {
        "favorite_genre":  "lofi",
        "mood":            "chill",
        "energy":           0.38,   # quiet, low-intensity
        "valence":          0.55,   # mellow but not sad
        "acousticness":     0.80,   # strongly prefers organic/acoustic texture
        "likes_acoustic":   True,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  TOP RECOMMENDATIONS")
    print("=" * 50)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Score: {score:.2f} / 5.0")
        print("    Why:")
        for reason in explanation.split(" | "):
            print(f"      - {reason}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
