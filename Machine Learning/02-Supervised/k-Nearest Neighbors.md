---
tags: [ml, supervised, non-parametric]
---
# k-Nearest Neighbors

Predict by majority vote (classification) or mean (regression) of the $k$ closest training points.

- **Lazy learner**: no training, all work at prediction.
- $k$ small → high variance; $k$ large → high bias ([[Bias-Variance Tradeoff]]). Choose by [[Cross-Validation and Model Selection]].
- **Distance**: Euclidean, Manhattan, cosine, Mahalanobis. **Scale features** ([[Data Preprocessing]]).
- **Curse of dimensionality**: distances concentrate in high dimensions.
- Speed-ups: k-d tree, ball tree, LSH, approximate NN (FAISS, HNSW).
- Weighted voting $w_i=1/d_i$.
- 1-NN error ≤ 2× Bayes error asymptotically (Cover–Hart).

## Learn more
- [scikit-learn – nearest neighbors](https://scikit-learn.org/stable/modules/neighbors.html)
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 2
