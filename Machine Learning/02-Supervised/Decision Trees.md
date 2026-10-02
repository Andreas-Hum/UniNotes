---
tags: [ml, supervised, trees]
---
# Decision Trees

Recursive partitioning: pick the split that best reduces impurity.

| Criterion | Formula |
|---|---|
| Entropy | $-\sum p_k\log_2p_k$ |
| Gini | $1-\sum p_k^2$ |
| Variance (regression) | $\frac1n\sum(y-\bar y)^2$ |

**Information gain** = parent impurity − weighted child impurity ([[Information Theory]]). ID3 uses gain, C4.5 uses gain ratio, CART uses Gini and binary splits.

## Controlling overfitting
Max depth, min samples per leaf, **cost-complexity pruning**, validation pruning.

## Pros / cons
+ interpretable, handles mixed types and missing values, no scaling needed
− unstable (high variance), axis-aligned boundaries

Fix variance with [[Ensemble Methods]] (Random Forest, Gradient Boosting).
