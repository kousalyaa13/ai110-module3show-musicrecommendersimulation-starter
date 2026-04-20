# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder tries to answer one question: given a user's musical preferences, which songs in the catalog are the best fit right now?

It takes a taste profile — things like preferred mood, energy level, and genre — and scores every song against it. The top 5 highest-scoring songs are returned as recommendations, each with a plain-language explanation of why it was chosen.

---

## 3. Data Used

- **Size:** 20 songs in `data/songs.csv`
- **Features per song:** genre, mood, energy, tempo, valence, danceability, acousticness
- **Genres covered:** lofi, pop, rock, jazz, ambient, synthwave, indie pop, hip-hop, folk, EDM, R&B, metal, country, blues, reggae, classical, soul
- **Moods covered:** happy, chill, intense, relaxed, focused, moody, energetic, sad, euphoric, romantic, angry, nostalgic, melancholy, peaceful, calm
- **Limits:** Only 20 songs total. Most genres have just 1 song. No lyrics, no audio files, no listening history. All data is made up — not from a real music service.

---

## 4. Algorithm Summary

Each song gets a score out of 5.0 points. Higher score = better match. Here is how points are earned:

- **Mood match (+2.0):** Does the song's mood label exactly match what the user wants? If yes, big bonus. If no, zero.
- **Energy match (up to +1.5):** How close is the song's energy to the user's target? A perfect match gets 1.5. A big gap gets close to 0.
- **Genre match (+0.75):** Does the genre label exactly match? Same idea as mood — all or nothing.
- **Acousticness match (up to +0.50):** How organic vs. electronic does the song feel compared to what the user prefers?
- **Valence match (up to +0.25):** How close is the song's emotional positivity to the user's target?

All five scores are added up. Songs are sorted from highest to lowest. The top 5 are returned.

---

## 5. Observed Behavior / Biases

**Mood is everything — maybe too much.** Mood carries 40% of the total score. A song that matches on every other feature but has the wrong mood label will always rank far below a song that matches on mood alone. Two songs can sound identical but score very differently just because of a label.

**"Gym Hero" keeps crashing pop parties.** For users who want happy pop music, Gym Hero — a workout song labeled "intense" — keeps appearing in the top 5. It scores well because it is pop (genre bonus) and has matching energy. The system cannot tell that "happy-energetic" and "workout-intense" feel completely different to a real listener. It only sees numbers and labels.

**Adjacent genres are strangers.** "Pop" and "indie pop" have nearly identical songs in this catalog, but the system treats them as completely unrelated. A user who says "pop" gets the genre bonus for Sunrise City but nothing for Rooftop Lights — even though they sound almost the same.

---

## 6. Evaluation Process

Six profiles were tested by running the recommender and reading the top 5 results:

| Profile | What it tests |
|---|---|
| Chill Lofi | Normal use case — clear, consistent preferences |
| High-Energy Pop | Upbeat mainstream taste |
| Deep Intense Rock | High energy, dark tone |
| Angry Cardio | Conflicting preferences (high energy + melancholy mood) |
| Ghost Genre | Genre that does not exist in the catalog ("bossa nova") |
| Perfectly Average | Everything set to the middle — tests tie-breaking |

One experiment was also run: the mood rule was completely disabled to see what changed. The top score dropped from 4.91 to 2.95 and a country song appeared in a lofi playlist — proving that mood is the most important rule in the system.

The biggest surprise was the Angry Cardio profile. No song in the catalog is both very high energy and melancholy at the same time. The best score was only 2.94 out of 5.0, which correctly shows that the user's preferences cannot be satisfied with this data.

---

## 7. Intended Use and Non-Intended Use

**This system is designed for:**
- Classroom learning about how content-based recommenders work
- Experimenting with scoring weights and feature importance
- Understanding why real recommendation systems are more complex than they look

**This system should NOT be used for:**
- Real music recommendations for actual users
- Any application where someone's experience depends on the quality of results
- Evaluating real songs or real artists — all data is fictional
- Drawing conclusions about what makes music "good" or "popular"

---

## 8. Ideas for Improvement

1. **Group similar moods together.** Instead of treating "chill", "focused", and "calm" as completely different, create mood clusters. A chill user should still get partial credit for a focused song — they are close enough that a real listener would probably enjoy both.

2. **Add a diversity rule.** Right now the top 5 can be filled with songs from the same genre or even the same artist. A simple rule like "no more than 2 songs per genre in the top 5" would make results feel more varied and useful.

3. **Score tempo.** Every song has a `tempo_bpm` value but the system never uses it. Adding a tempo range preference (like "I like songs between 70 and 90 BPM") would give the system a better handle on the difference between a slow ballad and a mid-tempo groove that happen to share the same energy score.

---

## 9. Personal Reflection

My biggest learning moment was realizing how much a single number can dominate a system. I assumed the recommendations would feel balanced across all five rules, but once I ran the mood experiment and watched a country song appear in a lofi playlist, it clicked — 40% of the score was riding on one label match. That made me think differently about every app I use. When Spotify recommends something that feels completely off, I now wonder which feature silently scored too high.

Claude Code helped me move a lot faster than I expected. I used them to generate the initial scoring logic, write out the algorithm recipe, and debug why certain songs were ranking in unexpected places. The moments I had to double-check were when the AI explained a score confidently but the actual numbers did not add up — I learned to always run the code myself and compare the output to what was predicted. The AI was great at explaining concepts but I still had to verify the math.

The most surprising thing was how much the system felt like a real recommender even with only 20 songs and five rules. When I ran the Chill Lofi profile and got Library Rain and Midnight Coding at the top, it genuinely felt correct — like the system understood what I wanted. It made me realize that "intelligence" in a recommendation is often just careful weighting. You do not need a neural network to make something feel smart; you just need the right features and the right priorities.

If I extended this project, I would try two things. First, I would add a feedback loop — let the user mark a recommendation as "good" or "skip," and use that to slowly adjust the weights over time. Second, I would replace exact mood matching with a similarity map so that "chill" and "focused" are treated as close neighbors instead of complete strangers. Those two changes alone would make the system feel much more like something a real person would actually want to use.
