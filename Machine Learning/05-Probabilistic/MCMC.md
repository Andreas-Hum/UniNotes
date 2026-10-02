---
tags: [ml, probabilistic, sampling]
---
# MCMC

Draw samples from $p(\theta\mid D)\propto p(D\mid\theta)p(\theta)$ without knowing $Z$.

| Method | Idea |
|---|---|
| **Metropolis–Hastings** | propose $\theta'\sim q$, accept with $\min\!\big(1,\frac{\tilde p(\theta')q(\theta\mid\theta')}{\tilde p(\theta)q(\theta'\mid\theta)}\big)$ |
| **Gibbs** | sample each variable from its conditional |
| **HMC / NUTS** | use gradients for long informed moves (Stan, PyMC) |
| Langevin dynamics | gradient + noise; links to diffusion models |
| Importance / rejection sampling | simple but poor in high dimensions |

## Diagnostics
Trace plots, effective sample size, $\hat R$ (≤ 1.01), burn-in, thinning.

Compared with [[Variational Inference]]: slower but asymptotically exact. Context: [[Bayesian Inference]], [[Probabilistic Graphical Models]].

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 11
- [PyMC docs](https://www.pymc.io/)
- [Statistical Rethinking 2024](https://github.com/rmcelreath/stat_rethinking_2024)
