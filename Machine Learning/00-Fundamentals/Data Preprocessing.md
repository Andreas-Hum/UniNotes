---
tags: [ml, fundamentals, data]
---
# Data Preprocessing

> [!summary] In one sentence
> Preprocessing puts raw data into a shape a model can learn from fairly: features on comparable scales, missing values handled honestly, outliers understood, and class imbalance accounted for, with every statistic learned **from the training set only**.

## Intuition first

Imagine judging how similar two people are from their **income in euros** and their **age in years**. A €1 000 difference in income swamps a 40-year age difference, purely because of the units. Any algorithm that measures distances (k-NN, SVMs, k-means) or takes gradient steps (linear models, neural nets) gets fooled in the same way. **Scaling** removes the arbitrary units.

Real data are also messy: a sensor drops out (**missing values**), someone types 1000 instead of 100 (**outliers**), or only 1 in 100 transactions is fraud (**imbalance**). Each of these can quietly ruin a model, and each has a toolkit.

The golden rule underneath it all: preprocessing is part of the model. Its parameters (means, medians, category lists) are **fitted on the training data**, then applied unchanged to validation and test data, exactly like model weights.

![Standardising a stretched, off-centre cloud](../../Attachments/ML%20Animations/Data%20Preprocessing%20-%20standardisation.gif)
*Watch two moves: subtracting $\mu$ slides the cloud to the origin, dividing by $\sigma$ squeezes the wide feature and stretches the narrow one until both have spread 1.*

## Scaling
- **Min–max**: $x' = \frac{x-x_{min}}{x_{max}-x_{min}}$
- **Standardization (z-score)**: $x' = \frac{x-\mu}{\sigma}$
- **Robust**: use median and IQR, resists outliers.

In words:
- **Min–max** maps the training range to $[0, 1]$. A single extreme value defines the range, so it squashes everything else.
- **Z-score** gives mean $0$ and standard deviation $1$. $\mu$ and $\sigma$ are themselves pulled by outliers, but less violently than min and max.
- **Robust**: $x' = \frac{x - \operatorname{median}(x)}{\mathrm{IQR}(x)}$ with $\mathrm{IQR} = Q_3 - Q_1$ (75th minus 25th percentile). Median and quartiles ignore the extreme tail, so the bulk of the data keeps a sensible spread.

Needed for: [[Gradient Descent]], [[k-Nearest Neighbors]], [[Support Vector Machines]], [[PCA]], regularized models. Not needed for tree models ([[Decision Trees]]).

**Why exactly these?**
- *Gradient descent*: with features on very different scales the loss surface becomes a long thin valley, and GD zig-zags; scaling makes it rounder and convergence faster.
- *k-NN, SVM (RBF kernel)*: rely on Euclidean distances, which are dominated by large-unit features.
- *PCA*: finds directions of maximal variance, so an unscaled large-unit feature *is* the first component.
- *Regularized models*: the penalty $\lambda\lVert w\rVert^2$ treats all weights equally, which is only fair if the features share a scale.
- *Trees* split on thresholds of one feature at a time; any monotone rescaling leaves the splits (and predictions) unchanged.

![Three scalers applied to data with one outlier](../../Attachments/ML%20Animations/Data%20Preprocessing%20-%20scalers%20and%20outliers.gif)
*Watch the four normal points: min–max and z-score crush them together because of the outlier, robust scaling keeps them spread out.*

## Worked example: three scalers on five numbers

$x = \{1, 2, 3, 4, 100\}$.

| | 1 | 2 | 3 | 4 | 100 |
|---|---|---|---|---|---|
| Min–max $(x-1)/99$ | 0 | 0.010 | 0.020 | 0.030 | 1 |
| Z-score ($\mu = 22$, $\sigma \approx 39.01$) | −0.538 | −0.513 | −0.487 | −0.461 | 2.00 |
| Robust (median 3, $Q_1 = 2$, $Q_3 = 4$, IQR 2) | −1 | −0.5 | 0 | 0.5 | 48.5 |

($\sigma$ here is the population standard deviation: $\sigma^2 = \frac15\sum (x_i - 22)^2 = 7610/5 = 1522$.)

**Masking.** A common outlier rule flags $\lvert z\rvert > 3$. Here the outlier has $z \approx 2.0$ and is **not** flagged, because it inflated $\sigma$ itself. The IQR rule flags points outside $[Q_1 - 1.5\,\mathrm{IQR},\ Q_3 + 1.5\,\mathrm{IQR}] = [-1, 7]$, which catches 100. Robust statistics do not let the outlier hide itself.

## Missing data
MCAR / MAR / MNAR. Options: drop, mean/median/mode, kNN or model-based imputation, missing-indicator.

**The three mechanisms** (whether a value is missing, $M$, depends on what?):
- **MCAR** (missing completely at random): $M$ is independent of everything. A lab sample dropped on the floor. Dropping rows loses data but does not bias.
- **MAR** (missing at random): $M$ depends only on *observed* variables. Older patients skip the online survey more often, and age is recorded. Imputation using the observed variables can correct for it.
- **MNAR** (missing not at random): $M$ depends on the missing value itself. People with very high income refuse to report income. No imputation from observed data fully fixes this; the fact of missingness is informative.

**Why mean imputation is dangerous.** Filling a fraction $m$ of values with the mean adds points with zero deviation, so the variance shrinks to roughly $(1-m)\,\sigma^2$ and correlations with other features weaken. kNN imputation (average of the $k$ most similar rows) or model-based imputation preserves structure better. A **missing-indicator** column (1 if the value was missing) lets the model learn from the missingness itself, which is crucial under MNAR.

## Outliers
Inspect (box plot, z-score, IQR), winsorize, or use robust losses (Huber). See [[Anomaly Detection]].

First ask: **error or signal?** A height of 2.5 m is a typo; a €1 M transaction might be exactly the fraud you want to detect. Never delete outliers blindly.
- **Winsorize**: clip values to, say, the 1st and 99th percentile.
- **Huber loss** is quadratic for small residuals and linear for large ones, so a single outlier cannot dominate the fit:
$$L_\delta(r) = \begin{cases} \tfrac12 r^2 & \lvert r\rvert \le \delta \\ \delta\big(\lvert r\rvert - \tfrac12\delta\big) & \lvert r\rvert > \delta \end{cases}$$

## Imbalance
Class weights, resampling (SMOTE), threshold moving, PR-AUC. See [[Model Evaluation and Metrics]].

- **Class weights**: multiply each example's loss by a class weight. "Balanced" weights are $w_c = \frac{N}{K\, N_c}$ ($N$ examples, $K$ classes, $N_c$ in class $c$), so every class contributes equally in total.
- **Resampling**: undersample the majority, or oversample the minority. **SMOTE** creates synthetic minority points on the line between a minority point and one of its minority neighbours: $x_{new} = x_i + u\,(x_{nn} - x_i)$, $u \sim \mathcal U(0,1)$. Resample **only the training folds**.
- **Prior correction**: training on rebalanced data inflates predicted probabilities. If the true positive rate is $\pi$ and the training positive rate was $\pi'$, correct the odds: $\text{odds}_{true} = \text{odds}_{model}\cdot\frac{\pi/(1-\pi)}{\pi'/(1-\pi')}$.
- **Threshold moving**: keep the model, choose the decision threshold on validation data to optimise the metric you care about (F1, recall at a given precision, expected cost).
- **Metrics**: use PR-AUC, F1, or recall/precision, not accuracy.

**Example.** 900 negatives, 100 positives, $K = 2$: $w_{neg} = 1000/(2\cdot 900) \approx 0.556$, $w_{pos} = 1000/(2\cdot100) = 5$. Each class now carries total weight 500.

## Pipeline rule
Compute statistics on **train only**, apply to val/test.

Inside cross-validation this means re-fitting the scaler, imputer and resampler **inside each fold**; scikit-learn's `Pipeline` does this automatically. Fitting them on all data first leaks information from the validation fold into training.

## Common confusions
- **"Standardization makes data Gaussian."** It only shifts and rescales; the shape (skew, outliers) is unchanged. Use a log or Box–Cox transform for skew.
- **"Tree models need scaling too."** They do not; splits are invariant to monotone transforms. (They can still benefit from imputation strategies.)
- **"Oversampling before the split is fine."** Copies or SMOTE interpolations of a validation point end up in training: a leak.
- **"Outliers should always be removed."** Sometimes they are the signal (fraud, faults).
- **"Mean imputation is neutral."** It shrinks variance and weakens correlations; add an indicator or use a better imputer.

## Check yourself

> [!question]- Which of these need scaling: k-NN, random forest, lasso, PCA, gradient-boosted trees?
> k-NN, lasso and PCA. The tree ensembles do not.

> [!question]- Patients with severe symptoms are too ill to complete a questionnaire, so their symptom scores are missing. Which mechanism is that?
> MNAR: missingness depends on the unobserved value itself.

> [!question]- Why can the $\lvert z\rvert > 3$ rule miss a huge outlier in a small sample?
> The outlier inflates $\sigma$ (and shifts $\mu$), so its own z-score stays small: masking. The IQR rule is robust to this.

> [!question]- A model trained on 50/50 rebalanced data predicts $p = 0.5$ for a case. The true positive rate is 10 %. What is the corrected probability?
> Model odds $= 1$. Correction factor $= \frac{0.1/0.9}{0.5/0.5} = 1/9$. Corrected odds $= 1/9$, so $p = 0.1$.

## Practice
[Data Preprocessing - Exercises](Data%20Preprocessing%20-%20Exercises.ipynb)

## Learn more
- [scikit-learn – preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
- [scikit-learn – imputation](https://scikit-learn.org/stable/modules/impute.html)
- [imbalanced-learn (SMOTE and friends)](https://imbalanced-learn.org/stable/)
