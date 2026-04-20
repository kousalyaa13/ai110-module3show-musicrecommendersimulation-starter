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
            row["id"]              = int(row["id"])
            row["energy"]          = float(row["energy"])
            row["tempo_bpm"]       = float(row["tempo_bpm"])
            row["valence"]         = float(row["valence"])
            row["danceability"]    = float(row["danceability"])
            row["acousticness"]    = float(row["acousticness"])
            row["popularity"]      = int(row["popularity"])
            row["release_decade"]  = int(row["release_decade"])
            row["vocal_presence"]  = float(row["vocal_presence"])
            row["complexity"]      = float(row["complexity"])
            songs.append(row)
    return songs

# ---------------------------------------------------------------------------
# Scoring Strategies — each function is one interchangeable scoring mode.
# All strategies share the same signature: (user_prefs, song) -> (float, List[str])
# Switch modes by passing a different function to recommend_songs().
# ---------------------------------------------------------------------------

def score_mood_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Mood-First mode: mood worth 2.0, energy 1.5, genre 0.75, acousticness 0.50, valence 0.25 (max 5.0)."""
    reasons = []

    if song["mood"] == user_prefs.get("mood", ""):
        mood_score = 2.0
        reasons.append(f"mood match: '{song['mood']}' (+2.0)")
    else:
        mood_score = 0.0
        reasons.append(f"mood '{song['mood']}' did not match (+0.0)")

    energy_diff  = abs(song["energy"] - float(user_prefs.get("energy", 0.5)))
    energy_score = round(1.5 * (1 - energy_diff), 3)
    reasons.append(f"energy {song['energy']} vs target {user_prefs.get('energy', 0.5)} (+{energy_score})")

    if song["genre"] == user_prefs.get("favorite_genre", ""):
        genre_score = 0.75
        reasons.append(f"genre match: '{song['genre']}' (+0.75)")
    else:
        genre_score = 0.0
        reasons.append(f"genre '{song['genre']}' did not match (+0.0)")

    acoustic_diff  = abs(song["acousticness"] - float(user_prefs.get("acousticness", 0.5)))
    acoustic_score = round(0.50 * (1 - acoustic_diff), 3)
    reasons.append(f"acousticness {song['acousticness']} vs target {user_prefs.get('acousticness', 0.5)} (+{acoustic_score})")

    valence_diff  = abs(song["valence"] - float(user_prefs.get("valence", 0.65)))
    valence_score = round(0.25 * (1 - valence_diff), 3)
    reasons.append(f"valence {song['valence']} vs target {user_prefs.get('valence', 0.65)} (+{valence_score})")

    total = mood_score + energy_score + genre_score + acoustic_score + valence_score
    return (round(total, 3), reasons)


def score_genre_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Genre-First mode: genre worth 2.0, mood 1.5, energy 1.0, acousticness 0.30, valence 0.20 (max 5.0)."""
    reasons = []

    if song["genre"] == user_prefs.get("favorite_genre", ""):
        genre_score = 2.0
        reasons.append(f"genre match: '{song['genre']}' (+2.0)")
    else:
        genre_score = 0.0
        reasons.append(f"genre '{song['genre']}' did not match (+0.0)")

    if song["mood"] == user_prefs.get("mood", ""):
        mood_score = 1.5
        reasons.append(f"mood match: '{song['mood']}' (+1.5)")
    else:
        mood_score = 0.0
        reasons.append(f"mood '{song['mood']}' did not match (+0.0)")

    energy_diff  = abs(song["energy"] - float(user_prefs.get("energy", 0.5)))
    energy_score = round(1.0 * (1 - energy_diff), 3)
    reasons.append(f"energy {song['energy']} vs target {user_prefs.get('energy', 0.5)} (+{energy_score})")

    acoustic_diff  = abs(song["acousticness"] - float(user_prefs.get("acousticness", 0.5)))
    acoustic_score = round(0.30 * (1 - acoustic_diff), 3)
    reasons.append(f"acousticness {song['acousticness']} vs target {user_prefs.get('acousticness', 0.5)} (+{acoustic_score})")

    valence_diff  = abs(song["valence"] - float(user_prefs.get("valence", 0.65)))
    valence_score = round(0.20 * (1 - valence_diff), 3)
    reasons.append(f"valence {song['valence']} vs target {user_prefs.get('valence', 0.65)} (+{valence_score})")

    total = genre_score + mood_score + energy_score + acoustic_score + valence_score
    return (round(total, 3), reasons)


def score_energy_focused(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Energy-Focused mode: energy worth 3.0, mood 1.0, acousticness 0.50, valence 0.30, genre 0.20 (max 5.0)."""
    reasons = []

    energy_diff  = abs(song["energy"] - float(user_prefs.get("energy", 0.5)))
    energy_score = round(3.0 * (1 - energy_diff), 3)
    reasons.append(f"energy {song['energy']} vs target {user_prefs.get('energy', 0.5)} (+{energy_score})")

    if song["mood"] == user_prefs.get("mood", ""):
        mood_score = 1.0
        reasons.append(f"mood match: '{song['mood']}' (+1.0)")
    else:
        mood_score = 0.0
        reasons.append(f"mood '{song['mood']}' did not match (+0.0)")

    acoustic_diff  = abs(song["acousticness"] - float(user_prefs.get("acousticness", 0.5)))
    acoustic_score = round(0.50 * (1 - acoustic_diff), 3)
    reasons.append(f"acousticness {song['acousticness']} vs target {user_prefs.get('acousticness', 0.5)} (+{acoustic_score})")

    valence_diff  = abs(song["valence"] - float(user_prefs.get("valence", 0.65)))
    valence_score = round(0.30 * (1 - valence_diff), 3)
    reasons.append(f"valence {song['valence']} vs target {user_prefs.get('valence', 0.65)} (+{valence_score})")

    if song["genre"] == user_prefs.get("favorite_genre", ""):
        genre_score = 0.20
        reasons.append(f"genre match: '{song['genre']}' (+0.20)")
    else:
        genre_score = 0.0
        reasons.append(f"genre '{song['genre']}' did not match (+0.0)")

    total = energy_score + mood_score + acoustic_score + valence_score + genre_score
    return (round(total, 3), reasons)


def score_advanced(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Advanced mode: uses 5 extra features — popularity, decade, detailed_mood, vocal_presence, complexity (max 5.0)."""
    reasons = []

    # Rule 1: Mood match — 1.5 pts
    if song["mood"] == user_prefs.get("mood", ""):
        mood_score = 1.5
        reasons.append(f"mood match: '{song['mood']}' (+1.5)")
    else:
        mood_score = 0.0
        reasons.append(f"mood '{song['mood']}' did not match (+0.0)")

    # Rule 2: Energy similarity — up to 1.0 pts
    energy_diff  = abs(song["energy"] - float(user_prefs.get("energy", 0.5)))
    energy_score = round(1.0 * (1 - energy_diff), 3)
    reasons.append(f"energy {song['energy']} vs target {user_prefs.get('energy', 0.5)} (+{energy_score})")

    # Rule 3: Detailed mood exact match — 0.75 pts
    if song["detailed_mood"] == user_prefs.get("detailed_mood", ""):
        detailed_score = 0.75
        reasons.append(f"detailed mood match: '{song['detailed_mood']}' (+0.75)")
    else:
        detailed_score = 0.0
        reasons.append(f"detailed mood '{song['detailed_mood']}' did not match (+0.0)")

    # Rule 4: Release decade match — 0.50 pts (exact match on preferred era)
    if song["release_decade"] == int(user_prefs.get("preferred_decade", 0)):
        decade_score = 0.50
        reasons.append(f"decade match: {song['release_decade']}s (+0.50)")
    else:
        decade_score = 0.0
        reasons.append(f"decade {song['release_decade']}s did not match (+0.0)")

    # Rule 5: Genre match — 0.50 pts
    if song["genre"] == user_prefs.get("favorite_genre", ""):
        genre_score = 0.50
        reasons.append(f"genre match: '{song['genre']}' (+0.50)")
    else:
        genre_score = 0.0
        reasons.append(f"genre '{song['genre']}' did not match (+0.0)")

    # Rule 6: Vocal presence similarity — up to 0.30 pts
    vocal_diff   = abs(song["vocal_presence"] - float(user_prefs.get("vocal_presence", 0.5)))
    vocal_score  = round(0.30 * (1 - vocal_diff), 3)
    reasons.append(f"vocal presence {song['vocal_presence']} vs target {user_prefs.get('vocal_presence', 0.5)} (+{vocal_score})")

    # Rule 7: Popularity bonus — +0.25 pts if popularity >= 70 (simulates "trending" preference)
    if user_prefs.get("prefer_popular", False) and song["popularity"] >= 70:
        pop_score = 0.25
        reasons.append(f"popularity {song['popularity']} >= 70 (+0.25)")
    else:
        pop_score = 0.0
        reasons.append(f"popularity {song['popularity']} — no bonus (+0.0)")

    # Rule 8: Complexity similarity — up to 0.20 pts
    complex_diff  = abs(song["complexity"] - float(user_prefs.get("complexity", 0.5)))
    complex_score = round(0.20 * (1 - complex_diff), 3)
    reasons.append(f"complexity {song['complexity']} vs target {user_prefs.get('complexity', 0.5)} (+{complex_score})")

    total = mood_score + energy_score + detailed_score + decade_score + genre_score + vocal_score + pop_score + complex_score
    return (round(total, 3), reasons)


# Map of mode names to strategy functions — add new modes here
SCORING_MODES: Dict[str, callable] = {
    "mood-first":      score_mood_first,
    "genre-first":     score_genre_first,
    "energy-focused":  score_energy_focused,
    "advanced":        score_advanced,
}

# Keep score_song pointing to the default mode so existing code still works
score_song = score_mood_first


def apply_diversity(
    scored: List[Tuple[Dict, float, str]],
    k: int,
    artist_penalty: float = 1.5,
    genre_limit: int = 2,
    genre_penalty: float = 0.8,
) -> List[Tuple[Dict, float, str]]:
    """Greedy diversity filter applied after scoring.

    Walks the sorted list and picks songs one at a time. Each time a song is
    selected, its artist and genre are recorded. Later candidates from the same
    artist lose artist_penalty points; candidates from a genre already at
    genre_limit lose genre_penalty points. Penalties are applied on the fly so
    a penalized song can still be picked if nothing better remains.
    """
    seen_artists: Dict[str, int] = {}
    seen_genres:  Dict[str, int] = {}
    remaining = list(scored)
    result = []

    while len(result) < k and remaining:
        # Re-score remaining candidates with current diversity penalties
        candidates = []
        for song, score, explanation in remaining:
            penalty = 0.0
            notes   = []

            if seen_artists.get(song["artist"], 0) >= 1:
                penalty += artist_penalty
                notes.append(f"artist '{song['artist']}' already in results (-{artist_penalty})")

            if seen_genres.get(song["genre"], 0) >= genre_limit:
                penalty += genre_penalty
                notes.append(f"genre '{song['genre']}' over limit of {genre_limit} (-{genre_penalty})")

            adjusted_score  = round(max(score - penalty, 0.0), 3)
            new_explanation = explanation + (" | DIVERSITY: " + ", ".join(notes) if notes else "")
            candidates.append((song, adjusted_score, new_explanation))

        # Pick the best candidate after penalties
        candidates.sort(key=lambda x: x[1], reverse=True)
        chosen_song, chosen_score, chosen_exp = candidates[0]

        result.append((chosen_song, chosen_score, chosen_exp))
        seen_artists[chosen_song["artist"]] = seen_artists.get(chosen_song["artist"], 0) + 1
        seen_genres[chosen_song["genre"]]   = seen_genres.get(chosen_song["genre"], 0) + 1

        # Remove the chosen song from remaining pool
        remaining = [(s, sc, ex) for s, sc, ex in remaining if s["id"] != chosen_song["id"]]

    return result


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "mood-first",
    diversity: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Score every song using the chosen mode, sort descending, return top k.

    Set diversity=True to apply the artist/genre diversity penalty before
    returning results.
    """
    strategy = SCORING_MODES.get(mode, score_mood_first)
    scored = [
        (song, score, " | ".join(reasons))
        for song in songs
        for score, reasons in [strategy(user_prefs, song)]
    ]
    scored.sort(key=lambda x: x[1], reverse=True)

    if diversity:
        return apply_diversity(scored, k)
    return scored[:k]
