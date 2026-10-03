---
tags: [ml, supervised, non-parametric]
status: not-started
notebook: not-started
level:
reviewed:
---
# k-Nearest Neighbors

> [!summary] In one sentence
> To predict for a new point, k-NN finds the $k$ most similar training points and lets them vote (classification) or averages their values (regression); there is no model beyond the stored data and a notion of distance.

## Intuition first

You move to a new city and want to guess whether a restaurant is good. You do not build a theory of restaurants; you ask the few people whose taste is *most like yours* and go with the majority. That is k-NN: "you are like your neighbours".

Three design choices completely determine the method:
1. **What "near" means**: the distance function (and therefore how features are scaled).
2. **How many neighbours to ask**: $k$. Ask one person and a single odd opinion decides; ask the whole city and you just get the city-wide average.
3. **How to combine their answers**: plain majority/mean, or weight closer neighbours more.

**What problem does it solve?** It gives a flexible, assumption-free predictor that can draw arbitrarily wiggly boundaries, works for classification and regression, and adapts instantly to new data (just add points). It is a great baseline and the core idea behind recommendation ("users like you"), retrieval and vector databases.

![A circle growing around a query point to include its 1, 3 and 7 nearest neighbours](../../Attachments/ML%20Animations/k-Nearest%20Neighbors%20-%20majority%20vote.gif)
*Watch the white query point change colour: with $k=1$ its single nearest neighbour is blue, with $k=3$ two yellows outvote one blue, and with $k=7$ blue wins 4 to 3. Same data, three different answers.*

## The algorithm

Predict by majority vote (classification) or mean (regression) of the $k$ closest training points.

Formally, for a query $x_\star$ let $N_k(x_\star)$ be the indices of the $k$ training points with the smallest distance $d(x_\star, x_i)$. Then
- classification: $\hat y = \arg\max_c \sum_{i\in N_k(x_\star)} \mathbb 1[y_i = c]$, and $\hat p(c\mid x_\star) = \frac1k\sum_{i\in N_k}\mathbb 1[y_i=c]$ is a (rough) probability estimate;
- regression: $\hat y = \frac1k\sum_{i\in N_k(x_\star)} y_i$.

With **weighted voting** $w_i=1/d_i$, each neighbour's vote (or value) is multiplied by $w_i$ and the result is divided by $\sum_i w_i$, so very close neighbours dominate. (If some $d_i = 0$, just return that point's label.)

## Key properties, and why they hold

- **Lazy learner**: no training, all work at prediction.
  "Training" is storing the data. A naive query computes $N$ distances in $D$ dimensions, $O(ND)$, and keeps the $k$ smallest. That is the opposite trade-off from, say, [[Linear Regression]] (slow-ish training, instant prediction). It is also **non-parametric**: the "model" grows with the data.
- $k$ small → high variance; $k$ large → high bias ([[Bias-Variance Tradeoff]]). Choose by [[Cross-Validation and Model Selection]].
  With $k=1$ every training point owns a little island (training error is 0, the boundary follows every noisy point). As $k$ grows, predictions average over larger regions, so the boundary smooths; at $k=N$ every query gets the majority class. Use odd $k$ for two classes to avoid ties.
- **Distance**: Euclidean, Manhattan, cosine, Mahalanobis. **Scale features** ([[Data Preprocessing]]).
  Distances add up contributions from every feature, so a feature measured in large units (income in euros) swamps one in small units (age in years). Standardise (zero mean, unit variance) or min–max scale first, or the "nearest" neighbours are just the ones with similar income.
- **Curse of dimensionality**: distances concentrate in high dimensions.
  In high $D$, the nearest and the farthest point are almost the same distance away (ratio → 1), so "nearest" loses meaning. And local neighbourhoods are not local: see the worked example. Remedies: fewer/better features, dimensionality reduction, learned embeddings.
- Speed-ups: k-d tree, ball tree, LSH, approximate NN (FAISS, HNSW).
  - **k-d tree**: recursively split on the median of one coordinate; at query time skip any subtree whose region is farther than the current $k$-th best distance. Great in low $D$ (< ~20), degrades towards brute force in high $D$.
  - **Ball tree**: nested hyperspheres instead of boxes; works with any metric and copes better with moderate $D$.
  - **LSH / FAISS / HNSW**: *approximate* search. They return neighbours that are probably among the true nearest (recall < 100%) in exchange for sub-linear query time on millions of vectors (this is how vector databases work).
- Weighted voting $w_i=1/d_i$.
  Reduces the sensitivity to the exact choice of $k$ and makes regression predictions vary smoothly.
- 1-NN error ≤ 2× Bayes error asymptotically (Cover–Hart).
  Precisely, as $N\to\infty$ (binary case) $R^* \le R_{1\text{NN}} \le 2R^*(1-R^*) \le 2R^*$, where $R^*$ is the Bayes error, the lowest error any classifier can achieve. Intuition: with infinite data the nearest neighbour sits essentially *at* $x_\star$, so its label is an independent draw from the same $p(y\mid x_\star)$. You err if the two draws disagree, which happens at most about twice as often as the Bayes classifier errs. It says the simplest possible method is never terrible with enough data, but says nothing about finite samples.

![k-NN decision regions for k = 1, 5, 15 and 121 on the same data](../../Attachments/ML%20Animations/k-Nearest%20Neighbors%20-%20effect%20of%20k.gif)
*Watch the coloured regions: at $k=1$ they are jagged islands around single points (overfitting), around $k=15$ they trace the two moons, and at $k=121$ the boundary flattens towards a straight line (underfitting).*

## The math, step by step: distances

For $x, z \in\mathbb R^D$:
- **Euclidean** $\|x-z\|_2=\sqrt{\sum_j(x_j-z_j)^2}$: straight-line distance; the default for dense, scaled numeric features.
- **Manhattan** $\|x-z\|_1=\sum_j|x_j-z_j|$: "city-block" distance; less dominated by one large coordinate difference.
- **Cosine distance** $1-\frac{x^\top z}{\|x\|\|z\|}$: compares *direction* only, ignoring length. Natural for text (TF-IDF) and embeddings, where document length should not matter.
- **Mahalanobis** $\sqrt{(x-z)^\top\Sigma^{-1}(x-z)}$: Euclidean distance after "whitening" the data with covariance $\Sigma$; automatically rescales features and accounts for correlations.

## Worked example

**Majority vote in 1-D.** Training: class A at $1,\ 2,\ 2.5$; class B at $4,\ 6$. Query $x_\star = 3.5$.
- Distances: A → $2.5,\ 1.5,\ 1.0$; B → $0.5,\ 2.5$.
- $k=1$: nearest is $4$ (B) → predict **B**.
- $k=3$: $4$ (B, 0.5), $2.5$ (A, 1.0), $2$ (A, 1.5) → 2 A vs 1 B → predict **A**.

**Regression, plain vs weighted.** Three neighbours at distances $1, 2, 4$ with targets $3, 6, 9$.
- Plain mean: $(3+6+9)/3 = 6$.
- Weights $1/d = 1,\ 0.5,\ 0.25$ (sum $1.75$): $\hat y = (3 + 3 + 2.25)/1.75 \approx 4.71$, pulled towards the closest neighbour.

**Four distances** between $x=(0,0)$ and $z=(3,4)$:
- Euclidean $\sqrt{9+16}=5$; Manhattan $3+4=7$;
- Mahalanobis with $\Sigma=\operatorname{diag}(4,1)$: $\sqrt{9/4+16}\approx 4.27$ (feature 1 has large variance, so its difference counts less);
- Cosine distance between $(1,0)$ and $(1,1)$: $1-\frac{1}{\sqrt2}\approx 0.29$, while $(1,0)$ and $(5,0)$ have cosine distance $0$ (same direction).

**Scaling changes the neighbours.** Person P = (age 30, income 50 000). Candidates Q = (31, 52 000) and R = (60, 50 500). Unscaled Euclidean: $d(P,Q)\approx 2000$, $d(P,R)\approx 500$, so the 60-year-old is "closer" purely because income is in euros. After standardising (say age sd 10, income sd 10 000) $d(P,Q)\approx\sqrt{0.01+0.04}\approx 0.22$ and $d(P,R)\approx\sqrt{9+0.0025}\approx 3.0$: Q is the sensible neighbour.

**How big is a "local" neighbourhood?** Data uniform in the unit hypercube $[0,1]^D$. To capture a fraction $r$ of the points with a sub-cube you need edge length $r^{1/D}$. For $r = 1\%$: $D=1$ → $0.01$; $D=10$ → $0.01^{0.1}\approx 0.63$; $D=100$ → $\approx 0.955$. In 10-D, your "1% nearest neighbours" span 63% of each feature's range: not local at all.

**Cover–Hart in numbers.** If the Bayes error is $R^* = 0.10$, then asymptotically $R_{1\text{NN}} \le 2(0.1)(0.9) = 0.18$.

## Common confusions
- *"k-NN has no hyperparameters because it has no training."* → $k$, the distance, the weighting and the feature scaling are all hyperparameters; tune them with cross-validation.
- *"Training error 0 at $k=1$ means a great model."* → Each point is its own nearest neighbour; that is memorisation. Judge on held-out data.
- *"Larger $k$ is always safer."* → Too large a $k$ underfits and lets the majority class win everywhere, especially with class imbalance.
- *"More features always help k-NN."* → Irrelevant features add noise to every distance and worsen the curse of dimensionality. Feature selection matters more for k-NN than for most models.
- *"Approximate NN is a different model."* → It is the same model with a faster, slightly inexact neighbour search; accuracy usually barely changes.

## Check yourself

> [!question]- Why must you scale features before k-NN, but not before a decision tree?
> k-NN adds up coordinate differences in one distance, so large-unit features dominate. Trees split on one feature at a time with thresholds, which are unaffected by monotone rescaling.

> [!question]- What happens to the predictions as $k\to N$?
> Every query uses all training points, so classification always returns the overall majority class and regression the global mean: maximal bias, minimal variance.

> [!question]- What is the training cost and the naive prediction cost of k-NN?
> Training $O(1)$ beyond storing $N\times D$ data; each prediction $O(ND)$ for the distances (plus selecting the $k$ smallest).

> [!question]- In 50 dimensions with uniform data, what edge length does a sub-cube need to hold 1% of the data?
> $0.01^{1/50} = e^{\ln 0.01/50}\approx e^{-0.092}\approx 0.91$, i.e. 91% of each axis.

> [!question]- What does the Cover–Hart result guarantee, and what does it not?
> Asymptotically (infinite data) 1-NN's error is at most twice the Bayes error. It gives no guarantee for any finite sample size, and convergence can be very slow in high dimensions.

## Practice
[k-Nearest Neighbors - Exercises](k-Nearest%20Neighbors%20-%20Exercises.ipynb): lazy learning, the role of $k$, distance concentration, k-d trees and ANN; by hand: 1-D votes, weighted regression, four distances, scaling, neighbourhood size, Cover–Hart; in code: vectorised distances, a k-NN classifier and weighted regressor, choosing $k$ by CV, scaling on the wine data, the curse of dimensionality and a Cover–Hart simulation.

**Project:** [[Project - kNN and the Curse of Dimensionality]] – kNN from scratch and the curse of dimensionality

## Learn more
- [scikit-learn – nearest neighbors](https://scikit-learn.org/stable/modules/neighbors.html)
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 2
- [Stanford CS231n – image classification notes](https://cs231n.github.io/classification/): k-NN on images, L1 vs L2 distance and choosing $k$ with validation
