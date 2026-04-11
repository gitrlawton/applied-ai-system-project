# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

---

## 3. How the Model Works

Explain your scoring approach in simple language.

Prompts:

- What features of each song are used (genre, energy, mood, etc.)
- What user preferences are considered
- How does the model turn those into a score
- What changes did you make from the starter logic

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

---

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

Prompts:

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

### One Weakness

The catalog contains three lofi songs but only one each of blues, soul, reggae, classical, and several other genres. Because the genre bonus is awarded per matching song, a lofi listener has three opportunities to earn it while a blues listener has exactly one — meaning four of their top five results will always be genre mismatches regardless of how well their other preferences align. This is not a flaw in the scoring math itself, but a structural bias baked into the data: the catalog was built to reflect a narrow slice of listening habits, and the recommender faithfully amplifies that imbalance. In practice this means the system works best for users whose taste already overlaps with the most represented genres, and quietly under-serves everyone else. A fairer design would either balance the catalog or normalize the genre bonus by the number of songs available in each genre so that rare-genre listeners are not penalized for catalog gaps outside their control.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

I tested eight different user profiles — three normal ones like a pop listener, a lofi listener, and a rock listener, plus five "trick" profiles designed to break the system. The normal profiles worked about how I expected, with the right genres showing up at the top. What surprised me was how hard it was to actually fool the scoring. When I gave the system a profile that wanted high energy but a sad mood, the sad song still won because matching both the genre and the mood was worth so many points that nothing else could beat it. The most interesting result was when I set all the music preferences to match lofi songs but told the system the user wanted metal — the metal song never showed up in the top five at all, because its actual sound was so different from what the numbers described. That made me realize the genre label matters a lot less than I thought when the numbers are pulling hard in the other direction.

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

---

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps
