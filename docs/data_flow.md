# Data Flow: Music Recommender Simulation

## Mermaid.js Flowchart

```mermaid
flowchart TD
    A([User Preferences\nfavorite_genre · mood · energy\nvalence · acousticness]) --> B

    B[load_songs\ndata/songs.csv] --> C

    C[Song Catalog\n20 songs] --> D

    D{For each song\nin catalog...} --> E

    E[score_song] --> F
    A --> E

    F[Rule 1: Mood match?\n+2.0 pts exact match]
    F --> G[Rule 2: Energy similarity\nup to +1.5 pts]
    G --> H[Rule 3: Genre match?\n+0.75 pts exact match]
    H --> I[Rule 4: Acousticness similarity\nup to +0.50 pts]
    I --> J[Rule 5: Valence similarity\nup to +0.25 pts]

    J --> K[Total Score\n0.0 – 5.0 pts\n+ reasons list]

    K --> D
    D -->|All songs scored| L

    L[recommend_songs\nsorted by score descending] --> M

    M[Top K Results\nsong · score · explanation]

    M --> N([Output\nTitle — Score: 4.94\nBecause: mood matches chill...])

    style A fill:#4a90d9,color:#fff
    style N fill:#27ae60,color:#fff
    style E fill:#8e44ad,color:#fff
    style L fill:#e67e22,color:#fff
```

---

## Written Map

```
User Preferences (main.py:19)
        │
        ▼
load_songs("data/songs.csv")          ← reads 20 songs into List[Dict]
        │
        ▼
FOR EACH song in catalog:
    score_song(user_prefs, song)       ← recommender.py:57
        ├─ Rule 1: mood match?         → +2.00 pts
        ├─ Rule 2: energy distance     → up to +1.50 pts
        ├─ Rule 3: genre match?        → +0.75 pts
        ├─ Rule 4: acousticness dist.  → up to +0.50 pts
        └─ Rule 5: valence distance    → up to +0.25 pts
    returns (score, reasons)
        │
        ▼
scored_songs = [(song, score, reasons), ...]   ← 20 entries
        │
        ▼
recommend_songs sorts by score DESC            ← recommender.py:66
takes top k=5
        │
        ▼
Output: [(song, 4.94, ["mood matches 'chill'", ...]), ...]
```
