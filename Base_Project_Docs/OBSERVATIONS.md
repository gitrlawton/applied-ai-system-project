## Phase 4, Step 3 - Weight Shift Experiment

**Change made:** genre weight halved (3.0 → 1.5), energy weight doubled (2.5 → 5.0). Max possible score shifted from 13.0 to 14.0.

**Verdict: just different, not more accurate** — and in most cases, worse. Here's what the weight shift exposed:

**Energy-Sad Clash** — Broken Hallelujah holds #1 but its margin collapsed from 10.43 → 10.08, while the gap to #2 closed dramatically (was 3.7 points, now only 0.9). High-energy wrong-mood songs are dangerously close to overtaking the correct match.

**Impossible Combo** — Iron Curtain's score jumped from 8.92 → 11.09. With energy worth 5.0 points, a strong energy match now dominates almost everything else. The ranking order didn't change but the scores inflated significantly.

**Lofi Numbers, Metal Label** — The most telling change. Previously Iron Curtain was just missing from the top 5. Now the lofi songs score even higher (Focus Flow: 7.89 → 10.39) because energy carries so much more weight. The genre label "metal" is now almost meaningless — 1.5 points can't compete with a near-perfect 5.0 energy score.

**Lone Wolf Genre** — The perfect score is now 14.00/13.0, which means the hardcoded `/ 13.0` display in `main.py` is wrong. The `MAX_SCORE` constant in `recipe.py` updates automatically, but the display label doesn't reference it.

**The core problem:** halving genre from 3.0 → 1.5 means a perfect energy match (+5.0) can now easily overpower a genre mismatch (−1.5). A metal song with the right energy profile will beat a lofi song with the wrong energy — which contradicts the original design goal stated in `recipe.py`: *"a wrong-genre song can never outscore a right-genre song purely on numeric similarity."* That guarantee is now broken.

---

## Scoring Logic Filter Bubble / Biases

### 1. The Energy Gap Formula Never Goes Negative — But It Can Reward the Wrong Songs

```python
pts = WEIGHTS["energy"] * (1 - abs(song["energy"] - user_prefs["target_energy"]))
```

Both `song["energy"]` and `target_energy` are bounded 0–1, so the difference is always 0–1 and the score never goes negative. But the formula is **symmetric** — being 0.3 above the target penalizes equally to being 0.3 below it. A low-energy user targeting 0.28 gets the same penalty from a 0.58 song as from a 0.98 song, even though those feel completely different. There's no concept of direction, only distance.

---

### 2. Catalog Representation Bias — Lofi Users Are Favored

Count the songs per genre:

| Genre | Songs |
|---|---|
| lofi | 3 |
| pop | 2 |
| happy (mood) | 2 |
| chill (mood) | 3 |
| Everything else | 1 each |

A lofi user gets **3 chances** to earn the genre bonus. A blues, reggae, soul, metal, or classical user gets **1 chance** — meaning 4 of their top 5 results will always be genre mismatches. The system structurally over-serves lofi listeners and under-serves everyone else.

---

### 3. Binary Mood Matching Has No Gradient

```python
if song["mood"] == user_prefs["mood"]:
    pts = WEIGHTS["mood"]
else:
    pts = 0.0
```

`"chill"` vs `"relaxed"` scores exactly the same as `"chill"` vs `"angry"` — zero either way. These moods are emotionally close neighbors, but the system treats them as equally wrong. A `"focused"` user has only one song that can ever earn the mood bonus (Focus Flow). A `"chill"` user has three.

---

### 4. "indie pop" Is a Separate String From "pop"

The catalog has `genre="indie pop"` for Rooftop Lights, but user profiles use `genre="pop"`. Because genre matching is exact string equality, an indie pop fan who enters `"indie pop"` gets only 1 genre match available in the entire catalog. If they type `"pop"` they miss that song entirely and only get Sunrise City and Gym Hero. There's no genre hierarchy — pop is not a parent of indie pop in the system's view.

---

### 5. The Catalog Has a "Dead Zone" in the Middle

Looking at energy values across all 20 songs:

- **Low cluster (0.18–0.45):** 10 songs — classical, folk, ambient, blues, reggae, lofi ×3, jazz, soul, country
- **High cluster (0.75–0.98):** 6 songs — synthwave, indie pop, pop, rock, pop, edm, metal
- **Middle (0.50–0.74):** only 4 songs — r&b (0.55), hip-hop (0.68), synthwave (0.75), indie pop (0.76)

A user targeting `energy=0.62` — a perfectly reasonable "moderate energy" preference — has almost nothing close to them. The two nearest songs (r&b at 0.55, hip-hop at 0.68) are still 0.07–0.08 away while low-energy users have 10 songs clustered tightly around them.

---

### 6. The `UserProfile` Dataclass and `score_song` Are Inconsistent

The OOP `UserProfile` stores acoustic preference as a **boolean** (`likes_acoustic: bool`), while `score_song` expects a **float** (`target_acousticness: float`). If the `Recommender` class ever gets fully implemented, this mismatch will either crash or silently produce wrong scores — a boolean `True` passed as a float becomes `1.0`, `False` becomes `0.0`, with nothing in between.

---

### 7. The `/ 13.0` Display Is Now Wrong

Since the weight shift, `MAX_SCORE = sum(WEIGHTS.values()) = 14.0`, but `main.py` still hardcodes `/ 13.0` in the output. Lone Wolf Genre already showed a score of `14.00 / 13.0`. The fix is to import and use `MAX_SCORE` from `recipe.py` rather than a magic number.

---

### 8. No Diversity Enforcement Creates a Real Filter Bubble

`recommend_songs` sorts by score and returns the top k — nothing more. For a strong lofi profile, all five results can be lofi songs. For a strong low-energy profile, every result clusters at the bottom of the energy scale. The system never asks "are these results too similar to each other?" A real recommender would introduce a diversity penalty to ensure the top 5 aren't all the same genre, mood, or energy tier.
