---
tags: [ml, practice]
---
# Common Pitfalls

> [!summary] In one sentence
> Most disappointing ML results come not from the wrong model but from a handful of recurring mistakes (information leaking from test to train, evaluating with the wrong metric or on the wrong split, and silent numerical or code bugs), and each has a simple, mechanical fix.

## Intuition first

A machine-learning experiment is a **simulation of the future**: the test set plays the role of data the model will meet after deployment. Almost every pitfall below breaks that simulation in one of three ways:

1. **The future leaks into the past** (data leakage, tuning on the test set, shuffled time series, duplicates across splits). The model, or *you*, has peeked at the exam, so the score is too good to be true.
2. **The scoreboard is wrong** (accuracy on imbalanced data, no baseline, misreading plots, confusing correlation with causation). The number is honest but answers the wrong question.
3. **The code lies quietly** (transposed matrices, broadcasting, forgetting `model.eval()`, overflow, irreproducible runs). Python raises no error; you just get a wrong number.

A good habit is to ask of every result: *"Could I have produced this number without any real signal?"* If the answer is yes (for example a 99% accuracy on 1% fraud), you have found a pitfall.

## The table

| Pitfall | Fix |
|---|---|
| **Data leakage** (scaling on all data, target in features, future info) | pipelines, split first, time-aware splits |
| Tuning on the test set | validation set / nested CV ([[Cross-Validation and Model Selection]]) |
| Accuracy on imbalanced data | PR-AUC, F1, baselines ([[Model Evaluation and Metrics]]) |
| Not scaling features for distance/gradient methods | [[Data Preprocessing]] |
| Duplicates/groups across train & test | group k-fold |
| Misreading t-SNE | [[Dimensionality Reduction]] |
| Confusing correlation with causation | experiments, causal inference |
| Ignoring baseline | always compare to dummy and simple model |
| Wrong shape/transposed matrices | assert shapes ([[NumPy Snippets]]) |
| Train/eval mode bugs (dropout, BN) | `model.eval()` ([[PyTorch Recipes]]) |
| Non-reproducible results | seeds, logged configs |
| Log of zero / overflow | log-sum-exp, clip probabilities |

The rest of this note explains *why* each row happens and how to recognise it.

## 1. Data leakage

**Leakage** means information that will not be available at prediction time influences training or model selection.

- **Preprocessing on all data.** Fitting a scaler, imputer, or (much worse) a **feature selector** on the full dataset before splitting lets test rows shape the transformation. Feature selection using the labels is dramatic: with 100 samples and 2000 pure-noise features, picking the 20 features most correlated with the labels on *all* data and then cross-validating reports around 78% accuracy on data with no signal at all; doing the selection inside each fold gives chance level.
- **Target in features.** A column computed *after* the outcome (a "diagnosis code", a "refund issued" flag) is basically the label in disguise. Symptom: one feature has a single-feature ROC-AUC near 1. Ask for every column *when* it becomes available.
- **Future information.** In time series, shuffled k-fold lets the model see $t-1$ and $t+1$ when predicting $t$, so it only interpolates. A $k$-NN on the time index can score $R^2\approx0.97$ with shuffled CV and strongly negative with a forward-chaining split. Use `TimeSeriesSplit`: always train on the past, test on the future.

![Leaky versus correct order: fitting the scaler on all rows lets test rows influence training; fitting on training rows only and then transforming the test rows does not](../../Attachments/ML%20Animations/Common%20Pitfalls%20-%20preprocessing%20leakage.gif)

*Watch which squares the brace covers: in the leaky row the orange test rows are inside the fit, in the correct row only the blue training rows are, and the test rows are merely transformed.*

**Fix:** split first; put every fitted preprocessing step in a `Pipeline` (e.g. `make_pipeline(scaler, model)`) and pass the raw data to `cross_val_score`, so each step is re-fit on the training folds only.

## 2. Tuning on the test set

Every time you look at the test score and change something, the test set becomes part of training. Picking the best of many configurations by test score is the **winner's curse**: the maximum of many noisy estimates is biased upwards.

![Twenty useless models scored on one test set: the best looks like 0.61, but on fresh data it scores 0.50](../../Attachments/ML%20Animations/Common%20Pitfalls%20-%20tuning%20on%20the%20test%20set.gif)

*Watch the tallest yellow bar (the "winner" among 20 coin-flip models) collapse back to 0.5 on fresh data: its lead was pure luck.*

**The math.** A classifier with true accuracy $p$ evaluated on $n$ test points has test accuracy with standard deviation $\mathrm{sd}=\sqrt{p(1-p)/n}$. For $p=0.5$, $n=100$: $\mathrm{sd}=0.05$, so a score of $0.6$ is just two standard deviations above chance ($P\approx0.0228$ for one model). With 20 independent useless models, $P(\text{at least one}>0.6)=1-(1-0.0228)^{20}\approx0.37$.

**Fix:** choose among configurations with a validation split or (nested) cross-validation on the training data, then evaluate the single chosen model **once** on the test set ([[Cross-Validation and Model Selection]]).

## 3. Accuracy on imbalanced data

With 2% positives, "always predict negative" has 98% accuracy and is useless. Use metrics that focus on the rare class: precision $=\frac{TP}{TP+FP}$, recall $=\frac{TP}{TP+FN}$, $F_1=\frac{2PR}{P+R}$, and **PR-AUC** (average precision) $\mathrm{AP}=\sum_n(R_n-R_{n-1})P_n$. ROC-AUC can look flattering: a small false-positive *rate* still means many false positives relative to the few true ones. The baseline for AP is the **prevalence** (not 0.5), because a random scorer has precision equal to the positive rate ([[Model Evaluation and Metrics]]).

## 4. Not scaling features

$k$-NN, $k$-means, SVMs, PCA and anything trained by gradient descent are sensitive to feature scales: a feature measured in thousands dominates Euclidean distances and creates an ill-conditioned loss surface that GD crawls across. Tree models do not care. Standardise inside the pipeline ([[Data Preprocessing]]).

## 5. Duplicates and groups across train and test

If one patient contributes 10 scans, or one user several sessions, or one image several augmented copies, a random split puts near-copies in both train and test. A 1-NN then "recognises the patient" and copies the label: near-100% accuracy even when labels are random. **Fix:** `GroupKFold` with the patient/user id as the group, and deduplicate before splitting.

## 6. Misreading t-SNE

t-SNE preserves **local neighbourhoods** only. It adapts its bandwidth per point (perplexity), so cluster **sizes** are not meaningful; distances **between** clusters are not preserved; and different seeds give different pictures because the objective is non-convex. Check claims in the original space or with PCA ([[Dimensionality Reduction]]).

## 7. Correlation vs. causation

Feature importance measures **predictive** usefulness, not causal effect. If "number of support tickets" predicts churn, a buggy product probably causes both; hiding the ticket button removes the signal, not the problem. To estimate effects, run an experiment or use the tools in [[Causal Inference]].

## 8. Ignoring the baseline

A metric means nothing without a reference. Always report a `DummyClassifier`/`DummyRegressor` (majority class, median) and a simple model (linear, small tree) next to the fancy one. A **skill score** $1-\mathrm{MAE}_{\text{model}}/\mathrm{MAE}_{\text{dummy}}$ near 0 means the model learned nothing.

## 9. Shape bugs and broadcasting

NumPy broadcasting silently turns `(200,1) - (200,)` into a $(200,200)$ matrix of all pairwise differences, so an "MSE" can be off by orders of magnitude with no error raised. Fix: `ravel()` one side and `assert err.shape == y_hat.shape` in every loss ([[NumPy Snippets]]).

## 10. Train vs. eval mode

**Inverted dropout** zeroes each unit with probability $p$ in training and scales survivors by $\frac1{1-p}$, so $\mathbb E[\text{out}]=(1-p)\cdot\frac{x}{1-p}=x$ and nothing changes at test time. Forgetting `model.eval()` keeps dropout active (random, worse predictions) and makes BatchNorm use the test batch's statistics instead of its running averages ([[PyTorch Recipes]]).

## 11. Non-reproducible results

Sources of drift: random seeds (NumPy, `random`, framework, `random_state` in splits and models), data versions, code and hyperparameters, library versions (defaults change), and hardware/GPU non-determinism. Fix: set and log seeds, version the data, log a config per run, pin the environment.

## 12. Log of zero and overflow

$e^{1000}$ overflows float64 (the maximum is about $e^{709.8}$), and $\log 0=-\infty$. Use the **log-sum-exp** trick

$$\mathrm{LSE}(z)=\log\sum_ie^{z_i}=m+\log\sum_ie^{z_i-m},\qquad m=\max_iz_i,$$

which is exact (factor $e^m$ out) and never exponentiates anything larger than $e^0=1$. For binary cross-entropy, compute from **logits** without forming $\sigma(z)$:
$\ell=\max(z,0)-zy+\log(1+e^{-|z|})$ (use `np.log1p`). Otherwise clip probabilities to $[\varepsilon,1-\varepsilon]$.

## Worked example

**The accuracy paradox.** 500 transactions, 10 frauds.
- Classifier A always says "not fraud": accuracy $490/500=0.98$, recall $0$.
- Classifier B: TP $=8$, FN $=2$, FP $=40$, TN $=450$. Accuracy $458/500=0.916$ (lower than A!), precision $8/48=0.167$, recall $8/10=0.8$, $F_1=\frac{2\cdot0.167\cdot0.8}{0.967}\approx0.28$.

B catches 80% of the fraud and is far more useful; accuracy rewards the majority class.

**Winner's curse with fewer models.** 10 useless models, same $n=100$: $1-0.9772^{10}\approx0.21$. Even a modest search gives a one-in-five chance of a fake "significant" result.

**Log-sum-exp.** $z=(800,799)$: naive `np.log(np.sum(np.exp(z)))` returns `inf`. With $m=800$: $\mathrm{LSE}=800+\ln(1+e^{-1})=800+0.3133=800.3133$, and $\log\mathrm{softmax}(z)_1=z_1-\mathrm{LSE}=-0.3133$.

## Common confusions

- *"Standardising before the split is harmless."* → It leaks a little (means and variances); feature selection or target encoding before the split leaks a lot. Put everything in a pipeline so you never have to judge.
- *"Cross-validation protects me from overfitting."* → Only if all fitting, *including* preprocessing and hyperparameter search, happens inside the folds (nested CV for tuning).
- *"High ROC-AUC means good performance on rare events."* → Check precision and PR-AUC; ROC can look good while most alerts are false.
- *"Two clusters close together in t-SNE are similar."* → Inter-cluster distances are not preserved.
- *"No error message means the code is right."* → Broadcasting, eval-mode and overflow bugs are silent. Assert shapes and sanity-check against a baseline.

## Check yourself

> [!question]- A classmate standardised the whole dataset, selected features by correlation with the label, split 80/20, tried 40 settings and reports the best test accuracy. Name three pitfalls.
> Leakage via preprocessing and label-based feature selection before splitting; tuning on the test set (best of 40); and, if the data is imbalanced, accuracy as the metric. Possibly also groups across splits and a causal claim from correlations.

> [!question]- Why does shuffled k-fold overestimate a forecasting model?
> Neighbouring time steps end up in training, so predicting $t$ becomes interpolation between $t-1$ and $t+1$. The real task is extrapolating into the future, which `TimeSeriesSplit` simulates.

> [!question]- What is the baseline value of average precision for a random scorer with 2% positives?
> About $0.02$, the prevalence, not $0.5$.

> [!question]- Why does inverted dropout need no rescaling at test time?
> Survivors are scaled by $1/(1-p)$ during training, so the expected activation already equals $x$.

> [!question]- What does `np.log(np.sum(np.exp([1000, 1000])))` return, and what is the correct value?
> `inf` (overflow). The correct value is $1000+\ln2\approx1000.693$, via log-sum-exp.

## Practice

[Common Pitfalls - Exercises](Common%20Pitfalls%20-%20Exercises.ipynb): spot-the-pitfall, feature selection before CV, hunting a target leak, shuffled CV on a time series, groups across folds, the winner's curse on the test set, the accuracy paradox, PR-AUC from scratch, baselines, t-SNE and causation questions, the broadcasting bug, dropout modes, reproducibility, log-sum-exp and stable losses, and debugging an oversampling pipeline.

> [!tip] Oversampling belongs inside the pipeline too
> SMOTE or random oversampling before the split (or before cross-validation) copies (or interpolates) minority samples into both train and test: the same leakage as duplicates across splits. Resample only the training folds (e.g. with an imbalanced-learn `Pipeline`).

## Learn more
- [Made With ML](https://madewithml.com/)
- [Molnar – Interpretable ML](https://christophm.github.io/interpretable-ml-book/)
- [scikit-learn — Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html)
- [Google — Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)
