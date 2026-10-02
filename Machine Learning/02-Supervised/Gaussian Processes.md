---
tags: [ml, supervised, probabilistic, kernels]
---
# Gaussian Processes

A distribution over functions: $f\sim\mathcal{GP}(m,k)$, any finite set of outputs is jointly Gaussian with covariance from a kernel ([[Kernel Methods]]).

## Regression posterior
With noise $\sigma^2$ and $K=k(X,X)$:
$$\mu_*=k_*^\top(K+\sigma^2I)^{-1}y,\qquad \Sigma_*=k_{**}-k_*^\top(K+\sigma^2I)^{-1}k_*$$

- Gives **uncertainty** along with predictions.
- Hyperparameters via maximizing the marginal likelihood.
- Cost $O(N^3)$; sparse/inducing-point approximations.
- Used in Bayesian optimization of hyperparameters ([[Cross-Validation and Model Selection]]).

Bayesian linear regression with basis functions is a GP with a finite-rank kernel ([[Bayesian Inference]]).

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 6
- [scikit-learn – Gaussian processes](https://scikit-learn.org/stable/modules/gaussian_process.html)
