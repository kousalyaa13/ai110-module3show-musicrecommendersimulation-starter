"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from tabulate import tabulate
from src.recommender import load_songs, recommend_songs


PROFILES = {
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "mood":           "chill",
        "energy":          0.38,
        "valence":         0.55,
        "acousticness":    0.80,
        "likes_acoustic":  True,
    },
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "mood":           "happy",
        "energy":          0.88,
        "valence":         0.85,
        "acousticness":    0.10,
        "likes_acoustic":  False,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "mood":           "intense",
        "energy":          0.90,
        "valence":         0.35,
        "acousticness":    0.08,
        "likes_acoustic":  False,
    },
    # --- Advanced mode profile (uses extra features) ---
    "Advanced Lofi": {
        "favorite_genre":   "lofi",
        "mood":             "chill",
        "energy":            0.38,
        "valence":           0.55,
        "acousticness":      0.80,
        "likes_acoustic":    True,
        "detailed_mood":    "dreamy",
        "preferred_decade":  2020,
        "vocal_presence":    0.08,
        "prefer_popular":    False,
        "complexity":        0.25,
    },
    "Advanced Pop": {
        "favorite_genre":   "pop",
        "mood":             "happy",
        "energy":            0.85,
        "valence":           0.85,
        "acousticness":      0.10,
        "likes_acoustic":    False,
        "detailed_mood":    "euphoric",
        "preferred_decade":  2020,
        "vocal_presence":    0.80,
        "prefer_popular":    True,
        "complexity":        0.50,
    },
    # --- Edge cases ---
    # Conflicting: wants high energy but a sad/melancholy mood
    "Angry Cardio": {
        "favorite_genre": "metal",
        "mood":           "melancholy",
        "energy":          0.95,
        "valence":         0.20,
        "acousticness":    0.05,
        "likes_acoustic":  False,
    },
    # Impossible genre: no songs in catalog match this label
    "Ghost Genre": {
        "favorite_genre": "bossa nova",
        "mood":           "relaxed",
        "energy":          0.40,
        "valence":         0.70,
        "acousticness":    0.75,
        "likes_acoustic":  True,
    },
    # Perfectly average: sits in the middle of every feature range
    "Perfectly Average": {
        "favorite_genre": "pop",
        "mood":           "focused",
        "energy":          0.50,
        "valence":         0.50,
        "acousticness":    0.50,
        "likes_acoustic":  False,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Switch profile name here to test different users
    active_profile = "Chill Lofi"
    user_prefs = PROFILES[active_profile]

    # Switch scoring mode here: "mood-first" | "genre-first" | "energy-focused" | "advanced"
    active_mode = "mood-first"

    # Set to True to apply artist/genre diversity penalty
    use_diversity = False

    recommendations = recommend_songs(user_prefs, songs, k=5, mode=active_mode, diversity=use_diversity)

    diversity_label = "diversity ON" if use_diversity else "diversity OFF"
    print(f"\nProfile: {active_profile}  |  Mode: {active_mode}  |  {diversity_label}\n")

    # Summary table — one row per recommendation
    table_rows = []
    for rank, (song, score, _) in enumerate(recommendations, start=1):
        table_rows.append([
            f"#{rank}",
            song["title"],
            song["artist"],
            song["genre"],
            song["mood"],
            f"{score:.2f} / 5.0",
        ])

    print(tabulate(
        table_rows,
        headers=["", "Title", "Artist", "Genre", "Mood", "Score"],
        tablefmt="outline",
    ))

    # Reasons breakdown — one block per song
    print("\n--- Score Breakdown ---\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"#{rank} {song['title']}")
        for reason in explanation.split(" | "):
            print(f"   - {reason}")
        print()


if __name__ == "__main__":
    main()
