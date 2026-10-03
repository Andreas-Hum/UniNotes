---
tags: [ml, supervised, ensemble]
status: not-started
notebook: not-started
level:
reviewed:
---
# Ensemble Methods

> [!summary] In one sentence
> Combine many weak/diverse models for lower error: averaging many *independent-ish* high-variance models cancels their noise (bagging, random forests), while adding models *sequentially*, each fixing the previous ones' mistakes, removes bias (boosting).

## Intuition first

Ask 100 people to guess the number of sweets in a jar. Individually they are way off, but the *average* guess is often remarkably close: each person's error is partly random, and random errors cancel when you average. That only works if the guessers are not all copying the same (wrong) person, so **diversity** is the secret ingredient. This is the "wisdom of crowds" idea behind **bagging** and **random forests**.

Boosting is a different story: a student revising for an exam. After the first practice test they focus on the questions they got wrong; after the second, on the ones they *still* get wrong; and so on. Each round is a small, simple correction, but the sum of many corrections becomes an expert. That is **AdaBoost** and **gradient boosting**.

So there are two levers:
- **Average in parallel** to reduce **variance** (use flexible, low-bias, high-variance base models such as deep [[Decision Trees]]).
- **Add in sequence** to reduce **bias** (use simple, high-bias base models such as stumps or depth-3 trees).

See [[Bias-Variance Tradeoff]].

![Six fully grown trees trained on bootstrap samples, then their average](../../Attachments/ML%20Animations/Ensemble%20Methods%20-%20bagging%20average.gif)
*Watch each coloured tree chase its own bootstrap sample (dimmed points were left out of that sample), then see the yellow average of 6 and finally 40 trees: the individual wobbles cancel.*

## The menu

| Method | Idea | Reduces |
|---|---|---|
| **Bagging** | train on bootstrap samples, average | variance |
| **Random Forest** | bagged [[Decision Trees]] + random feature subset per split | variance, decorrelates trees |
| **AdaBoost** | reweight misclassified points, weighted vote | bias |
| **Gradient Boosting** | fit each tree to the negative gradient (residuals) of the loss | bias |
| **XGBoost / LightGBM / CatBoost** | fast, regularized gradient boosting | state of the art on tabular data |
| **Stacking** | meta-learner on base model predictions | both |
| **Voting** | hard/soft vote of heterogeneous models | variance |

## The math, step by step

### Why averaging helps: the variance of an average
Suppose $B$ predictors $f_1,\dots,f_B$ each have variance $\sigma^2$ and every pair has correlation $\rho$. Their average $\bar f=\frac1B\sum_bf_b$ has

$$\operatorname{Var}(\bar f)=\frac1{B^2}\Big(\sum_b\operatorname{Var}f_b+\sum_{b\ne c}\operatorname{Cov}(f_b,f_c)\Big)=\frac{B\sigma^2+B(B-1)\rho\sigma^2}{B^2}=\rho\sigma^2+\frac{1-\rho}{B}\sigma^2.$$

In words: the second term vanishes as you add models, but the first term $\rho\sigma^2$ does **not**. More trees never hurt, but beyond a point only *lower correlation* helps. The bias of $\bar f$ equals the bias of a single model, so averaging does nothing for bias.

### Bagging (bootstrap aggregating)
Draw $B$ bootstrap samples (size $N$, with replacement), fit a model to each, and average the predictions (regression) or take a majority vote (classification).

A given point is left out of one bootstrap sample with probability $(1-\tfrac1N)^N\to e^{-1}\approx0.368$, so each model never sees about 37% of the data. Predicting each training point using only the models that did not see it gives the **out-of-bag (OOB) error**:
- Random forests give out-of-bag (OOB) error for free, a nearly unbiased estimate of test error without a separate validation set.

### Random forests: decorrelate the trees
If one feature is very strong, every bagged tree splits on it at the root and the trees look alike ($\rho$ is large). A random forest, at *every split*, only considers a random subset of `max_features` features (typically $\sqrt d$ for classification, about $d/3$ for regression). Some trees are forced to do without the strong feature, which lowers $\rho$ and therefore the $\rho\sigma^2$ floor, at the cost of slightly higher variance per tree.

### AdaBoost
Labels $y_i\in\{-1,+1\}$, weights $w_i=1/N$ initially. For $m=1,\dots,M$:
1. Fit a weak learner $h_m$ (e.g. a stump) using weights $w_i$.
2. Weighted error $\varepsilon_m=\sum_iw_i\,\mathbb 1[h_m(x_i)\ne y_i]$ (weights sum to 1).
3. Model weight $\alpha_m=\tfrac12\ln\frac{1-\varepsilon_m}{\varepsilon_m}$: accurate learners get a big say; $\varepsilon=0.5$ (coin flip) gets zero.
4. Reweight $w_i\leftarrow w_i\,e^{-\alpha_my_ih_m(x_i)}$, then normalise: misclassified points ($y_ih_m=-1$) are multiplied by $e^{\alpha_m}>1$, correct ones by $e^{-\alpha_m}<1$.

Predict $H(x)=\operatorname{sign}\big(\sum_m\alpha_mh_m(x)\big)$. That $\alpha_m$ is not arbitrary: AdaBoost is forward stagewise minimisation of the **exponential loss** $\sum_ie^{-y_iF(x_i)}$, and minimising over $\alpha$ for a fixed $h$ gives exactly the formula above.

### Gradient boosting
Build an additive model $F_M(x)=F_0(x)+\nu\sum_{m=1}^Mh_m(x)$ for any differentiable loss $L(y,F)$:
1. $F_0$ = best constant (the mean for squared loss, the log-odds of the base rate for log-loss).
2. Compute **pseudo-residuals** $r_i=-\dfrac{\partial L(y_i,F)}{\partial F}\Big|_{F=F_{m-1}(x_i)}$.
3. Fit a small regression tree $h_m$ to $(x_i,r_i)$.
4. Update $F_m=F_{m-1}+\nu\,h_m$ with learning rate $\nu\in(0,1]$.

This is [[Gradient Descent]] in *function space*: the residual vector is the direction of steepest descent of the loss at the training points, and the tree generalises that direction to new $x$. For squared loss $L=\tfrac12(y-F)^2$ we get $r=y-F$, literally "fit each tree to the residuals". For log-loss with $p=\sigma(F)$ we get $r=y-p$.

![Gradient boosting fitting residuals round by round](../../Attachments/ML%20Animations/Ensemble%20Methods%20-%20gradient%20boosting.gif)
*Watch the bottom panel: each green tree $h_m$ is fit to the red residuals, a step of size $\nu=0.3$ is added to the yellow model, and the residuals shrink towards zero. By $m=60$ the training MSE has fallen below the noise level, a reminder that boosting can overfit if you never stop.*

## Worked example

**AdaBoost, one round.** 10 points with weights $0.1$; a stump misclassifies 3 of them.
- $\varepsilon=0.3$, $\alpha=\tfrac12\ln\frac{0.7}{0.3}=\tfrac12\ln2.33\approx0.424$.
- Misclassified: $0.1\cdot e^{0.424}=0.153$; correct: $0.1\cdot e^{-0.424}=0.0655$.
- Totals before normalising: $3\cdot0.153=0.458$ and $7\cdot0.0655=0.458$, sum $0.917$. After normalising, each misclassified point weighs $0.167$ and each correct one $0.071$; the misclassified points now hold exactly half the weight, so the old stump would have error $0.5$ and the next stump must find something new.

**Gradient boosting, squared loss.** Targets $y=(2,4,9)$, $\nu=0.5$.
- $F_0=\bar y=5$; residuals $r=(-3,-1,4)$.
- A stump groups points 1, 2 (leaf value $-2$) and point 3 (leaf value $4$).
- $F_1=5+0.5\cdot(-2,-2,4)=(4,4,7)$; new residuals $(-2,0,2)$, the squared error dropped from $26$ to $8$.

## Practical knobs
- Boosting hyperparameters: learning rate (small + many trees), depth (3–8), subsampling.
  - A small $\nu$ (0.01–0.1) with many trees generalises better than a few big steps (shrinkage is regularisation); pick the number of trees by early stopping on a validation set.
  - Shallow trees (depth 3–8) keep each learner weak; depth controls the order of feature interactions the model can express.
  - Fitting each tree on a random subsample of rows (and/or columns) adds randomness, which reduces variance and speeds things up (stochastic gradient boosting).
- Random forests barely overfit when adding trees; tune `max_features` and leaf size, then use "enough" trees (the OOB error flattens).
- XGBoost / LightGBM / CatBoost add L1/L2 penalties on leaf values, second-order (Newton) steps, histogram-based split finding, and clever handling of missing values and categorical features; they are usually the first thing to try on tabular data.

## Stacking and voting
- **Voting**: hard voting takes the majority class, soft voting averages predicted probabilities (usually better when the models are calibrated). Works best when the models are *different* (e.g. a forest, an SVM and a logistic regression), because their errors are less correlated.
- **Stacking**: train a meta-learner (often a regularised [[Logistic Regression]]) on the base models' predictions. These must be **out-of-fold** predictions from [[Cross-Validation and Model Selection|cross-validation]]; predictions on data the base models were trained on are over-confident (a deep tree predicts its training points perfectly), so the meta-learner would learn to trust the most overfitted model.

## Feature importance
- Feature importance: impurity-based (biased) vs. permutation importance (preferred).
- *Impurity-based* (mean decrease in impurity): sum the impurity reductions of all splits on a feature, averaged over trees. It is computed on the training data and biased towards continuous or high-cardinality features, which offer many thresholds and can "win" splits by chance even when they are pure noise.
- *Permutation importance*: shuffle one feature's column in a held-out set and measure how much the score drops. It measures what the model actually relies on for generalisation. (Caveat: correlated features share credit and can each look unimportant.)

## Common confusions
- *"Bagging reduces bias."* → It reduces variance; the average has the same bias as one tree. Bagging a stable, low-variance model (like linear regression) therefore achieves almost nothing.
- *"More trees in a random forest cause overfitting."* → No; the error plateaus. More boosting rounds *can* overfit, which is why you use a small learning rate and early stopping.
- *"Boosting just averages trees."* → Boosting trees are fitted sequentially to the current errors and *added*; they are not interchangeable and are useless on their own.
- *"Stacking can use in-sample predictions."* → That leaks the training labels into the meta-learner; use out-of-fold predictions.
- *"Impurity importance tells me which features matter."* → It can rank a random continuous column above a truly informative binary one; prefer permutation importance on held-out data.

## Check yourself

> [!question]- With $\sigma^2=1$, $\rho=0.5$, what is the variance of an average of 10 models, and of infinitely many?
> $0.5+\frac{0.5}{10}=0.55$; as $B\to\infty$ it tends to $\rho\sigma^2=0.5$.

> [!question]- Five independent classifiers are each correct with probability 0.6. Is their majority vote better than one of them?
> Yes: $P(\ge3\text{ correct})=10(0.6^3)(0.4^2)+5(0.6^4)(0.4)+0.6^5=0.346+0.259+0.078\approx0.68>0.6$. If they were perfectly correlated, it would stay at 0.6.

> [!question]- What does a weak learner with weighted error $\varepsilon=0.5$ contribute to AdaBoost?
> $\alpha=\tfrac12\ln1=0$: nothing, it is a coin flip on the current weights.

> [!question]- Which base learner suits bagging, and which suits boosting?
> Bagging: deep, low-bias/high-variance trees (variance is what averaging removes). Boosting: shallow, high-bias trees such as stumps (boosting removes bias, and weak learners keep each step small).

> [!question]- What is the pseudo-residual for squared loss $\tfrac12(y-F)^2$?
> $-\partial L/\partial F=y-F$, the ordinary residual.

## Practice
[Ensemble Methods - Exercises](Ensemble%20Methods%20-%20Exercises.ipynb): variance vs bias reducers, random feature subsets, which importance to trust, stacking without leakage; by hand: variance of an average, OOB probability, majority-vote accuracy, one round of AdaBoost, gradient boosting by hand, log-loss pseudo-residuals, deriving AdaBoost's $\alpha$; in code: bagging with OOB, AdaBoost with stumps, gradient boosting for regression, decorrelating trees, permutation vs impurity importance.

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 8
- [scikit-learn – ensembles](https://scikit-learn.org/stable/modules/ensemble.html)
- [XGBoost docs](https://xgboost.readthedocs.io/)
- [StatQuest videos](https://statquest.org/video_index.html): Random Forests, AdaBoost and the four-part Gradient Boost series
- [Elements of Statistical Learning (free)](https://hastie.su.domains/ElemStatLearn/) ch. 10 (boosting) and ch. 15 (random forests)
