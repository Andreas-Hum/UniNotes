---
tags: [ml, probabilistic, bayesian]
---
# Bayesian Inference

$$\underbrace{p(\theta\mid D)}_{\text{posterior}}=\frac{\overbrace{p(D\mid\theta)}^{\text{likelihood}}\ \overbrace{p(\theta)}^{\text{prior}}}{\underbrace{p(D)}_{\text{evidence}}}$$

- **Predictive**: $p(y_*\mid x_*,D)=\int p(y_*\mid x_*,\theta)p(\theta\mid D)d\theta$ — averages over uncertainty instead of a point estimate.
- **Conjugate priors** give closed forms: Beta–Bernoulli, Dirichlet–Multinomial, Gaussian–Gaussian.
- **Bayesian linear regression**: prior $w\sim\mathcal N(0,\alpha^{-1}I)$ ⇒ Gaussian posterior; MAP = ridge ([[Linear Regression]]).
- **Model comparison** via evidence $p(D\mid M)$ (automatic Occam's razor).
- Intractable posteriors ⇒ [[Variational Inference]] or [[MCMC]].
- Non-parametric: [[Gaussian Processes]].

Foundations: [[Probability for ML]].
