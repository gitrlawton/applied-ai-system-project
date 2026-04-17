# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

This system is designed to suggest songs from a small catalog based on a user's stated preferences — things like their favorite genre, mood, and how energetic they want the music to feel. It assumes the user already knows what they like and can describe it upfront. It is built for classroom exploration, not for real-world use. It would not work well as an actual product because it relies on a hand-built catalog of only 20 songs and requires the user to fill in very specific preference values that most people would not naturally think about.

---

## 3. How the Model Works

Every song in the catalog gets a score based on how closely it matches the user's preferences. The system looks at seven things: genre, mood, energy level, emotional brightness (valence), how acoustic or electronic it sounds, tempo, and danceability. Genre and mood are all-or-nothing — a match earns full points, a mismatch earns zero. The other five features are scored on a sliding scale where a perfect match earns the full weight and a big difference earns close to nothing. All seven scores get added up and the top five songs by total score are returned as recommendations. The scoring weights were tuned so that genre carries the most influence, followed by energy, then mood, and the rest are secondary.

---

## 4. Data

The catalog has 20 songs spanning 17 genres including pop, lofi, rock, jazz, metal, classical, folk, blues, r&b, hip-hop, ambient, synthwave, edm, country, soul, reggae, and indie pop. Moods include happy, chill, intense, focused, relaxed, melancholic, peaceful, nostalgic, romantic, moody, sad, euphoric, and angry. The data was not pulled from a real music service — it was hand-built for this project, which means it reflects a narrow and specific slice of music taste. Some genres like lofi and pop have multiple songs while most others have only one, and several common genres like R&B, country, and folk are underrepresented. There are also no songs that blend genres or sit between moods, which limits how well the system handles listeners with mixed or evolving taste.

---

## 5. Strengths

The system works best when a user's preferences line up clearly with one of the well-represented genres in the catalog. A lofi listener, a pop listener, or a jazz listener all got results that felt accurate and made intuitive sense. The scoring also handles extreme preferences well — a workout profile asking for very high energy and fast tempo consistently surfaced the right songs at the top. The explain feature was another strength: because every score is broken down by feature, it is always clear exactly why a song ranked where it did, which is something most real recommenders cannot offer.

---

## 6. Limitations and Bias

The catalog contains three lofi songs but only one each of blues, soul, reggae, classical, and several other genres. Because the genre bonus is awarded per matching song, a lofi listener has three opportunities to earn it while a blues listener has exactly one — meaning four of their top five results will always be genre mismatches regardless of how well their other preferences align. This is not a flaw in the scoring math itself, but a structural bias baked into the data: the catalog was built to reflect a narrow slice of listening habits, and the recommender faithfully amplifies that imbalance. In practice this means the system works best for users whose taste already overlaps with the most represented genres, and quietly under-serves everyone else. A fairer design would either balance the catalog or normalize the genre bonus by the number of songs available in each genre so that rare-genre listeners are not penalized for catalog gaps outside their control.

---

## 7. Evaluation

I tested eight different user profiles — three normal ones like a pop listener, a lofi listener, and a rock listener, plus five "trick" profiles designed to break the system. The normal profiles worked about how I expected, with the right genres showing up at the top. What surprised me was how hard it was to actually fool the scoring. When I gave the system a profile that wanted high energy but a sad mood, the sad song still won because matching both the genre and the mood was worth so many points that nothing else could beat it. The most interesting result was when I set all the music preferences to match lofi songs but told the system the user wanted metal — the metal song never showed up in the top five at all, because its actual sound was so different from what the numbers described. That made me realize the genre label matters a lot less than I thought when the numbers are pulling hard in the other direction.

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

The first thing I would change is adding a diversity rule so the top five results cannot all come from the same genre, allowing the user to be introduced to new genres. Right now a strong lofi profile can return three lofi songs in a row. I would also replace the binary mood matching with a similarity scale so that "chill" and "relaxed" are treated as closer to each other than "chill" and "angry" — right now the system treats any mood mismatch as equally bad. Lastly, I would expand the catalog significantly and balance the number of songs per genre so that niche-genre listeners are not structurally disadvantaged from the start.

---

## 9. Personal Reflection

Building this made me realize how much work goes into deciding what a "good" recommendation even means. I assumed the hardest part would be writing the scoring logic, but the hardest part was actually choosing the weights — small changes to a single number could completely change which songs showed up at the top. The most surprising thing I discovered was that a song can score well for all the wrong reasons: a metal song could rank highly for a lofi listener just because its energy and tempo happen to be in the right range.

The biggest learning moment was stress-testing the system and seeing how changing the weights affected the recommended songs. It was cool to see that a simple algorithm recipe could still feel like a real recommendation when everything lined up. If I kept working on this I would try implementing user feedback, to help strengthen their personal preferences, improve the recommendation algorithm, and what gets recommended to them in the future.
