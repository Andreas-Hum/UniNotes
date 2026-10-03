---
tags: [ml, supervised, probabilistic]
status: not-started
notebook: not-started
level:
reviewed:
---
# Naive Bayes

> [!summary] In one sentence
> Naive Bayes classifies by Bayes' rule, $p(y\mid x)\propto p(y)\,p(x\mid y)$, after making the bold ("naive") simplification that, once you know the class, every feature is independent of the others, so the likelihood becomes a simple product that can be learned just by counting.

## Intuition first

A doctor sees a patient with a fever, a cough and a rash. A naive-Bayes doctor reasons like this: "How common is flu in general? How often does a flu patient have a fever? A cough? A rash?" and multiplies those numbers together, then does the same for measles, and picks the disease with the bigger product. They never ask "how often do fever *and* cough *and* rash occur *together* in flu patients?", which would need far more past cases to estimate.

That is the whole method:
- **Prior** $p(y)$: how common each class is before looking at the features.
- **Likelihood per feature** $p(x_j\mid y)$: how typical feature $j$'s value is for that class.
- **Multiply** the prior by all per-feature likelihoods, compare across classes, normalise if you want probabilities.

**What problem does it solve?** It gives a classifier that trains in one pass of counting, handles thousands of features (e.g. every word in a vocabulary), needs little data, and is hard to beat as a quick baseline, which is why it powered the first wave of spam filters.

![Two class-conditional Gaussians scaled by their priors, producing the posterior curve](../../Attachments/ML%20Animations/Naive%20Bayes%20-%20prior%20times%20likelihood.gif)
*Watch the yellow class shrink when its likelihood is multiplied by its smaller prior (0.3); the decision boundary sits where the two weighted curves cross, which is exactly where the posterior below passes 0.5.*

## The math, step by step

### Bayes' rule plus one assumption
Assume features are conditionally independent given the class:
$$p(y\mid x)\propto p(y)\prod_j p(x_j\mid y)$$

Step by step:
1. Bayes' rule: $p(y\mid x) = \dfrac{p(y)\,p(x\mid y)}{p(x)}$. The denominator $p(x)=\sum_k p(y{=}k)\,p(x\mid y{=}k)$ is the same for every class, so for choosing the class we can ignore it ("$\propto$").
2. In general $p(x\mid y) = p(x_1\mid y)\,p(x_2\mid y, x_1)\cdots p(x_D\mid y, x_1,\dots,x_{D-1})$ (chain rule). Every factor depends on all previous features, which is hopeless to estimate.
3. **Naive assumption**: given $y$, knowing $x_1$ tells you nothing more about $x_2$. Then each factor collapses to $p(x_j\mid y)$ and the likelihood is the product.
4. Prediction: $\hat y = \arg\max_k \big[\log p(y{=}k) + \sum_j \log p(x_j\mid y{=}k)\big]$.

Note "conditionally" independent: features may well be correlated overall (because both depend on the class), the assumption is only about correlation *within* a class.

**Why it saves so much.** With $D$ binary features, a full table of $p(x\mid y)$ needs $2^D - 1$ numbers per class; with $D=30$ that is over a billion. Naive Bayes needs $D = 30$ numbers per class. Fewer parameters = far less data needed, at the cost of bias when the assumption is wrong.

### Variants: what $p(x_j\mid y)$ looks like

| Variant | $p(x_j\mid y)$ | Typical use |
|---|---|---|
| Gaussian | normal | continuous features |
| Multinomial | counts | text (bag of words) |
| Bernoulli | binary | presence/absence |

- **Gaussian**: $p(x_j\mid y{=}k) = \mathcal N(x_j\mid\mu_{jk},\sigma^2_{jk})$, one mean and variance per feature per class. In 2-D this means axis-aligned elliptical class blobs (no correlation term).
- **Multinomial**: a document is a bag of word counts; $p(x\mid y{=}k)\propto\prod_j \theta_{jk}^{\,x_j}$ where $\theta_{jk}$ is the probability that a random word in a class-$k$ document is word $j$ and $x_j$ is the count.
- **Bernoulli**: each feature is present/absent; $p(x\mid y{=}k)=\prod_j \theta_{jk}^{x_j}(1-\theta_{jk})^{1-x_j}$. Unlike multinomial, *absent* words also contribute evidence.

### Training
- Training = counting; MLE of priors and likelihoods.

Concretely, with $N_k$ training examples in class $k$:
- prior $p(y{=}k) = N_k/N$;
- Bernoulli: $\theta_{jk} = \frac{\#\{\text{class-}k\text{ examples with feature }j\}}{N_k}$;
- multinomial: $\theta_{jk} = \frac{n_{jk}}{n_k}$, where $n_{jk}$ is the total count of word $j$ in class $k$ and $n_k=\sum_j n_{jk}$;
- Gaussian: $\mu_{jk}$, $\sigma^2_{jk}$ = sample mean and variance of feature $j$ in class $k$.

These are exactly the maximum-likelihood estimates (maximising $\sum_i\log p(x_i, y_i)$ splits into independent per-feature problems, each solved by a frequency or a sample mean).

### Laplace smoothing
- **Laplace smoothing** avoids zero probabilities: $\frac{n_{jk}+\alpha}{n_k+\alpha V}$.

Here $V$ is the vocabulary size (number of possible values) and $\alpha>0$ (Laplace: $\alpha = 1$) acts like pretending you saw every word $\alpha$ extra times in every class. Why it is essential: if the word "blockchain" never appeared in a ham training email, the MLE gives $p(\text{blockchain}\mid\text{ham}) = 0$, and one occurrence in a test email multiplies the whole ham product by zero, regardless of all the other evidence. In Bayesian terms smoothing is the posterior mean under a symmetric Dirichlet prior.

### Log space
- Work in log space.

A document with 1000 words, each with probability around $10^{-4}$, has likelihood around $10^{-4000}$, far below the smallest double ($\approx 10^{-308}$): the product underflows to 0 for every class. Sum logs instead: $\log p(y) + \sum_j \log p(x_j\mid y)$. To turn log-scores $a_k$ back into probabilities use the **log-sum-exp** trick: $\log\sum_k e^{a_k} = m + \log\sum_k e^{a_k - m}$ with $m = \max_k a_k$, so the largest exponent is $e^0 = 1$ and nothing overflows or underflows.

## Worked example

**A spam posterior.** Priors $p(\text{spam}) = 0.4$, $p(\text{ham}) = 0.6$. Word likelihoods: $p(\text{free}\mid\text{spam}) = 0.5$, $p(\text{free}\mid\text{ham}) = 0.05$; $p(\text{win}\mid\text{spam}) = 0.3$, $p(\text{win}\mid\text{ham}) = 0.02$. An email contains "free" and "win".
- Spam score: $0.4\times0.5\times0.3 = 0.06$.
- Ham score: $0.6\times0.05\times0.02 = 0.0006$.
- Normalise: $p(\text{spam}\mid x) = 0.06/(0.06+0.0006)\approx 0.990$.
- In log space: $\log 0.06\approx -2.81$ vs $\log 0.0006\approx -7.42$; same decision, no tiny numbers.

**Laplace smoothing.** A word never seen in spam ($n_{jk}=0$), spam has $n_k = 1000$ word tokens, vocabulary $V = 5000$, $\alpha=1$: $p = (0+1)/(1000+5000) = 1/6000\approx 1.7\times10^{-4}$: small, but not a veto.

**Gaussian NB in 1-D** (the animation's numbers). Class 0: $\mu=3$, $\sigma=1$, prior $0.7$. Class 1: $\mu=6.5$, $\sigma=1.3$, prior $0.3$. At $x = 5$:
- $\mathcal N(5\mid 3, 1)\approx 0.054$, times $0.7$ → $0.038$.
- $\mathcal N(5\mid 6.5, 1.3^2)\approx 0.158$, times $0.3$ → $0.047$.
- $p(y{=}1\mid x{=}5) = 0.047/(0.038+0.047)\approx 0.56$: just past the boundary. At $x = 4.5$ the same computation gives $\approx 0.24$.

**Counting MLE.** 10 training emails, 4 spam; "free" appears in 2 of the 4 spam and 1 of the 6 ham. Bernoulli MLE: $p(\text{spam}) = 0.4$, $\theta_{\text{free},\text{spam}} = 2/4 = 0.5$, $\theta_{\text{free},\text{ham}} = 1/6\approx 0.17$.

## Why it works, and where it fails

- Surprisingly strong baseline; probabilities are poorly calibrated.
  - *Strong baseline*: classification only needs the **argmax** to be right, not the probabilities. Even when the independence assumption is wrong, the product often still ranks the correct class first. With few samples, its low variance beats more flexible models.
  - *Poor calibration*: correlated features are counted as if they were independent pieces of evidence. If "free" and "FREE!!!" always co-occur, their evidence is counted twice, pushing posteriors towards 0 or 1. Do not read 0.9999 as "almost certain"; recalibrate (Platt scaling, isotonic regression) if you need probabilities.
- **Gaussian NB can be a linear classifier.** If each feature's variance is shared across classes ($\sigma_{jk} = \sigma_j$), the $x_j^2$ terms cancel in $\log\frac{p(y=1\mid x)}{p(y=0\mid x)}$, which is then linear in $x$: $p(y{=}1\mid x)=\sigma(w^\top x + b)$, the same form as logistic regression. With class-specific variances the boundary is quadratic.
- It is the simplest [[Probabilistic Graphical Models|graphical model]] (star-shaped Bayesian network).
  The class node $y$ sits in the middle with an arrow to each feature $x_j$ and no arrows between features; that missing-edge structure *is* the conditional-independence assumption.

Compare: [[Logistic Regression]] (discriminative counterpart).

Naive Bayes (generative: models $p(x, y)$) and logistic regression (discriminative: models $p(y\mid x)$) can represent the same family of linear decision boundaries. A classic result (Ng & Jordan, 2001) is that naive Bayes approaches its best error with far fewer examples, while logistic regression, which does not rely on the independence assumption, usually reaches a lower error once data are plentiful.

## Common confusions
- *"Naive Bayes assumes the features are independent."* → It assumes they are independent **given the class**; overall they can be strongly correlated.
- *"It is Bayesian because it uses Bayes' rule."* → Plain NB uses MLE point estimates; it is not Bayesian inference over parameters (smoothing is the one Bayesian touch).
- *"Its probabilities are reliable because it is a probabilistic model."* → Double-counted evidence makes it over-confident; the argmax is often good, the numbers less so.
- *"Multinomial and Bernoulli NB are the same for text."* → Multinomial uses counts and ignores absent words; Bernoulli uses presence/absence and penalises missing words. Bernoulli can do better on short texts.
- *"Laplace smoothing is optional."* → Without it a single unseen feature value zeros out a class.

## Check yourself

> [!question]- Write the naive Bayes decision rule in log space.
> $\hat y=\arg\max_k\big[\log p(y{=}k)+\sum_j\log p(x_j\mid y{=}k)\big]$.

> [!question]- Why does an unseen word without smoothing break the classifier?
> Its MLE probability is 0, so the whole product for that class becomes 0 (log $-\infty$) regardless of all other evidence.

> [!question]- You duplicate one feature 5 times. What happens to the predicted probabilities?
> That feature's likelihood ratio is applied 6 times, so posteriors become more extreme (over-confident) even though no new information was added.

> [!question]- When is Gaussian naive Bayes a linear classifier?
> When each feature's variance is the same in every class; then the quadratic terms cancel in the log-odds.

> [!question]- How many parameters does Bernoulli NB need for 2 classes and 1000 binary features?
> $2\times 1000$ likelihoods plus $1$ free prior parameter, i.e. 2001 (versus $2\,(2^{1000}-1)$ for the full joint).

## Practice
[Naive Bayes - Exercises](Naive%20Bayes%20-%20Exercises.ipynb): what is naive, choosing a variant, double counting and calibration, the generative vs discriminative pair; by hand: a spam posterior, Laplace smoothing, 1-D Gaussian NB, parameter counting, MLE by counting, when Gaussian NB is linear, log space; in code: Gaussian, multinomial and Bernoulli NB from scratch, log-sum-exp and measuring over-confidence.

**Project:** [[Project - SMS Spam Filter]] – a word-counting spam filter checked against scikit-learn

## Learn more
- [scikit-learn – Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)
- [CS229 cheatsheets](https://stanford.edu/~shervine/teaching/cs-229/)
- [Stanford CS229 lecture notes](https://cs229.stanford.edu/main_notes.pdf): generative learning algorithms, GDA and naive Bayes with Laplace smoothing
