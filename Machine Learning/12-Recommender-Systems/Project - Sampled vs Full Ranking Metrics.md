---
tags: [ml, project, evaluation, recommender-systems]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Sampled vs Full Ranking Metrics

> [!summary] In one sentence
> Measure hit@10 for random, popularity and SVD recommenders on MovieLens both against 99 sampled negatives and against the full catalogue, and see how sampling inflates scores and hides the gaps between models.

**Notebook:** [Project - Sampled vs Full Ranking Metrics](Project%20-%20Sampled%20vs%20Full%20Ranking%20Metrics.ipynb) · topic: [[Evaluating Recommenders]] · all projects: [[Projects Overview]]

## What you build
1. `hit_full`: rank the held-out item against every unseen item.
2. `hit_sampled`: rank it against 99 random unseen items.

## Reference results (solution, laptop CPU)
| model | sampled HR@10 | full HR@10 |
|---|---|---|
| random | 0.080 | 0.000 |
| popularity | 0.624 | 0.039 |
| SVD (k = 64) | 0.675 | 0.085 |

On the full ranking SVD is **2.2×** better than popularity; on the sampled metric it looks only 8 % better.

## Check yourself
> [!question]- Why does a random recommender get ≈ 10 % sampled HR@10?
> With 1 positive and 99 negatives, a random score puts the positive in the top 10 of 100 with probability 10/100.

> [!question]- Why can sampled metrics change which model looks best?
> Sampling mostly measures how well the model separates the positive from *easy* random items. The full ranking is decided by the *hard* items near the top, which sampling rarely draws.

## Learn more
- [Krichene & Rendle – On Sampled Metrics for Item Recommendation (KDD 2020)](https://doi.org/10.1145/3394486.3403226)

---
Back to [[00 - Machine Learning Index]].
