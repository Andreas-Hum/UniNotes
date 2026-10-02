---
tags: [ml, recsys, index]
---
# Recommender Systems Overview

Goal: predict which items a user will like (rating prediction) or produce a ranked list (top-K recommendation).

## Feedback types
| Explicit | Implicit |
|---|---|
| ratings, likes, reviews | clicks, views, purchases, dwell time |
| sparse but clear | abundant but noisy; no true negatives |

## Families of approaches
| Approach | Idea | Note |
|---|---|---|
| Popularity / non-personalised | recommend top items | strong baseline |
| **Content-based** | match item features to the user profile | [[Content-Based and Hybrid Recommenders]] |
| **Collaborative filtering** | similar users like similar items | [[Collaborative Filtering and Matrix Factorization]] |
| **Matrix factorization** | latent user and item vectors | same note |
| **Hybrid** | combine content and CF | handles cold start |
| **Deep / two-tower / sequential** | neural encoders, transformers | [[Deep Learning Recommenders]] |
| **Graph-based** | user–item bipartite graph, GNNs | [[Graph Neural Networks]], [[Link Prediction]] |
| **Bandits / RL** | explore vs exploit online | [[RL Basics and MDPs]] |

## Industrial architecture (multi-stage)
1. **Candidate generation / retrieval** — thousands from millions (two-tower + approximate nearest neighbours).
2. **Ranking / scoring** — rich model (GBDT, DLRM, Wide & Deep) predicts CTR or watch time.
3. **Re-ranking** — diversity, freshness, business rules, fairness.

## Core challenges
Cold start · sparsity · popularity bias · feedback loops · scalability · diversity/serendipity · privacy.

Evaluation: [[Evaluating Recommenders]]. Learning material: [[Recommender Systems Resources]].

> [!tip] Recommender recipe
> Start with popularity → item-kNN → implicit MF (ALS/BPR) → LightGBM ranker with features → two-tower / sequential transformer.
