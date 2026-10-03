---
tags: [ml, project, bias-variance, learning-curves]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - How Much Data Do I Need

> [!summary] In one sentence
> Plot learning curves for three models on handwritten digits and turn their shape into a decision: collect more data (high variance) or change the model (high bias).

**Notebook:** [Project - How Much Data Do I Need](Project%20-%20How%20Much%20Data%20Do%20I%20Need.ipynb) · topic: [[Bias-Variance Tradeoff]] · all projects: [[Projects Overview]]

## What you build
1. `learning_curve`: train/validation error vs. training-set size (fresh model per size, averaged over repeats).
2. `diagnose`: good enough / high variance / high bias from the curve's end.

## Reference results (solution, laptop CPU)
| model (n = 1,000) | train error | val error | diagnosis |
|---|---|---|---|
| logistic regression | 0.013 | 0.031 | high bias (just misses the 3 % target) |
| decision tree, depth 3 | 0.520 | 0.530 | high bias |
| RBF SVM | 0.006 | 0.017 | good enough |

## Check yourself
> [!question]- Training and validation error are both 0.52 and flat. Will more data help?
> No. The curves have converged at a high error, so the model can't represent the problem (high bias). Use a more flexible model or better features.

> [!question]- What does a large, shrinking gap between the curves tell you?
> High variance that more data is still fixing: keep collecting, or regularise.

---
Back to [[00 - Machine Learning Index]].
