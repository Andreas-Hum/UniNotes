---
tags: [ml, recsys]
---
# Content-Based and Hybrid Recommenders

> [!summary] In one sentence
> Content-based recommenders describe every item by its features and recommend items that resemble what the user already liked, and hybrids combine this with collaborative filtering so each covers the other's blind spots (especially cold start).

## Intuition first

A content-based recommender behaves like a friend who knows *what kind of thing* you like: "You enjoyed two space operas with robots, here is another space opera with robots." It never asks what other people did. It only needs:

1. a description of each item (genres, tags, words in the synopsis, an image embedding);
2. a summary of the user's taste in the same feature space (the **profile**);
3. a way to compare the two (usually cosine similarity).

Because it reasons from item features, it can recommend a film released *this morning* that nobody has watched yet: something collaborative filtering cannot do. The price: it will rarely surprise you. If you have only liked space operas, it will only find space operas.

**Hybrids** exist because content-based and collaborative methods fail in opposite places. CF is great at surprising, "people like you also loved…" discoveries but is blind to new items. Content-based handles new items but is narrow. Mixing them is standard in practice.

## Content-based
1. Represent items with features: genre, tags, TF-IDF of text, image/text embeddings ([[Text Representations]]).
2. Build a user profile: weighted average of liked item vectors, or train a per-user classifier ([[Logistic Regression]], [[Naive Bayes]]).
3. Score by similarity (cosine).

+ no cold-start for new items, explainable ("because you liked X")
− over-specialisation (filter bubble), needs good features, new users still cold

![Liked items combine into a profile vector; candidates are scored by the angle to it; a cone shows the filter bubble](../../Attachments/ML%20Animations/Content-Based%20and%20Hybrid%20Recommenders%20-%20profile%20and%20cosine%20scores.gif)

*Watch the profile $\mathbf u$ appear as the rating-weighted average of the two liked films, then notice that cosine only cares about angle: C wins even though A has larger feature values. The shaded cone is where all future recommendations will come from.*

## The math, step by step

**Item vectors.** Each item $i$ is a vector $\mathbf x_i\in\mathbb R^d$: genre flags (Action, Comedy, …), TF-IDF weights of its description, or an embedding from a text/image model.

**TF-IDF** weights a word by how often it appears in this item and how *rare* it is across items:
$$\text{tf-idf}(t,d)=\mathrm{tf}(t,d)\cdot\mathrm{idf}(t),\qquad \mathrm{idf}(t)=\ln\frac{N}{\mathrm{df}(t)},$$
with $\mathrm{tf}$ the count of term $t$ in document $d$, $N$ the number of documents and $\mathrm{df}(t)$ the number of documents containing $t$. A word in every description ("film") gets $\mathrm{idf}=0$: it does not distinguish anything. scikit-learn uses a smoothed variant $\mathrm{idf}(t)=\ln\frac{1+N}{1+\mathrm{df}(t)}+1$ and then L2-normalises each row.

**Profile, option 1: weighted average of liked items.**
$$\mathbf u=\frac{\sum_{i\in L_u}r_{ui}\,\mathbf x_i}{\sum_{i\in L_u}r_{ui}},$$
where $L_u$ are the items the user liked (e.g. rating $\ge4$). A 5-star film pulls the profile harder than a 4-star one.

**Profile, option 2: use dislikes too (Rocchio-style).** Centre the ratings by the user's mean:
$$\mathbf u=\sum_i(r_{ui}-\bar r_u)\,\mathbf x_i.$$
Above-average items push the profile toward their features; below-average items push it *away*. Now a hated romance actively lowers the score of other romances.

**Scoring.** Cosine similarity between profile and candidate:
$$\mathrm{score}(u,i)=\cos(\mathbf u,\mathbf x_i)=\frac{\mathbf u^\top\mathbf x_i}{\lVert\mathbf u\rVert\,\lVert\mathbf x_i\rVert}.$$
It measures the *angle* only, so an item with fewer tags is not penalised for having a short vector.

**Profile, option 3: a per-user classifier.** Treat the user's liked/not-liked items as a labelled dataset and fit [[Logistic Regression]] ($P(\text{like})=\sigma(w^\top\mathbf x+b)$, the weights $w$ *are* the profile and can be negative) or Bernoulli [[Naive Bayes]] with Laplace smoothing $P(x_j=1\mid c)=\frac{n_{cj}+1}{n_c+2}$. Useful when the user has enough labelled history.

## Worked example

**Profile and cosine** (the numbers from the animation). Features are (action, romance). Liked: $\mathbf x_1=(0.9,0.2)$ with 5 stars, $\mathbf x_2=(0.7,0.45)$ with 4 stars.
$$\mathbf u=\frac{5(0.9,0.2)+4(0.7,0.45)}{9}=\frac{(7.3,\,2.8)}{9}\approx(0.81,\,0.31),\qquad\lVert\mathbf u\rVert\approx0.87.$$
Candidate C $=(0.55,0.12)$: $\mathbf u^\top\mathbf x_C\approx0.81\cdot0.55+0.31\cdot0.12\approx0.483$, $\lVert\mathbf x_C\rVert\approx0.563$, so $\cos\approx\frac{0.483}{0.87\cdot0.563}\approx0.99$.
Candidate A $=(0.85,0.55)$ gives $\approx0.98$ and B $=(0.35,0.85)$ gives $\approx0.69$. Recommend C, then A.

**TF-IDF.** Three descriptions: $d_1$ = "robots fight robots", $d_2$ = "robots love", $d_3$ = "love story". With $N=3$: "robots" appears in 2 documents, so $\mathrm{idf}=\ln(3/2)\approx0.41$ and $\text{tf-idf}(\text{robots},d_1)=2\cdot0.41=0.81$. "fight" appears in 1 document: $\mathrm{idf}=\ln3\approx1.10$, so one occurrence of the rare word "fight" outweighs two of "robots".

**Score scales in a weighted hybrid.** Three items; CF scores $(0.9,0.3,0.6)$, content scores $(2,9,6)$. Blend $0.5\cdot\text{CF}+0.5\cdot\text{content}$ on raw scores: $(1.45,4.65,3.3)$, so item 2 wins purely because content scores live on a larger scale. Min-max normalise each model first: CF $\to(1,0,0.5)$, content $\to(0,1,0.57)$, blend $\to(0.5,0.5,0.54)$, and now item 3, decent on both, wins. **Always put scores on a common scale before blending.**

## Knowledge-based / constraint-based
Explicit requirements (budget, size) — cars, real estate.

Why not CF here? People buy a car or a flat rarely (no history, every user is cold), items are unique and short-lived (each listing sells once), and hard constraints matter more than taste ("max €300k, 3 rooms, near the station"). The system filters by constraints first, then ranks what is left, often with an interactive "show me cheaper / bigger" critique loop.

## Hybrids
| Type | Example |
|---|---|
| Weighted | blend CF and content scores |
| Switching | content for new items, CF otherwise |
| Feature augmentation | CF output as a feature for a ranker |
| Model-level | LightFM, factorization machines, two-tower with side features ([[Deep Learning Recommenders]]) |

The *why* of each:
- **Weighted**: $s=\alpha\,s_{\text{CF}}+(1-\alpha)\,s_{\text{content}}$. If the two models make *independent* errors, averaging cancels part of the noise, so the best $\alpha$ is usually strictly between 0 and 1. Tune $\alpha$ on validation data and normalise scales first.
- **Switching**: use content while an item has fewer than, say, 10 interactions, then switch to CF. Simple, but the two score types still need calibration if they are ranked in the same list.
- **Feature augmentation**: a GBDT ranker gets the MF score, the content similarity, popularity, recency… as input features and learns how to combine them per context.
- **Model-level**: one model learns from IDs *and* features. In LightFM, an item's embedding is the sum of the embeddings of its features (including its ID), so a new item with known tags gets a sensible embedding immediately.

## Diversity: fighting the filter bubble

Over-specialisation is measurable. **Intra-list similarity** of a list $L$ is the mean pairwise similarity
$$\mathrm{ILS}(L)=\frac{2}{|L|(|L|-1)}\sum_{a<b}\mathrm{sim}(a,b),$$
lower = more diverse. **Maximal Marginal Relevance (MMR)** re-ranks greedily, trading relevance against similarity to what is already in the list:
$$i^\star=\arg\max_{i\notin L}\ \lambda\,\mathrm{rel}(i)-(1-\lambda)\max_{j\in L}\mathrm{sim}(i,j).$$
$\lambda=1$ is pure relevance; smaller $\lambda$ buys diversity at a small cost in relevance.

## Cold-start strategies
Onboarding questionnaires, popularity by segment, content/meta features, bandit exploration ([[Q-Learning and Policy Gradients]]), transfer from other domains.

| Strategy | Helps new users | Helps new items | Main downside |
|---|---|---|---|
| Onboarding questionnaire | yes | no | friction, users skip it |
| Popularity by segment (country, age, device) | yes | no | not personal, reinforces the head |
| Content / meta features | partly (from a few clicks) | yes | needs good features |
| Bandit exploration | yes | yes | costs some bad impressions while learning |
| Transfer from other domains | yes | sometimes | needs linked accounts or shared features |

## Common confusions

- **"Content-based means no data is needed."** → It needs no data about *other users*, but it still needs some history for *this* user. New users are cold for content-based too.
- **"Cosine prefers items with more features."** → Cosine ignores vector length; only direction matters. (Plain dot product does prefer long vectors.)
- **"A weighted hybrid can blend raw scores."** → Different models output different scales; the larger scale silently dominates. Normalise or calibrate first.
- **"Content-based gives serendipity if the features are good."** → It can only find items near the profile in feature space. Unexpected-but-loved items come from CF ("people like you also liked…") or explicit exploration.
- **"Knowledge-based is just content-based with filters."** → It is driven by explicit user requirements, works with zero history, and is used precisely where taste-based methods break (rare, high-stakes purchases).

## Check yourself

> [!question]- Why can a content-based recommender handle a brand-new item but not a brand-new user?
> The new item has features, so it can be compared with existing profiles immediately. The new user has no liked items, so there is no profile to compare against.

> [!question]- What changes when you build the profile with centred ratings $\sum_i(r_{ui}-\bar r_u)\mathbf x_i$?
> Disliked (below-average) items contribute with a negative weight, so their features are pushed out of the profile and similar items score lower. The plain average of liked items ignores dislikes completely.

> [!question]- Which hybrid type is "a GBDT ranker gets the MF score as one input feature"?
> Feature augmentation.

> [!question]- Why is the best blending weight in a weighted hybrid usually strictly between 0 and 1?
> When the two models make partly independent errors, a mix averages out noise that each has alone, so it beats either model on its own.

> [!question]- What does MMR do when $\lambda=0.5$?
> At each step it picks the item with the best balance of high relevance and low maximum similarity to the items already selected, producing a more diverse list than pure top-K.

## Practice

[Content-Based and Hybrid Recommenders - Exercises](Content-Based%20and%20Hybrid%20Recommenders%20-%20Exercises.ipynb): profiles and cosine scores by hand, a centred profile, TF-IDF, a per-user logistic model, score scales in a weighted hybrid; then TF-IDF like sklearn, content-based top-K, Bernoulli Naive Bayes, switching and weighted hybrids, intra-list similarity and MMR re-ranking in code.

## Learn more

See [[Recommender Systems Overview]].
- [scikit-learn: TF-IDF term weighting](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting)
- [LightFM documentation](https://making.lyst.com/lightfm/docs/home.html) (hybrid matrix factorization with item and user features)
- [Google ML course: Content-based filtering](https://developers.google.com/machine-learning/recommendation/content-based/basics)
- [[Recommender Systems Resources]]
