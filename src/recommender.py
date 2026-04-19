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
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    return []

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    Max possible score: 5.0
    """
    reasons = []

    # Rule 1: Mood — 2.0 pts
    if song["mood"] == user_prefs.get("mood", ""):
        mood_score = 2.0
        reasons.append(f"mood matches '{song['mood']}'")
    else:
        mood_score = 0.0

    # Rule 2: Energy — up to 1.5 pts
    energy_diff = abs(float(song["energy"]) - float(user_prefs.get("energy", 0.5)))
    energy_score = 1.5 * (1 - energy_diff)
    if energy_diff < 0.15:
        reasons.append(f"energy {song['energy']} closely matches your target")

    # Rule 3: Genre — 0.75 pts
    if song["genre"] == user_prefs.get("favorite_genre", ""):
        genre_score = 0.75
        reasons.append(f"genre '{song['genre']}' matches your preference")
    else:
        genre_score = 0.0

    # Rule 4: Acousticness — up to 0.50 pts
    acoustic_diff = abs(float(song["acousticness"]) - float(user_prefs.get("acousticness", 0.5)))
    acoustic_score = 0.50 * (1 - acoustic_diff)
    if acoustic_diff < 0.15:
        reasons.append(f"acoustic texture ({song['acousticness']}) suits your preference")

    # Rule 5: Valence — up to 0.25 pts
    valence_diff = abs(float(song["valence"]) - float(user_prefs.get("valence", 0.65)))
    valence_score = 0.25 * (1 - valence_diff)

    total = mood_score + energy_score + genre_score + acoustic_score + valence_score
    return (round(total, 3), reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
