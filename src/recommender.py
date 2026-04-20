import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]           = int(row["id"])
            row["energy"]       = float(row["energy"])
            row["tempo_bpm"]    = float(row["tempo_bpm"])
            row["valence"]      = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences (max 5.0) and return (score, reasons)."""
    reasons = []

    # Rule 1: Mood — 2.0 pts (exact match)
    if song["mood"] == user_prefs.get("mood", ""):
        mood_score = 2.0
        reasons.append(f"mood match: '{song['mood']}' (+2.0)")
    else:
        mood_score = 0.0
        reasons.append(f"mood '{song['mood']}' did not match (+0.0)")

    # Rule 2: Energy — up to 1.5 pts (linear distance)
    energy_diff  = abs(song["energy"] - float(user_prefs.get("energy", 0.5)))
    energy_score = round(1.5 * (1 - energy_diff), 3)
    reasons.append(f"energy {song['energy']} vs target {user_prefs.get('energy', 0.5)} (+{energy_score})")

    # Rule 3: Genre — 0.75 pts (exact match)
    if song["genre"] == user_prefs.get("favorite_genre", ""):
        genre_score = 0.75
        reasons.append(f"genre match: '{song['genre']}' (+0.75)")
    else:
        genre_score = 0.0
        reasons.append(f"genre '{song['genre']}' did not match (+0.0)")

    # Rule 4: Acousticness — up to 0.50 pts (linear distance)
    acoustic_diff  = abs(song["acousticness"] - float(user_prefs.get("acousticness", 0.5)))
    acoustic_score = round(0.50 * (1 - acoustic_diff), 3)
    reasons.append(f"acousticness {song['acousticness']} vs target {user_prefs.get('acousticness', 0.5)} (+{acoustic_score})")

    # Rule 5: Valence — up to 0.25 pts (linear distance)
    valence_diff  = abs(song["valence"] - float(user_prefs.get("valence", 0.65)))
    valence_score = round(0.25 * (1 - valence_diff), 3)
    reasons.append(f"valence {song['valence']} vs target {user_prefs.get('valence', 0.65)} (+{valence_score})")

    total = mood_score + energy_score + genre_score + acoustic_score + valence_score
    return (round(total, 3), reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k results."""
    scored = [
        (song, score, " | ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
