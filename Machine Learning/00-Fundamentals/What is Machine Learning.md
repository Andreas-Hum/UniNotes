---
tags: [ml, fundamentals]
---
# What is Machine Learning

> [!quote] Mitchell (1997)
> A program learns from experience **E** with respect to task **T** and performance measure **P**, if its performance at T, as measured by P, improves with E.

## Core idea
Instead of hand-writing rules, we fit a function $f_\theta : \mathcal{X} \to \mathcal{Y}$ to data by minimizing a loss.

$$\hat\theta = \arg\min_\theta \; \frac{1}{N}\sum_{i=1}^N \ell\big(f_\theta(x_i), y_i\big) + \lambda\,\Omega(\theta)$$

- $\ell$ — loss function (squared error, cross-entropy, hinge…)
- $\Omega$ — regularizer, see [[Overfitting and Regularization]]
- Optimization is usually [[Gradient Descent]]

## Ingredients
| Ingredient | Examples |
|---|---|
| Representation (hypothesis class) | linear, tree, neural net, kernel |
| Objective | MSE, log-likelihood, margin |
| Optimization | closed form, SGD, EM, greedy splits |
| Evaluation | [[Model Evaluation and Metrics]] |

## Task types
- **Classification** — discrete label; **Regression** — continuous target
- **Clustering**, **density estimation**, **dimensionality reduction** — no labels
- **Sequential decision making** — see [[RL Basics and MDPs]]

See [[Learning Paradigms]] and [[ML Workflow]].

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/)
- [Stanford CS229](https://cs229.stanford.edu/)
- [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course)
