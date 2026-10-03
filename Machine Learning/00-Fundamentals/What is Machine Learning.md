---
tags: [ml, fundamentals]
status: not-started
notebook: not-started
level:
reviewed:
---
# What is Machine Learning

> [!summary] In one sentence
> Machine learning means choosing a function from a family of candidates by **minimising a loss on example data**, so that the program improves with experience instead of being hand-coded.

> [!quote] Mitchell (1997)
> A program learns from experience **E** with respect to task **T** and performance measure **P**, if its performance at T, as measured by P, improves with E.

## Intuition first

Think about how you would write a spam filter by hand. You might start with rules: "if the subject contains FREE, it is spam". Soon you need hundreds of rules, they contradict each other, and spammers change their wording faster than you can update them. Machine learning flips the process: instead of writing the rules, you **collect examples** (emails marked spam / not spam), **pick a flexible family of functions** (say, a weighted sum of word counts), and let an algorithm **tune the knobs** of that function until it makes as few mistakes as possible on the examples.

Mitchell's definition names the three things you must pin down before anything can be "learned":

- **Task T**: what the program does (classify emails).
- **Experience E**: the data it learns from (labelled emails).
- **Performance P**: how we score it (accuracy, or better, precision/recall on spam).

If you cannot name all three, the problem is not yet a learning problem.

When is learning better than rules? When the rules are **too many or unknown** (recognising faces), **change over time** (spam, fraud), or **differ per user** (recommendations). When a short exact rule exists (e.g. computing tax from a formula), just write the rule.

![Fitting a line by minimising the loss](../../Attachments/ML%20Animations/What%20is%20Machine%20Learning%20-%20fitting%20by%20minimising%20loss.gif)
*Watch the red residuals shrink and the loss number fall as gradient descent adjusts $w$ and $b$: "learning" is exactly this knob-turning.*

## Core idea
Instead of hand-writing rules, we fit a function $f_\theta : \mathcal{X} \to \mathcal{Y}$ to data by minimizing a loss.

$$\hat\theta = \arg\min_\theta \; \frac{1}{N}\sum_{i=1}^N \ell\big(f_\theta(x_i), y_i\big) + \lambda\,\Omega(\theta)$$

- $\ell$: loss function (squared error, cross-entropy, hinge…)
- $\Omega$: regularizer, see [[Overfitting and Regularization]]
- Optimization is usually [[Gradient Descent]]

## The math, step by step

**Symbols.** $\mathcal{X}$ is the input space (e.g. $\mathbb{R}^d$), $\mathcal{Y}$ the output space ($\mathbb{R}$ for regression, $\{0,1\}$ for binary classification). $\theta$ are the parameters (the "knobs"), $f_\theta$ the model, $(x_i, y_i)$ the $N$ training examples, $\lambda \ge 0$ the regularization strength.

**1. Expected risk: what we actually care about.** Data come from an unknown distribution $p(x, y)$. The ideal model minimises the *expected* loss on new data:
$$R(\theta) = \mathbb{E}_{(x,y)\sim p}\big[\ell(f_\theta(x), y)\big].$$
We cannot compute this, because $p$ is unknown.

**2. Empirical risk: what we can compute.** Replace the expectation by an average over the training sample:
$$\hat R(\theta) = \frac{1}{N}\sum_{i=1}^N \ell\big(f_\theta(x_i), y_i\big).$$
Minimising $\hat R$ is called **empirical risk minimisation (ERM)**. By the law of large numbers $\hat R(\theta) \to R(\theta)$ for a *fixed* $\theta$, but the $\theta$ we pick is chosen *because* it does well on this sample, so $\hat R(\hat\theta)$ is optimistic. That gap is overfitting.

**3. Regularized risk.** Add a penalty $\lambda\,\Omega(\theta)$ that prefers "simple" parameters (e.g. $\Omega = \lVert\theta\rVert_2^2$). Larger $\lambda$ means more preference for simplicity and less trust in the data.

**Common losses** (with $\hat y = f_\theta(x)$):

| Loss | Formula | Used for |
|---|---|---|
| Squared | $(\hat y - y)^2$ | regression; best constant is the **mean** |
| Absolute | $\lvert \hat y - y\rvert$ | robust regression; best constant is the **median** |
| Cross-entropy (log loss) | $-\big[y\log\hat p + (1-y)\log(1-\hat p)\big]$ | probabilistic classification |
| Hinge | $\max(0,\, 1 - y\,s)$, $y\in\{-1,+1\}$, score $s$ | SVMs |
| 0-1 | $\mathbb{1}[y\,s \le 0]$ | what we "really" count, but not differentiable |

The hinge loss is a convex **upper bound** on the 0-1 loss: it is never smaller, and it still penalises correct but low-confidence predictions ($0 < ys < 1$).

**Density estimation is also loss minimisation**: with no labels, use the negative log-likelihood $\ell(\theta; x) = -\log p_\theta(x)$, so $\hat\theta = \arg\min_\theta -\frac1N\sum_i \log p_\theta(x_i)$, i.e. maximum likelihood.

**Why the mean is the best constant under squared loss.** Minimise $g(c) = \frac1N\sum_i (c - y_i)^2$. Its derivative is $g'(c) = \frac2N\sum_i (c - y_i)$; setting it to zero gives $c = \frac1N\sum_i y_i = \bar y$. (For absolute loss the derivative counts points above minus points below, which is zero at the median.)

## Worked example

Data: $(x, y) = (1, 2),\ (2, 3),\ (3, 7)$. Model: $f_w(x) = w x$ (no intercept).

1. **Empirical risk of $w = 2$.** Predictions $2, 4, 6$; errors $0, 1, -1$; squared $0, 1, 1$. $\hat R = \tfrac{2}{3} \approx 0.667$.
2. **Best $w$ without regularization.** $\hat R(w) = \frac13\sum_i (w x_i - y_i)^2$. Set the derivative to zero: $\sum_i x_i (w x_i - y_i) = 0 \Rightarrow w = \frac{\sum x_i y_i}{\sum x_i^2} = \frac{2 + 6 + 21}{1 + 4 + 9} = \frac{29}{14} \approx 2.071$.
3. **Add a regularizer** $\lambda w^2$ with $\lambda = 1$. Derivative: $\frac{2}{N}\sum_i x_i(w x_i - y_i) + 2\lambda w = 0 \Rightarrow w = \frac{\sum x_i y_i}{\sum x_i^2 + N\lambda} = \frac{29}{14 + 3} \approx 1.706$.

The penalty pulled $w$ towards $0$: that is shrinkage, the core mechanism of regularization.

## Ingredients
| Ingredient | Examples |
|---|---|
| Representation (hypothesis class) | linear, tree, neural net, kernel |
| Objective | MSE, log-likelihood, margin |
| Optimization | closed form, SGD, EM, greedy splits |
| Evaluation | [[Model Evaluation and Metrics]] |

**Why each ingredient matters.**
- The **hypothesis class** decides what is even learnable. A linear model can never fit a sine wave, however much data you give it; a degree-15 polynomial can fit it, and it can also fit the noise.
- The **objective** encodes what "good" means. Squared error punishes big mistakes heavily; absolute error is robust to outliers; log-likelihood rewards calibrated probabilities.
- The **optimizer** is how you search the class. Some objectives have closed forms (least squares), some are convex (logistic regression) so any descent method finds the optimum, and some are non-convex (neural nets), where the optimizer itself shapes the result.
- **Evaluation** must happen on data the model did not train on; otherwise you are measuring memory, not learning.

## Task types
- **Classification**: discrete label; **Regression**: continuous target
- **Clustering**, **density estimation**, **dimensionality reduction**: no labels
- **Sequential decision making**: see [[RL Basics and MDPs]]

Quick test: look at the **target**. A category (spam/ham, digit 0–9) is classification; a number on a continuous scale (price, temperature) is regression; no target at all means one of the unsupervised tasks; a reward that arrives after a sequence of actions means sequential decision making.

See [[Learning Paradigms]] and [[ML Workflow]].

## Common confusions
- **"Low training loss means a good model."** No: ERM is optimistic. Judge on held-out data; see [[Overfitting and Regularization]].
- **"The loss and the metric are the same thing."** Often not. We train with cross-entropy (smooth, differentiable) but report accuracy or F1. The loss is for the optimizer; the metric is for humans.
- **"More flexible models are always better."** Flexibility helps only when you have enough data to pin it down; otherwise it fits noise.
- **"ML replaces domain knowledge."** Domain knowledge goes into the choice of features, hypothesis class, loss and metric.
- **"Regularization is a hack."** It is principled: it equals a prior on the parameters (MAP estimation) and directly controls the train/test gap.

## Check yourself

> [!question]- A chess program improves by playing games against itself. Name T, E and P.
> T = playing chess; E = the self-play games; P = e.g. win rate (or Elo) against a fixed set of opponents.

> [!question]- What is the difference between empirical and expected risk?
> Expected risk is the average loss over the true data distribution (what we want, not computable). Empirical risk is the average over the training sample (computable). ERM minimises the latter as a proxy for the former.

> [!question]- Under squared loss, what is the best constant prediction? Under absolute loss?
> The mean of the targets for squared loss; the median for absolute loss.

> [!question]- Why do we train with hinge or cross-entropy instead of directly minimising the 0-1 loss?
> The 0-1 loss is piecewise constant (zero gradient almost everywhere) and minimising it is NP-hard in general. Hinge and cross-entropy are convex, differentiable (almost everywhere) surrogates that upper-bound or approximate it.

> [!question]- Increasing $\lambda$ in the regularized objective does what to the solution of the worked example?
> It shrinks $w = \frac{\sum x_i y_i}{\sum x_i^2 + N\lambda}$ towards $0$: more bias, less variance.

## Practice
[What is Machine Learning - Exercises](What%20is%20Machine%20Learning%20-%20Exercises.ipynb)

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/)
- [Stanford CS229](https://cs229.stanford.edu/)
- [Google ML Crash Course](https://developers.google.com/machine-learning/crash-course)
- [3Blue1Brown – Neural networks series](https://www.3blue1brown.com/topics/neural-networks) (visual intuition for "learning = minimising a cost")
