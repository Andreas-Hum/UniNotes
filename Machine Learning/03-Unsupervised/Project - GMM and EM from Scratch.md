---
tags: [ml, project, gmm, em, clustering]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - GMM and EM from Scratch

> [!summary] In one sentence
> Fit a Gaussian mixture with expectation–maximisation written from scratch, watch the log-likelihood rise monotonically, and beat k-means on stretched clusters.

**Notebook:** [Project - GMM and EM from Scratch](Project%20-%20GMM%20and%20EM%20from%20Scratch.ipynb) · topic: [[Gaussian Mixture Models and EM]] · all projects: [[Projects Overview]]

## What you build
1. `e_step`: responsibilities + log-likelihood.
2. `m_step`: weighted mixing proportions, means and covariances.

## Reference results (solution, laptop CPU)
EM converged in 55 iterations with a monotone log-likelihood. Adjusted Rand index vs. the true clusters: **GMM 0.773** vs k-means 0.411 (k-means can't model the elongated, overlapping clusters).

## Check yourself
> [!question]- Why does the log-likelihood never decrease in EM?
> Each E-step makes a lower bound (ELBO) tight at the current parameters, and each M-step maximises that bound, so the likelihood can only go up (or stay).

> [!question]- When does a GMM component collapse?
> If a component sits on a single point, its variance → 0 and the likelihood → ∞. The tiny ridge on Σ prevents that.

---
Back to [[00 - Machine Learning Index]].
