---
tags: [ml, fundamentals, features]
status: not-started
notebook: not-started
level:
reviewed:
---
# Feature Engineering

> [!summary] In one sentence
> Feature engineering rewrites raw inputs into a representation $\phi(x)$ in which the pattern you want is **simple for your model**, often turning a hard non-linear problem into an easy linear one.

## Intuition first

A model can only use what you show it, in the form you show it. A linear model given "hour of day" as a number 0–23 thinks 23:00 and 00:00 are as far apart as possible. A linear model given "date of birth" cannot easily learn anything about age. A model given raw text cannot multiply words by weights at all.

Good features encode **domain knowledge about what matters and what is "close"**: that time is circular, that price ratios matter more than prices, that the word "refund" is informative but "the" is not. The best model with bad features usually loses to a simple model with good features, especially on tabular data.

There are two big moves:
1. **Transform or create** features so the relationship becomes simpler (logs, interactions, cyclic encodings, embeddings).
2. **Select or compress** features so the model is not drowned in noise (filter/wrapper/embedded selection, PCA).

![Cyclic encoding: hours on a line become points on a circle](../../Attachments/ML%20Animations/Feature%20Engineering%20-%20cyclic%20hour%20encoding.gif)
*Watch hours 23 and 0 (yellow): 23 apart on the number line, but neighbours once the line is bent into a circle with the sin/cos encoding.*

## The toolbox
- **Numeric**: scaling, log/Box–Cox for skew, binning, polynomial and interaction terms.
- **Categorical**: one-hot, ordinal, target/mean encoding (beware leakage), hashing, learned embeddings.
- **Text**: bag-of-words, TF-IDF, n-grams, word/sentence embeddings, [[Transformers]].
- **Time**: lags, rolling statistics, cyclic sin/cos encoding of hour/month.
- **Missing values**: indicator flags + imputation (see [[Data Preprocessing]]).
- **Selection**: filter (correlation, mutual information), wrapper (RFE), embedded (L1, tree importances).
- **Extraction**: [[PCA]], autoencoders, [[Kernel Methods]] (implicit feature maps).

### Numeric, with the *why*
- **Log / Box–Cox** compress long right tails (incomes, counts), turning multiplicative effects into additive ones a linear model can capture.
- **Binning** lets a linear model represent a step-shaped effect (age bands), at the cost of resolution.
- **Polynomial and interaction terms** ($x_1^2$, $x_1 x_2$) let a linear model represent curvature and "it depends" effects. The number of monomials of degree $\le p$ in $d$ features (including the constant) is $\binom{d+p}{p}$, which explodes quickly: $d = 10, p = 3$ gives 286.

### Categorical, with the *why*
- **One-hot**: one 0/1 column per category; no fake order. With an intercept, use $K-1$ columns (drop one), otherwise the columns sum to the intercept column and $X^\top X$ is singular: the **dummy-variable trap**. Regularized models tolerate all $K$.
- **Ordinal**: integers $0, 1, 2, \dots$ Only sensible when the order is real (small < medium < large), or for trees.
- **Target (mean) encoding**: replace a category by the mean target in that category. Powerful for high-cardinality features (zip codes) but **leaks**: a row's own label is part of its encoding, so rare categories become near-perfect predictors in training. Fix it with **out-of-fold** encoding (compute the mean on the other folds) and **smoothing** towards the global mean $\bar y$:
$$\text{enc}(c) = \frac{n_c\,\bar y_c + m\,\bar y}{n_c + m},$$
where $n_c$ is the category count, $\bar y_c$ its mean target, and $m$ a pseudo-count (how many "virtual" global-mean observations to add).
- **Hashing trick**: map each category or token to column $h(\text{token}) \bmod D$. Fixed memory, handles unseen categories, at the cost of occasional collisions.
- **Learned embeddings**: dense vectors trained jointly with a neural net; similar categories end up close.

### Text
- **Bag-of-words**: count of each word; **n-grams** add short phrases ("not good").
- **TF-IDF** down-weights words that appear everywhere:
$$\text{tfidf}(t, d) = \text{tf}(t, d)\cdot \log\frac{N}{\text{df}(t)},$$
with $\text{tf}$ the count of term $t$ in document $d$, $N$ the number of documents, $\text{df}(t)$ the number of documents containing $t$. (scikit-learn uses the smoothed $\ln\frac{1+N}{1+\text{df}} + 1$.) A word in every document gets weight $\log 1 = 0$.
- **Embeddings / Transformers** capture meaning and context, so "cheap" and "inexpensive" are close.

### Time
- **Lags and rolling statistics** (yesterday's sales, 7-day mean) give a model memory. Compute them using only the past.
- **Cyclic encoding**: $h \mapsto \big(\sin\frac{2\pi h}{24}, \cos\frac{2\pi h}{24}\big)$; months use period 12. Two numbers are needed because sine alone maps 6:00 and 18:00 to opposite values but 3:00 and 9:00 to the same one.

### Selection
- **Filter**: score each feature independently of any model (correlation, **mutual information** $I(X;Y) = \sum_{x,y} p(x,y)\log\frac{p(x,y)}{p(x)p(y)}$, which also catches non-linear dependence). Fast, but ignores interactions and redundancy.
- **Wrapper**: search subsets using the model's validation score, e.g. recursive feature elimination (RFE). Accurate but expensive and prone to overfitting the validation set.
- **Embedded**: selection happens during training: L1 drives weights to exactly zero; trees report importances.

## The math, step by step: why feature maps make models non-linear

Non-linear feature maps $\phi(x)$ turn linear models into non-linear ones; see [[Linear Models for Classification]].

1. A linear model computes $f(x) = w^\top x + b$: its decision boundary $f(x) = 0$ is a straight line (hyperplane) in $x$-space.
2. Replace $x$ by $\phi(x)$: $f(x) = w^\top \phi(x) + b$. The model is still **linear in the parameters** $w$, so fitting is just as easy (least squares, logistic regression, convex).
3. But as a function of $x$ it can be curved. With $\phi(x) = (x, x^2)$, the boundary $w_1 x + w_2 x^2 + b = 0$ is a pair of thresholds on $x$, enough to separate "inside an interval" from "outside".
4. Kernel methods take this to infinitely many features without computing $\phi$ explicitly.

![Adding x squared makes the classes linearly separable](../../Attachments/ML%20Animations/Feature%20Engineering%20-%20x%20squared%20makes%20classes%20separable.gif)
*Watch the 1-D points lift onto the parabola: no single threshold separates orange from blue on the line, but one horizontal line does after adding $x^2$.*

## Worked example

**Distances on the clock.** Hours 23 and 0 in the cyclic encoding: $23 \mapsto (\sin\frac{23\pi}{12}, \cos\frac{23\pi}{12}) \approx (-0.259, 0.966)$ and $0 \mapsto (0, 1)$. Euclidean distance $\approx \sqrt{0.067 + 0.001} \approx 0.261 = 2\sin\frac{\pi}{24}$. Hours 0 and 12 are at distance $2$, the maximum. Exactly as on a real clock.

**XOR with an interaction.** With $x_1, x_2 \in \{0, 1\}$, $\text{XOR} = x_1 + x_2 - 2x_1x_2$. No linear function of $(x_1, x_2)$ can produce XOR, but it is exactly linear in $(x_1, x_2, x_1 x_2)$.

**TF-IDF.** Documents: $d_1$ = "cat sat", $d_2$ = "cat cat dog", $d_3$ = "dog ran". $N = 3$. $\text{idf}(\text{cat}) = \ln\frac32 \approx 0.405$, $\text{idf}(\text{sat}) = \ln 3 \approx 1.099$. In $d_2$: $\text{tfidf}(\text{cat}) = 2 \times 0.405 = 0.811$, $\text{tfidf}(\text{dog}) = 0.405$. In $d_1$, the rare "sat" (1.099) outweighs "cat" (0.405).

**Smoothed target encoding.** A zip code seen $n_c = 4$ times, all positive ($\bar y_c = 1$); global rate $\bar y = 0.2$; $m = 10$: $\text{enc} = \frac{4\cdot 1 + 10 \cdot 0.2}{14} \approx 0.43$, not the over-confident $1.0$.

**Mutual information.** Binary $X, Y$ with $p(1,1) = p(0,0) = 0.4$, $p(1,0) = p(0,1) = 0.1$ (all marginals $0.5$): $I = 2(0.4\ln\frac{0.4}{0.25}) + 2(0.1\ln\frac{0.1}{0.25}) \approx 0.376 - 0.183 = 0.193$ nats.

## Common confusions
- **"Ordinal encoding is fine for any category."** It invents an order and distances (red = 0, green = 1, blue = 2 implies green is "between"). Linear models are misled; trees cope better.
- **"Target encoding is just another encoding."** Without out-of-fold computation it leaks the label and inflates validation scores.
- **"More features is always better."** Irrelevant features add variance and cost; they can hurt k-NN and unregularized models badly.
- **"Encoding the hour with sine alone is enough."** Sine is not one-to-one over a day; you need both sine and cosine.
- **"Feature selection on the whole dataset, then CV."** That selection saw the validation folds: do it inside the pipeline.

## Check yourself

> [!question]- Which encoding for a "country" feature with 200 values in a linear model? In a gradient-boosted tree?
> Linear model: one-hot (with regularization) or smoothed out-of-fold target encoding. Trees: ordinal or target encoding work well; one-hot also works but makes trees deeper.

> [!question]- How many features does a full degree-2 polynomial expansion of 4 inputs create, including the constant?
> $\binom{4+2}{2} = 15$: 1 constant, 4 linear, 4 squares, 6 pairwise interactions.

> [!question]- Why does a word that appears in every document get zero TF-IDF weight?
> $\text{idf} = \log(N/N) = 0$: it carries no information to distinguish documents.

> [!question]- Is L1-regularized regression a filter, wrapper or embedded selection method?
> Embedded: selection (zero weights) happens as part of fitting the model.

## Practice
[Feature Engineering - Exercises](Feature%20Engineering%20-%20Exercises.ipynb)

## Learn more
- [Kaggle Learn – Feature Engineering](https://www.kaggle.com/learn)
- [scikit-learn – preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
- [Kuhn & Johnson – Feature Engineering and Selection (free online book)](https://www.feat.engineering/)
