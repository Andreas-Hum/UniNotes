---
tags: [ml, recsys, project]
---
# Project - MovieLens Recommender

> [!summary] In one sentence
> A build-along project: start with a popularity list on MovieLens, then replace it five times (matrix factorization → BPR → two-tower → multimodal with posters), measuring every model with the same split and metric so you can see what each idea actually buys.

## How to use this project
- Work through the milestones **in order**; each reuses the data split and `evaluate` function from the one before, and each notebook starts with the same setup cells so they also run on their own.
- Dataset: **MovieLens `ml-latest-small`** (about 100k ratings, 600 users, 9k movies) from [GroupLens](https://grouplens.org/datasets/movielens/). Small enough to train on a CPU in minutes.
- Treat ratings ≥ 4 as positives (implicit feedback) and split **by time, leave-last-out**: the latest positive per user is test, the one before it is validation. Tune on validation, touch test once per milestone at the end.
- Log one row per model in a results table (HR@10, NDCG@10, training time). The table is the deliverable.
- Notebooks are starters: setup, split and evaluation are done, the interesting parts are `TODO`s. Try before looking up solutions in the linked notes.

> [!warning] Evaluation honesty
> The starter `evaluate` ranks the held-out item against 99 sampled negatives. That is fast but can reorder models. Report **full-ranking** metrics for your final numbers (see [[Evaluating Recommenders]]).

## Milestones at a glance

| # | Model | New idea | Notebook |
|---|---|---|---|
| 1 | Popularity baseline | the number to beat | [M1](Project%20-%20MovieLens%20Recommender%20-%20M1%20Popularity%20Baseline.ipynb) |
| 2 | Matrix factorization | latent taste vectors | [M2](Project%20-%20MovieLens%20Recommender%20-%20M2%20Matrix%20Factorization.ipynb) |
| 3 | BPR | optimise ranking, not ratings | [M3](Project%20-%20MovieLens%20Recommender%20-%20M3%20BPR.ipynb) |
| 4 | Two-tower | features + fast retrieval | [M4](Project%20-%20MovieLens%20Recommender%20-%20M4%20Two-Tower.ipynb) |
| 5 | Multimodal | posters and text for cold items | [M5](Project%20-%20MovieLens%20Recommender%20-%20M5%20Multimodal%20with%20Posters.ipynb) |

## Milestone 1 · Popularity baseline
**Goals**
- Load the data, build the time-based split and the `evaluate` function (HR@10, NDCG@10).
- Score by training popularity and report numbers; also evaluate a random scorer to check the evaluator (expect HR@10 ≈ 0.10 with 99 negatives).
- Implement one variant: time-decayed popularity, per-genre popularity, or Bayesian-average rating.

**Hints**
- Never count popularity on validation or test rows (leak).
- Break score ties randomly; with an optimistic tie rule, a constant scorer looks perfect.
- Print the top 10 titles. A sensible-looking list of blockbusters that still wins is normal on MovieLens.

**Notebook:** [M1](Project%20-%20MovieLens%20Recommender%20-%20M1%20Popularity%20Baseline.ipynb)
**Read:** [[Recommender Systems Overview]] · [[Evaluating Recommenders]] · [[Model Evaluation and Metrics]]

## Milestone 2 · Matrix factorization
**Goals**
- Implement biased MF with SGD from scratch and check RMSE on held-out ratings.
- Switch to implicit feedback (ALS, or the `implicit` library) and evaluate with the ranking metric from M1.
- Inspect the learned item vectors: nearest neighbours of a movie you know.

**Hints**
- Initialise factors with small noise (std ≈ 0.1); zeros never move.
- If MF loses to popularity, raise the regularisation and add item biases first; popularity is mostly an item-bias effect.
- Sweep the number of factors (8, 32, 128) and plot HR@10 against it.

**Notebook:** [M2](Project%20-%20MovieLens%20Recommender%20-%20M2%20Matrix%20Factorization.ipynb)
**Read:** [[Collaborative Filtering and Matrix Factorization]] · [[Linear Algebra for ML]] · [[Gradient Descent]]

## Milestone 3 · BPR
**Goals**
- Implement the BPR loss $-\ln\sigma(\hat x_{ui}-\hat x_{uj})$ with a negative sampler in PyTorch.
- Train BPR-MF and compare to M2 on the same split.
- Run at least one ablation: popularity-biased negatives, several negatives per positive, or no item bias.

**Hints**
- Sampled negatives must exclude the user's training positives; vectorise this with a rejection-sampling loop on the batch, not per row in Python.
- Regularise only the embeddings used in the batch.
- A loss that falls while HR@10 stays flat usually means the sampler or the evaluation excludes the wrong items.

**Notebook:** [M3](Project%20-%20MovieLens%20Recommender%20-%20M3%20BPR.ipynb)
**Read:** [[Collaborative Filtering and Matrix Factorization]] (implicit feedback) · [[Evaluating Recommenders]] · [[PyTorch Recipes]] · [[Optimizers]]

## Milestone 4 · Two-tower
**Goals**
- Build a user tower (id + recent history) and an item tower (id + genres + year), each ending in a normalised embedding.
- Train with an in-batch softmax; compare with and without the logQ correction.
- Do retrieval with precomputed item embeddings and compare exact search with an approximate index.

**Hints**
- Mask accidental hits: the same item appearing twice in a batch is a false negative.
- Use a temperature (≈ 0.05–0.1) with normalised embeddings; without it the softmax is too flat.
- Build history features only from training interactions, otherwise the target leaks into the user tower.

**Notebook:** [M4](Project%20-%20MovieLens%20Recommender%20-%20M4%20Two-Tower.ipynb)
**Read:** [[Deep Learning Recommenders]] · [[Content-Based and Hybrid Recommenders]] · [[Neural Networks]] · [[Self-Supervised and Contrastive Learning]]

## Milestone 5 · Multimodal with posters
**Goals**
- Fetch posters via TMDB using the ids in `links.csv` and extract frozen CLIP image features (plus text features from title and genres).
- Add them to your BPR model VBPR-style and compare with plain BPR.
- Run the **cold-item test**: hide all training interactions of 10% of the items and evaluate only on those. Add a modality ablation (image, text, both).

**Hints**
- A TMDB API key is free but personal; read it from an environment variable and never commit it. Cache every response.
- Not every movie has a poster; report coverage and decide how to treat the rest (zero vector plus a mask is fine).
- Standardise features before projecting them, or one modality will dominate ([[Multimodal Recommender Systems]], fusion section).
- Expect small gains on warm items and a large gain on cold ones; if the cold-item result is flat, check that the item ID embeddings of cold items really are untrained.

**Notebook:** [M5](Project%20-%20MovieLens%20Recommender%20-%20M5%20Multimodal%20with%20Posters.ipynb)
**Read:** [[Multimodal Recommender Systems]] · [[Computer Vision Overview]] · [[Text Representations]] · [[Self-Supervised and Contrastive Learning]]

## Wrap-up checklist
- One results table with all five models, same split, full-ranking metrics.
- One paragraph per milestone: what changed, what improved, what surprised you.
- Beyond accuracy: item coverage and average popularity of the top 10 for each model ([[Evaluating Recommenders]]).
- Optional follow-up: repeat M5 on a domain where images matter more, using the [[Recommender Systems Resources|resources]] list (Amazon Reviews 2023 with MMRec).

## Learn more
- [MovieLens datasets (GroupLens)](https://grouplens.org/datasets/movielens/)
- [BPR: Bayesian Personalized Ranking from Implicit Feedback](https://arxiv.org/abs/1205.2618)
- [VBPR: Visual Bayesian Personalized Ranking](https://arxiv.org/abs/1510.01784)
- [CLIP: Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020)
