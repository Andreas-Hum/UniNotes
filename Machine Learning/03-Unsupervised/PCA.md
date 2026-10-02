---
tags: [ml, unsupervised, dimensionality-reduction]
---
# PCA

Find orthogonal directions of maximal variance.

## Algorithm
1. Center the data (and usually standardize, [[Data Preprocessing]]).
2. Covariance $S=\frac1N X^\top X$.
3. Eigen-decompose $S=Q\Lambda Q^\top$; keep top $k$ eigenvectors $W$.
4. Project $Z=XW$. Reconstruct $\hat X=ZW^\top$.

Equivalent via SVD of $X$ ([[Linear Algebra for ML]]): $X=U\Sigma V^\top$, components are columns of $V$, $\lambda_i=\sigma_i^2/N$.

## Choosing $k$
Explained variance ratio $\frac{\sum_{i\le k}\lambda_i}{\sum\lambda_i}$ (e.g. ≥ 95%), scree plot.

## Views
- Maximize projected variance = minimize reconstruction error.
- Probabilistic PCA: latent variable model with Gaussian noise ([[Probabilistic Graphical Models]]).

## Limits
Linear only, sensitive to scale, components hard to interpret. Non-linear alternatives in [[Dimensionality Reduction]].
