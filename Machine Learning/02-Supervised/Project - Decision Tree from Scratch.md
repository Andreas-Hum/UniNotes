---
tags: [ml, project, decision-trees]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Decision Tree from Scratch

> [!summary] In one sentence
> Implement CART (Gini impurity, exhaustive split search, recursion) on the breast-cancer data, match scikit-learn, and watch depth trade bias for variance.

**Notebook:** [Project - Decision Tree from Scratch](Project%20-%20Decision%20Tree%20from%20Scratch.ipynb) · topic: [[Decision Trees]] · all projects: [[Projects Overview]]

## What you build
1. `gini`: $1-\sum_kp_k^2$.
2. `best_split`: try every feature and threshold and keep the largest impurity decrease.

The recursive `build`/`predict` is given.

## Reference results (solution, laptop CPU)
| depth | train | test (yours) | test (sklearn) |
|---|---|---|---|
| 1 | 0.932 | 0.889 | 0.889 |
| 3 | 0.980 | 0.906 | 0.901 |
| 5 | 0.997 | 0.918 | 0.912 |
| 8 | 1.000 | 0.912 | 0.906 |

Root split: *worst perimeter ≤ 106.0*. Small differences from sklearn come from its midpoint thresholds.

## Check yourself
> [!question]- Why is the greedy best split not the best tree?
> Finding the optimal tree is NP-hard. CART picks the locally best split and never revisits it, so a worse first split can enable better ones later.

> [!question]- Why does training accuracy reach 1.0 at depth 8 while test accuracy stalls?
> Deep trees carve out regions around individual training points (high variance). Prune, limit depth, or average many trees (random forest).

---
Back to [[00 - Machine Learning Index]].
