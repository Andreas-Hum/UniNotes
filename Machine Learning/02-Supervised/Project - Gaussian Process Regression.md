---
tags: [ml, project, gaussian-processes, bayesian]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Gaussian Process Regression

> [!summary] In one sentence
> Implement GP regression from scratch (RBF kernel, Cholesky-based posterior), match scikit-learn exactly, and see honest uncertainty: narrow error bars near data, wide ones in the gap.

**Notebook:** [Project - Gaussian Process Regression](Project%20-%20Gaussian%20Process%20Regression.ipynb) · topic: [[Gaussian Processes]] · all projects: [[Projects Overview]]

## What you build
1. `rbf`: the squared-exponential kernel matrix.
2. `gp_posterior`: mean and covariance via Cholesky solves.

## Reference results (solution, laptop CPU)
Mean and standard deviation match `GaussianProcessRegressor` with the same fixed kernel. Posterior std in the data gap ≈ **0.94** vs **0.14** next to data (ℓ = 1). Plots compare ℓ = 0.3 / 1 / 3.

## Check yourself
> [!question]- What does the length-scale ℓ control?
> How far apart two inputs can be while their outputs stay correlated: small ℓ = wiggly functions and error bars that grow quickly away from data; large ℓ = smooth functions.

> [!question]- Why Cholesky instead of inverting K?
> It's about twice as fast, numerically stabler, and gives the log-determinant for the marginal likelihood for free.

---
Back to [[00 - Machine Learning Index]].
