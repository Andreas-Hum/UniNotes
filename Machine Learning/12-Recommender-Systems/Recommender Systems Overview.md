---
tags: [ml, recsys, index]
status: not-started
notebook: not-started
level:
reviewed:
---
# Recommender Systems Overview

> [!summary] In one sentence
> A recommender system learns from what people did (ratings, clicks, purchases) to **predict which items a user will like** (rating prediction) or to **produce a ranked list** of the best items for them (top-K recommendation).

## Intuition first

Picture a good bookshop owner. After a few visits they know you liked *Dune* and *The Martian*, they notice that other customers who bought those also loved *Project Hail Mary*, and they put it in your hands. That owner combines three kinds of knowledge:

1. **What the item is** (sci-fi, hard science, humour): this is *content-based* recommendation.
2. **What similar people liked**: this is *collaborative filtering*.
3. **What is popular right now**: the *non-personalised baseline*, which is surprisingly hard to beat.

A recommender system automates this for millions of users and millions of items. The core problem is a **huge, mostly empty table**: rows are users, columns are items, and almost every cell is unknown because each person has interacted with a tiny fraction of the catalogue. Every method below is a different way of guessing the empty cells, or more precisely of guessing *which empty cells are worth showing first*.

Two goals are worth separating early:
- **Rating prediction**: "how many stars would Alice give this film?" Measured with RMSE/MAE.
- **Top-K recommendation**: "which 10 items should go on Alice's home page?" Only the order of the top few matters. Measured with ranking metrics like Recall@K and NDCG@K ([[Evaluating Recommenders]]).

Modern systems care mostly about the second.

## Feedback types

| Explicit | Implicit |
|---|---|
| ratings, likes, reviews | clicks, views, purchases, dwell time |
| sparse but clear | abundant but noisy; no true negatives |

**Explicit** feedback is a deliberate statement of preference (5 stars, thumbs down). It is clear but rare, because most people never rate anything.

**Implicit** feedback is inferred from behaviour (played a song, opened an article, added to cart). It is plentiful, but:
- it is **noisy**: a click can be a mis-tap, a long dwell time can be a forgotten tab;
- there are **no true negatives**: a missing interaction is ambiguous. The user may dislike the item, or may simply never have seen it. This is why implicit methods treat missing entries as *weak* negatives with low confidence, rather than as zeros.

A common trick (Hu, Koren & Volinsky) turns a raw count $r_{ui}$ (e.g. plays) into a binary **preference** $p_{ui}=\mathbb 1[r_{ui}>0]$ and a **confidence** $c_{ui}=1+\alpha r_{ui}$. More plays means more confidence that the user really likes it; zero plays still has confidence $1$, a weak "probably not". Details in [[Collaborative Filtering and Matrix Factorization]].

## Families of approaches

| Approach | Idea | Note |
|---|---|---|
| Popularity / non-personalised | recommend top items | strong baseline |
| **Content-based** | match item features to the user profile | [[Content-Based and Hybrid Recommenders]] |
| **Collaborative filtering** | similar users like similar items | [[Collaborative Filtering and Matrix Factorization]] |
| **Matrix factorization** | latent user and item vectors | same note |
| **Hybrid** | combine content and CF | handles cold start |
| **Deep / two-tower / sequential** | neural encoders, transformers | [[Deep Learning Recommenders]] |
| **Multimodal** | fuse image/text/audio item features with interactions | [[Multimodal Recommender Systems]] |
| **Graph-based** | user–item bipartite graph, GNNs | [[Graph Neural Networks]], [[Link Prediction]] |
| **Bandits / RL** | explore vs exploit online | [[RL Basics and MDPs]] |

How to pick, roughly:
- **No interaction data yet?** Popularity, content-based or knowledge-based rules.
- **Items appear faster than they collect interactions** (news, fashion seasons)? Content-based, hybrid or multimodal, because pure CF cannot score an item nobody has touched.
- **Dense logs and order matters** (next song, next video)? Sequential deep models.
- **You must learn online which option works** (which banner to show)? Bandits.

## Industrial architecture (multi-stage)

![A catalogue of items narrowing through retrieval, ranking and re-ranking](../../Attachments/ML%20Animations/Recommender%20Systems%20Overview%20-%20multi-stage%20funnel.gif)

*Watch the item count shrink at each stage, and how the re-ranker swaps a same-colour top list for a diverse final slate.*

1. **Candidate generation / retrieval** — thousands from millions (two-tower + approximate nearest neighbours).
2. **Ranking / scoring** — rich model (GBDT, DLRM, Wide & Deep) predicts CTR or watch time.
3. **Re-ranking** — diversity, freshness, business rules, fairness.

Why not one big model that scores everything? **Latency.** Suppose a ranking model costs $0.02$ ms per item and the catalogue has $10^8$ items: scoring all of them takes $10^8\times 2\cdot10^{-5}\,\text{s}=2000$ s per request. A page must load in about 100 ms. So each stage is optimised for something different:
- retrieval: **recall**, cheaply (do not lose good items), using a model whose item vectors can be precomputed and indexed;
- ranking: **precision** on a few hundred candidates, with expensive cross features;
- re-ranking: **business goals** on the final list. Diversity rules belong here because they are properties of the *whole list*, which only exists at the end.

## The math, step by step

A few symbols used throughout the recsys notes:
- $U$ users, $I$ items; $r_{ui}$ the feedback of user $u$ on item $i$.
- $\Omega$ = the set of observed $(u,i)$ pairs. **Density** $=|\Omega|/(|U|\cdot|I|)$; sparsity is $1-$density. Real systems are often below 0.1% dense.
- $\hat r_{ui}$ = the model's predicted score.

**Bias baseline.** Before personalising, explain ratings with a global mean plus "this user is generous" and "this item is good" offsets:
$$\hat r_{ui}=\mu+b_u+b_i,\qquad \min_{\mu,b}\sum_{(u,i)\in\Omega}(r_{ui}-\mu-b_u-b_i)^2+\lambda\Big(\sum_u b_u^2+\sum_i b_i^2\Big).$$
In words: fit the observed ratings with additive offsets, and shrink the offsets toward zero ($\lambda$) so a user with one rating does not get an extreme bias. It is [[Linear Regression|ridge regression]] on one-hot user and item columns. Matrix factorization adds a personalised term $p_u^\top q_i$ on top of exactly this.

**Damped (Bayesian) mean.** Ranking by raw mean rating puts an item with a single 5-star rating on top. Shrink each item's mean toward the global mean $\mu$ with $m$ pseudo-ratings:
$$\tilde r_i=\frac{\sum_{u\in\Omega_i}r_{ui}+m\,\mu}{n_i+m}.$$
Few ratings → close to $\mu$; many ratings → close to the item's own mean.

## Worked example

Global mean $\mu=3.5$, pseudo-count $m=5$.
- Item X: ratings 5, 5. Raw mean $5.0$. Damped: $\frac{10+5\cdot3.5}{2+5}=\frac{27.5}{7}\approx3.93$.
- Item Y: ratings 4, 5, 4, 4, 5, 4, 5, 4 (sum 35, $n=8$). Raw mean $4.375$. Damped: $\frac{35+17.5}{13}\approx4.04$.

Raw mean ranks X first; the damped mean ranks Y first because eight consistent ratings are stronger evidence than two. This "popularity with shrinkage" is a legitimate baseline every fancy model must beat.

## Core challenges

Cold start · sparsity · popularity bias · feedback loops · scalability · diversity/serendipity · privacy.

- **Cold start**: a new user or new item has no history, so CF has nothing to work with. Content features, onboarding questions and exploration help.
- **Sparsity**: with 0.05% of cells observed, similarity estimates between users are based on very few co-rated items.
- **Popularity bias / long tail**: a few items get most interactions (e.g. the top 20% of items often collect well over half the clicks). Models learn to recommend the head, and niche items starve. The **Gini coefficient** of item popularity measures this concentration (0 = equal, near 1 = one item gets everything).
- **Feedback loops**: users can only click what was shown, and tomorrow's model trains on today's clicks. Popular items get shown more, so they get clicked more, so they look even better. Offline metrics on such logs can improve while real quality drops. Mitigations: exploration (e.g. ε-greedy bandits), logging propensities and using off-policy evaluation, diversity constraints.
- **Scalability**: millions of users × millions of items, answered in milliseconds; hence the multi-stage pipeline.
- **Diversity / serendipity**: a list of ten near-identical items is accurate but useless. **Catalogue coverage** (share of items that appear in at least someone's top-K) is a quick sanity check.
- **Privacy**: interaction logs are personal data.

Evaluation: [[Evaluating Recommenders]]. Learning material: [[Recommender Systems Resources]].

> [!tip] Recommender recipe
> Start with popularity → item-kNN → implicit MF (ALS/BPR) → LightGBM ranker with features → two-tower / sequential transformer.

Each step should beat the previous one on a proper temporal split before you add complexity.

## Common confusions

- **"No click means the user dislikes it."** → With implicit feedback a missing interaction is mostly *not seen*. Treat it as a weak negative or sample it as a negative, never as a confident zero.
- **"Higher RMSE accuracy means better recommendations."** → Users see a ranked list. A model can predict stars well on average and still put the wrong items in the top 10. Use ranking metrics for top-K.
- **"Popularity is too dumb to bother with."** → It is often within a few percent of complex models, and it is the honest baseline every paper should report.
- **"One model should do everything."** → At catalogue scale you need a cheap high-recall retriever followed by an expensive precise ranker.
- **"Offline gains will show up in the A/B test."** → Feedback loops and biased logs mean offline and online can disagree; online testing is the final judge.

## Check yourself

> [!question]- Why does implicit feedback have "no true negatives"?
> Because a missing interaction is ambiguous: the user may dislike the item, or may never have been shown it. Only explicit negative signals (thumbs down, skip after 2 seconds) are real negatives.

> [!question]- What is each stage of the industrial pipeline optimised for?
> Retrieval: recall at very low cost per item (millions → thousands). Ranking: precision with rich features on a few hundred candidates. Re-ranking: list-level goals such as diversity, freshness, fairness and business rules.

> [!question]- A new fashion shop renews 30% of its items every season. Which family suits it, and why not pure CF?
> Content-based, hybrid or multimodal (images and text of the items), because new items have no interactions and pure CF cannot score them until people interact with them.

> [!question]- What does the damped mean protect against?
> Items with very few ratings getting extreme average scores. It pulls their mean toward the global mean until enough evidence accumulates.

> [!question]- Describe the feedback loop in one sentence.
> The recommender decides what users see, users can only click what they see, and those clicks train the next recommender, so early popularity gets amplified regardless of true quality.

## Practice

[Recommender Systems Overview - Exercises](Recommender%20Systems%20Overview%20-%20Exercises.ipynb): explicit vs implicit signals, sparsity, damped means, preference/confidence, the long tail, a latency budget, then popularity, coverage, the bias baseline, the Gini coefficient, a feedback-loop simulation and ε-greedy exploration in code.

## Learn more

- [[Recommender Systems Resources]] for the curated list of courses, books and libraries.
- [Google Machine Learning: Recommendation Systems course](https://developers.google.com/machine-learning/recommendation) (free, covers candidate generation, scoring and re-ranking).
