---
tags: [ml, project, mcmc, bayesian]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Bayesian AB Test with MCMC

> [!summary] In one sentence
> Answer "how likely is version B better, and by how much?" for two note templates with a Bayesian binomial model, sampled by a random-walk Metropolis sampler you write yourself and checked against the exact Beta posterior.

**Notebook:** [Project - Bayesian AB Test with MCMC](Project%20-%20Bayesian%20AB%20Test%20with%20MCMC.ipynb) · topic: [[MCMC]] · all projects: [[Projects Overview]]

## What you build
1. `log_post`: binomial log-likelihood with flat priors.
2. `metropolis`: random-walk Metropolis–Hastings.

## Reference results (solution, laptop CPU)
Data: A 54/120 (45.0 %), B 66/115 (57.4 %).

| | value |
|---|---|
| P(B better), MCMC | 0.970 |
| P(B better), exact Beta | 0.971 |
| 95 % interval for pB − pA | [−0.005, +0.238] |
| acceptance rate | 51 % |

## Check yourself
> [!question]- Why does Metropolis only need the posterior up to a constant?
> The acceptance ratio p(x')/p(x) cancels the normalising constant, which is the intractable part of Bayes' rule.

> [!question]- P(B better) is 97 %, but the interval includes 0. Contradiction?
> No. The interval's lower end is just below 0, so about 3 % of the posterior mass has B worse. The interval shows how large the effect might be; the probability answers the decision question.

---
Back to [[00 - Machine Learning Index]].
