---
tags: [ml, project, knn, dimensionality]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - kNN and the Curse of Dimensionality

> [!summary] In one sentence
> Write a vectorised kNN that gets 98.5 % on digits, then watch accuracy collapse to 53 % when you append 1,024 irrelevant features, and see why: in high dimensions the nearest and farthest points are almost equally far.

**Notebook:** [Project - kNN and the Curse of Dimensionality](Project%20-%20kNN%20and%20the%20Curse%20of%20Dimensionality.ipynb) · topic: [[k-Nearest Neighbors]] · all projects: [[Projects Overview]]

## What you build
1. `knn_predict`: distance matrix + majority vote.
2. `distance_ratio`: nearest/farthest distance for random points in [0,1]^d.

## Reference results (solution, laptop CPU)
| | accuracy (k = 3) |
|---|---|
| 64 pixel features | 0.985 |
| + 64 noise features | 0.950 |
| + 256 noise features | 0.809 |
| + 1,024 noise features | 0.528 |

The min/max distance ratio goes from < 0.05 in 2-D to > 0.8 in 1,000-D.

## Check yourself
> [!question]- Why does logistic regression suffer much less from the noise features?
> It *learns* a weight per feature and can push noise weights towards 0. kNN's Euclidean distance weighs every feature equally, so noise drowns the signal.

---
Back to [[00 - Machine Learning Index]].
