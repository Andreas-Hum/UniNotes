---
tags: [ml, unsupervised, probabilistic, em]
---
# Gaussian Mixture Models and EM

$$p(x)=\sum_{k=1}^K\pi_k\,\mathcal N(x\mid\mu_k,\Sigma_k)$$
Latent variable $z$ = component. Direct MLE has a log of a sum, no closed form → **EM**.

## EM
- **E-step**: responsibilities $\gamma_{ik}=\frac{\pi_k\mathcal N(x_i\mid\mu_k,\Sigma_k)}{\sum_j\pi_j\mathcal N(x_i\mid\mu_j,\Sigma_j)}$
- **M-step**: with $N_k=\sum_i\gamma_{ik}$:
  $\mu_k=\frac1{N_k}\sum\gamma_{ik}x_i$, $\Sigma_k=\frac1{N_k}\sum\gamma_{ik}(x_i-\mu_k)(x_i-\mu_k)^\top$, $\pi_k=N_k/N$

The log-likelihood never decreases (it maximizes a lower bound; same ELBO idea as [[Variational Inference]]).

## Practical
- Local optima: multiple restarts, init with k-means ([[Clustering]]).
- Singularities when a component collapses on one point: regularize $\Sigma$.
- Choose $K$ with BIC ([[Cross-Validation and Model Selection]]).
- k-means = GMM with equal spherical covariances and hard assignments.

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 9
- [Mathematics for ML (free)](https://mml-book.github.io/) ch. 11
- [scikit-learn – GMMs](https://scikit-learn.org/stable/modules/mixture.html)
