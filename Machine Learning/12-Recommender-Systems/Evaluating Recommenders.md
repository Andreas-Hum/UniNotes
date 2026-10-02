---
tags: [ml, recsys, evaluation]
---
# Evaluating Recommenders

## Offline metrics
| Metric | Formula / idea |
|---|---|
| RMSE / MAE | rating prediction error |
| Precision@K / Recall@K | relevant items in top K |
| HitRate@K | ≥1 relevant in top K |
| **MRR** | $\frac1{|U|}\sum\frac1{\text{rank}_u}$ of first relevant |
| **MAP@K** | mean of average precision |
| **NDCG@K** | $\frac{DCG}{IDCG}$, $DCG=\sum_{k}\frac{2^{rel_k}-1}{\log_2(k+1)}$ |
| AUC | pairwise ranking correctness |
| Coverage, diversity, novelty, serendipity | beyond accuracy |

## Splitting
- **Temporal / leave-last-out**: hold out each user's most recent interaction(s) — avoids future leakage ([[Common Pitfalls]]).
- Random splits overestimate performance.
- **Sampled metrics** (rank among 100 random negatives) can mis-rank models — prefer full ranking (Krichene & Rendle 2020).

## Online
A/B tests (CTR, conversion, retention, watch time), interleaving, counterfactual / off-policy evaluation (IPS) from logged data.

General metrics: [[Model Evaluation and Metrics]].
