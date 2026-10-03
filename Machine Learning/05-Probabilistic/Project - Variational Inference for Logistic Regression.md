---
tags: [ml, project, variational-inference, bayesian]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Variational Inference for Logistic Regression

> [!summary] In one sentence
> Fit a Bayesian logistic regression with mean-field variational inference (reparameterisation trick + Adam), compare it with a long MCMC run, and watch VI underestimate the uncertainty of strongly correlated weights.

**Notebook:** [Project - Variational Inference for Logistic Regression](Project%20-%20Variational%20Inference%20for%20Logistic%20Regression.ipynb) · topic: [[Variational Inference]] · all projects: [[Projects Overview]]

## What you build
1. `elbo`: reparameterised Monte Carlo ELBO = expected log-likelihood + log-prior + entropy.

## Reference results (solution, laptop CPU)
Two features with correlation 0.94:

| | mean VI / MCMC | std VI / MCMC |
|---|---|---|
| bias | +0.13 / +0.06 | 0.33 / 0.34 |
| w1 | +1.70 / +1.66 | **0.51 / 1.14** |
| w2 | +0.61 / +0.50 | **0.50 / 1.08** |

MCMC finds a posterior correlation of −0.88 between w1 and w2; the mean-field approximation can't represent it and halves the standard deviations.

## Check yourself
> [!question]- Why does mean-field VI underestimate variance?
> It minimises KL(q‖p), which punishes q for putting mass where p has little. A factorised q fitted to a correlated, elongated posterior chooses a narrow, axis-aligned blob inside it.

> [!question]- What does the reparameterisation trick buy?
> Writing w = μ + σ⊙ε moves the randomness into ε, so the sample is a differentiable function of μ and σ and the ELBO gradient has low variance.

---
Back to [[00 - Machine Learning Index]].
