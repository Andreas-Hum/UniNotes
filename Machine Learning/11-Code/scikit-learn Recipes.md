---
tags: [ml, code, sklearn]
---
# scikit-learn Recipes

> [!summary] In one sentence
> scikit-learn gives every model and preprocessing step the same `fit` / `transform` / `predict` interface, so a whole workflow (split, scale, model, cross-validate, tune, report) is a few lines, and wrapping preprocessing + model in a `Pipeline` is what keeps the evaluation honest (no leakage).

## Intuition first

Think of a recipe card in a kitchen. Each step (wash, chop, cook) has a standard interface: it takes ingredients and hands something to the next step. In scikit-learn:
- A **transformer** (e.g. `StandardScaler`, `PCA`) has `fit(X)` (learn its parameters, e.g. means and stds) and `transform(X)` (apply them).
- An **estimator/predictor** (e.g. `SVC`, `LogisticRegression`) has `fit(X, y)` (learn the model) and `predict(X)` (use it); classifiers often add `predict_proba` or `decision_function`.
- A **pipeline** chains them: `fit` calls `fit_transform` on each transformer in turn and `fit` on the final model; `predict` calls `transform` through the chain and then `predict`.

The golden rule: **anything that learns from data must learn only from training data.** The test set is a sealed envelope you open once at the end. Cross-validation repeats this discipline inside the training set: each fold is a mini test set, and the pipeline guarantees the scaler is re-fit without seeing it.

**What problem does it solve?** Honest model selection with almost no boilerplate: the same code works for any model, and the main ways of fooling yourself (leakage, tuning on the test set, unstratified splits) are prevented by construction.

![Train/test split, then 5-fold CV with the pipeline re-fit on each training part](../../Attachments/ML%20Animations/scikit-learn%20Recipes%20-%20pipeline%20inside%205-fold%20cross-validation.gif)
*Watch the test set (red) get locked away first; then each row is one fold: the pipeline (scaler + model) is fit only on the blue parts and scored on the orange part, and the CV score is the mean of the five fold scores.*

## The recipes, explained

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
```
The imports are the toolbox: model selection utilities, linear models (`LogisticRegression` for classification, `Ridge` for regression), tree ensembles ([[Ensemble Methods]]), kernel SVMs ([[Support Vector Machines]]) and metrics. Any of the models can be dropped into the pipelines below in place of `SVC`, because they all share the same interface.

### 1. Split once, stratified
```python
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
```
- Holds out 20% as the final test set.
- `stratify=y` keeps the class proportions the same in both parts. Without it, a rare class (say 5% of data) could end up with very few test examples by chance, making the test score noisy or misleading.
- `random_state=0` makes the split reproducible. Shuffling is on by default (`shuffle=True`); for time series you must *not* shuffle (train on the past, test on the future).

### 2. Pipeline + cross-validation
```python
# Pipeline avoids leakage (scaler is fit inside each CV fold)
pipe = make_pipeline(StandardScaler(), SVC(kernel="rbf"))
scores = cross_val_score(pipe, X_tr, y_tr, cv=StratifiedKFold(5, shuffle=True, random_state=0))
```
- `StandardScaler` learns each feature's mean and standard deviation in `fit` and computes $(x-\mu)/\sigma$ in `transform` (population std, `ddof=0`). Scaling matters for the RBF SVM because its kernel uses distances; unscaled features with large units would dominate.
- **Why the pipeline avoids leakage**: if you scaled `X_tr` once and then cross-validated, each validation fold would have contributed to the mean/std used to train on the other folds. With the pipeline, `cross_val_score` clones it and calls `fit` on the 4 training folds only, so the scaler never sees the validation fold. The same holds for feature selection, imputation, PCA, target encoding: every learned step belongs in the pipeline.
- `StratifiedKFold(5, shuffle=True, random_state=0)`: 5 folds, each with the class proportions of the whole, shuffled reproducibly. `scores` is an array of 5 accuracies; report `scores.mean()` and `scores.std()` (the spread tells you how much to trust differences between models). See [[Cross-Validation and Model Selection]].
- To compare models fairly, pass the **same** `cv` object (same folds) to each, so differences come from the models, not from luckier splits.

### 3. Hyperparameter search
```python
# Hyperparameter search
grid = GridSearchCV(pipe, {"svc__C": [0.1, 1, 10, 100], "svc__gamma": [1e-3, 1e-2, 1e-1]}, cv=5)
grid.fit(X_tr, y_tr)
print(grid.best_params_, grid.score(X_te, y_te))

print(classification_report(y_te, grid.predict(X_te)))
```
- `make_pipeline` names steps after their lowercase class (`standardscaler`, `svc`); `step__param` reaches inside the pipeline, so `svc__C` is the SVM's `C`.
- The grid has $4\times3=12$ combinations; with `cv=5` that is 60 fits, plus **1 refit** of the best combination on all of `X_tr` (`refit=True` by default) = 61 fits. For a classifier, `cv=5` means `StratifiedKFold(5)` (not shuffled).
- `C` trades margin width against training errors (large `C` = less regularization); `gamma` is the RBF width (large `gamma` = very local, wiggly boundary). Log-spaced grids are standard because their effect is multiplicative.
- `grid.score(X_te, y_te)` evaluates the refit best model **once** on the untouched test set. Never pick hyperparameters by looking at the test score: that turns the test set into a validation set and the number becomes optimistic.
- `classification_report` prints, per class, **precision** (of predicted positives, how many are right), **recall** (of actual positives, how many were found), **F1** (their harmonic mean) and **support** (number of true instances), plus accuracy and macro (unweighted mean over classes) and weighted (by support) averages.
- `confusion_matrix(y_te, y_pred)` has rows = true class and columns = predicted class (binary: `[[TN, FP], [FN, TP]]`). `roc_auc_score(y_te, scores)` needs continuous **scores**, not hard labels: use `grid.decision_function(X_te)` for an SVM (or `predict_proba(...)[:, 1]` for models that have it).

### 4. Unsupervised
```python
# Unsupervised
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
Z = PCA(n_components=2).fit_transform(StandardScaler().fit_transform(X))
labels = KMeans(n_clusters=3, n_init=10).fit_predict(Z)
```
- Standardize first so no feature dominates the variance (PCA) or the distances (k-means) just because of its units.
- `PCA(n_components=2)` projects onto the top two principal directions ([[PCA]]); `fit_transform` = `fit` then `transform` in one call.
- `KMeans(n_clusters=3, n_init=10)` runs k-means from 10 random initializations and keeps the best (lowest inertia), because a single run can get stuck in a poor local optimum. `fit_predict` returns a cluster label per sample.
- Alternatives: `DBSCAN` (density-based, finds arbitrary shapes and noise, no $k$), `GaussianMixture` (soft, probabilistic clusters fitted by EM, [[Gaussian Mixture Models and EM]]). See [[Clustering]].
- Clustering on 2 PCA components is mainly for visualization; for the clustering itself you may keep more components.

### Recipes the exercises add
**Mixed numeric + categorical columns** with `ColumnTransformer`:
```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
pre = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
])
pipe = make_pipeline(pre, LogisticRegression(max_iter=1000))
```
Each column group gets its own transformer, all fit inside CV. `handle_unknown="ignore"` stops a category seen only in the test set from crashing `transform`.

**A custom transformer**: inherit `BaseEstimator, TransformerMixin`, learn in `fit` and store learned attributes with a trailing underscore, `return self`, apply in `transform`:
```python
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
class Clipper(BaseEstimator, TransformerMixin):
    def __init__(self, q=0.01):
        self.q = q
    def fit(self, X, y=None):
        self.lo_, self.hi_ = np.quantile(X, [self.q, 1 - self.q], axis=0)
        return self
    def transform(self, X):
        return np.clip(X, self.lo_, self.hi_)
```
Hyperparameters are stored unchanged in `__init__` so `clone` and `GridSearchCV` (`clipper__q`) work. A custom classifier is the same with `ClassifierMixin`, a `classes_` attribute and a `predict` method.

**Choosing a decision threshold**: `predict` uses 0.5 (or 0 for decision functions). If false negatives are costly, pick a threshold on validation scores (e.g. from `precision_recall_curve`) and apply `(proba >= t)`; never choose it on the test set.

Concepts: [[Cross-Validation and Model Selection]], [[Support Vector Machines]], [[Ensemble Methods]], [[Clustering]], [[PCA]], [[Gaussian Mixture Models and EM]].

## Worked example

**Metrics from a confusion matrix.** 100 test cases: TP = 40, FN = 10, FP = 5, TN = 45.
1. Accuracy $=\frac{40+45}{100}=0.85$.
2. Precision $=\frac{40}{40+5}\approx0.89$; recall $=\frac{40}{40+10}=0.80$.
3. F1 $=\frac{2\cdot0.89\cdot0.80}{0.89+0.80}\approx0.84$.

**ROC AUC as a ranking probability.** Positive scores $\{0.9,0.6\}$, negative scores $\{0.7,0.2\}$. Of the 4 (positive, negative) pairs, the positive is ranked higher in 3 ($0.9>0.7$, $0.9>0.2$, $0.6>0.2$), so AUC $=3/4=0.75$: the probability that a random positive outranks a random negative.

**What StandardScaler computes.** Feature values $[1,2,3]$: $\mu=2$, $\sigma=\sqrt{2/3}\approx0.816$, scaled values $\approx[-1.22,0,1.22]$.

## Common confusions
- **"I scaled the data before splitting, but it's just scaling."** → It is leakage: the test set's statistics influenced training. Usually small for scaling, but large for feature selection or target encoding. Put it in the pipeline.
- **"The best CV score from GridSearchCV is my expected test performance."** → It is optimistically biased (you picked the max over many configurations). The held-out test score, or nested CV, is the honest estimate.
- **"`cross_val_score` returns a trained model."** → It returns scores only; the clones it trains are discarded. Fit the pipeline (or use `grid.best_estimator_`) to get a model.
- **"`roc_auc_score(y, model.predict(X))`."** → `predict` gives hard labels, collapsing the ROC curve to one point. Pass scores or probabilities.
- **"High accuracy means a good classifier."** → With 95% negatives, predicting "negative" always gets 95%. Read per-class recall/precision in the report.

## Check yourself

> [!question]- How many fits does `GridSearchCV` run for a 3×4 grid with `cv=10`?
> $12\times10=120$, plus one refit on the full training set: 121.

> [!question]- Why must `StandardScaler` be inside the pipeline passed to `cross_val_score`?
> So that it is fit on the training folds only; otherwise the validation fold's mean and std leak into training and the CV score is optimistic.

> [!question]- What does `stratify=y` guarantee, and when would you not shuffle?
> The same class proportions in train and test. Do not shuffle when order matters (time series), and keep groups (e.g. all images of one patient) on one side with `GroupKFold`.

> [!question]- How do you set the RBF `gamma` of the SVC inside `make_pipeline(StandardScaler(), SVC())` in a grid?
> Key `"svc__gamma"`: lowercase class name, two underscores, parameter name.

> [!question]- Your report shows class 1 recall 0.30 and precision 0.90. What does that mean?
> When the model says class 1 it is usually right, but it finds only 30% of the actual class-1 cases: too conservative. Lower the decision threshold or rebalance (e.g. `class_weight="balanced"`).

## Practice
[scikit-learn Recipes - Exercises](scikit-learn%20Recipes%20-%20Exercises.ipynb): fit/transform/predict, leakage and pipelines, stratification, reading reports, counting GridSearchCV fits, metrics and ROC AUC by hand, then code: split-pipeline-CV, demonstrating leakage, grid search, ColumnTransformer, custom transformer and classifier, comparing models on the same folds, threshold choice and the unsupervised recipe.

## Learn more
- [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html)
- [scikit-learn – Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html): the official explanation of leakage and why pipelines fix it.
- [scikit-learn – Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)
