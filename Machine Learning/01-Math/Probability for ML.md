---
tags: [ml, math, probability]
---
# Probability for ML

## Rules
- Sum: $p(x)=\sum_y p(x,y)$ · Product: $p(x,y)=p(y\mid x)p(x)$
- **Bayes**: $p(\theta\mid D)=\frac{p(D\mid\theta)p(\theta)}{p(D)}$ → [[Bayesian Inference]]
- Independence $p(x,y)=p(x)p(y)$; conditional independence underlies [[Naive Bayes]] and [[Probabilistic Graphical Models]].

## Moments
$\mathbb E[X]$, $\mathrm{Var}(X)=\mathbb E[X^2]-\mathbb E[X]^2$, $\mathrm{Cov}$. Linearity of expectation always holds.

## Key distributions
| Name | Use |
|---|---|
| Bernoulli / Binomial | binary outcomes, coin flips |
| Categorical / Multinomial | class labels, word counts |
| Gaussian $\mathcal N(\mu,\Sigma)$ | continuous noise, [[Gaussian Processes]] |
| Beta / Dirichlet | priors over probabilities (conjugate) |
| Poisson | counts |
| Exponential family | unifying form; GLMs |

## Estimation
- **MLE**: $\hat\theta=\arg\max\sum\log p(x_i\mid\theta)$. Gaussian → least squares; Bernoulli → cross-entropy.
- **MAP**: MLE + log prior. Gaussian prior ⇒ L2, Laplace ⇒ L1 ([[Overfitting and Regularization]]).

## Limits
Law of large numbers, CLT, Hoeffding bound (used in PAC arguments).

See [[Information Theory]].

## Learn more
- [Mathematics for ML (free)](https://mml-book.github.io/) ch. 6
- [Murphy – Probabilistic ML (free)](https://probml.github.io/pml-book/)
- [StatQuest videos](https://statquest.org/video_index.html)
