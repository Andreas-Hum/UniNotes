---
tags: [ml, supervised, probabilistic]
---
# Naive Bayes

Assume features are conditionally independent given the class:
$$p(y\mid x)\propto p(y)\prod_j p(x_j\mid y)$$

| Variant | $p(x_j\mid y)$ | Typical use |
|---|---|---|
| Gaussian | normal | continuous features |
| Multinomial | counts | text (bag of words) |
| Bernoulli | binary | presence/absence |

- Training = counting; MLE of priors and likelihoods.
- **Laplace smoothing** avoids zero probabilities: $\frac{n_{jk}+\alpha}{n_k+\alpha V}$.
- Work in log space.
- Surprisingly strong baseline; probabilities are poorly calibrated.
- It is the simplest [[Probabilistic Graphical Models|graphical model]] (star-shaped Bayesian network).

Compare: [[Logistic Regression]] (discriminative counterpart).

## Learn more
- [scikit-learn – Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)
- [CS229 cheatsheets](https://stanford.edu/~shervine/teaching/cs-229/)
