---
tags: [ml, fundamentals, evaluation]
---
# Model Evaluation and Metrics

> [!summary] In one sentence
> A metric turns "is this model good?" into a number, and the right number depends on **which mistakes are expensive**, **how imbalanced the classes are**, and **whether you need labels, scores or rankings**.

## Intuition first

Imagine a COVID test. "It is right 99 % of the time" sounds great, until you learn that only 1 % of people tested are infected, so a test that always says "negative" is also right 99 % of the time. What we actually want to know is: *of the infected, how many does it catch?* (recall) and *of the people it flags, how many are really infected?* (precision). Different stakeholders care about different cells of the same table.

All classification metrics are built from four counts, the **confusion matrix**:

| | predicted positive | predicted negative |
|---|---|---|
| **actually positive** | TP (hit) | FN (miss) |
| **actually negative** | FP (false alarm) | TN (correct rejection) |

Most classifiers actually output a **score** (e.g. a probability); the counts depend on the **threshold** you apply. Threshold-free metrics like ROC-AUC summarise performance over *all* thresholds.

![Sweeping the threshold traces the ROC curve](../../Attachments/ML%20Animations/Model%20Evaluation%20and%20Metrics%20-%20threshold%20sweep%20traces%20ROC.gif)
*Watch the yellow threshold slide from right to left: the green area (positives above it) is the TPR, the red area (negatives above it) is the FPR, and each position becomes one point of the ROC curve.*

## Classification
Confusion matrix: TP, FP, FN, TN.

| Metric | Formula | Use when |
|---|---|---|
| Accuracy | $\frac{TP+TN}{N}$ | balanced classes |
| Precision | $\frac{TP}{TP+FP}$ | false positives costly |
| Recall (TPR) | $\frac{TP}{TP+FN}$ | false negatives costly |
| F1 | $\frac{2PR}{P+R}$ | imbalance, single number |
| Specificity | $\frac{TN}{TN+FP}$ | |
| ROC-AUC | area under TPR vs FPR | ranking quality, threshold-free |
| PR-AUC | area under precision vs recall | heavy imbalance |
| Log loss | $-\frac1N\sum y\log\hat p+(1-y)\log(1-\hat p)$ | probabilistic quality |
| MCC | balanced correlation | imbalance |

## The math, step by step

**Precision vs. recall.** Precision divides by the *predicted* positives (column), recall by the *actual* positives (row). Raising the threshold flags fewer cases: precision usually rises, recall falls.

**F1 is a harmonic mean.** $F_1 = \frac{2PR}{P+R} = \frac{2}{1/P + 1/R}$. The harmonic mean is dragged towards the smaller value, so you cannot get a high F1 by maxing one and ignoring the other ($P = 1, R = 0.01$ gives $F_1 \approx 0.02$).

**Specificity and FPR.** $\text{FPR} = \frac{FP}{FP + TN} = 1 - \text{specificity}$: the fraction of negatives wrongly flagged.

**ROC curve and AUC.** For every threshold $t$, plot $(\text{FPR}(t), \text{TPR}(t))$. A random scorer gives the diagonal (AUC 0.5), a perfect one hugs the top-left corner (AUC 1). AUC has a beautiful interpretation:
$$\text{AUC} = P\big(\text{score}(\text{random positive}) > \text{score}(\text{random negative})\big),$$
counting ties as ½. So AUC measures **ranking** quality and ignores calibration and threshold.

**Why PR-AUC under heavy imbalance.** FPR divides by the (huge) number of negatives, so thousands of false alarms barely move it; ROC looks great. Precision divides by the predicted positives, so false alarms hit it directly. Precision also depends on prevalence $\pi$:
$$\text{precision} = \frac{\text{TPR}\cdot \pi}{\text{TPR}\cdot\pi + \text{FPR}\cdot(1-\pi)}.$$
Same model (TPR 0.9, FPR 0.05): precision 0.95 at $\pi = 0.5$, but only 0.15 at $\pi = 0.01$.

**Log loss** punishes confident mistakes without bound ($-\log \hat p \to \infty$ as $\hat p \to 0$ for a true positive). It rewards **calibrated** probabilities. Baseline: always predicting the base rate $\pi$ gives log loss $-[\pi\log\pi + (1-\pi)\log(1-\pi)]$ (the binary entropy), so any useful model must beat that.

**MCC (Matthews correlation coefficient)** is the correlation between true and predicted labels:
$$\text{MCC} = \frac{TP\cdot TN - FP\cdot FN}{\sqrt{(TP+FP)(TP+FN)(TN+FP)(TN+FN)}} \in [-1, 1].$$
It is only high if the model does well on **both** classes, and it is symmetric (swapping the class names does not change it), unlike F1.

## Worked example

Fraud test set, $N = 1000$: TP = 40, FP = 10, FN = 20, TN = 930.

| Metric | Computation | Value |
|---|---|---|
| Accuracy | $(40 + 930)/1000$ | 0.970 |
| Majority baseline | $940/1000$ | 0.940 |
| Precision | $40/50$ | 0.800 |
| Recall | $40/60$ | 0.667 |
| F1 | $2\cdot0.8\cdot0.667/(0.8+0.667)$ | 0.727 |
| Specificity | $930/940$ | 0.989 |
| MCC | $(40\cdot930 - 10\cdot20)/\sqrt{50\cdot60\cdot940\cdot950}$ | 0.715 |

Accuracy says "97 %!", but the model misses a third of the frauds.

**AUC by counting pairs.** Positive scores $\{0.9, 0.6, 0.4\}$, negative scores $\{0.7, 0.3, 0.2\}$. Of the $3\times3 = 9$ (positive, negative) pairs, the positive wins in $3 + 2 + 2 = 7$, so AUC $= 7/9 \approx 0.78$.

**Log loss of the base-rate predictor** with $\pi = 0.1$: $-(0.1\ln0.1 + 0.9\ln0.9) \approx 0.325$.

## Regression
MSE, RMSE, MAE, $R^2 = 1-\frac{SS_{res}}{SS_{tot}}$, MAPE.

- **MSE** $= \frac1N\sum (y_i - \hat y_i)^2$: squares errors, so it is dominated by large errors; matches a Gaussian noise assumption.
- **RMSE** $= \sqrt{\text{MSE}}$: same units as $y$.
- **MAE** $= \frac1N\sum\lvert y_i - \hat y_i\rvert$: robust to outliers; "typical" error.
- **$R^2$** with $SS_{res} = \sum(y_i - \hat y_i)^2$ and $SS_{tot} = \sum(y_i - \bar y)^2$: fraction of variance explained. $R^2 = 0$ means "no better than predicting the mean"; it can be **negative** on test data.
- **MAPE** $= \frac{100\%}{N}\sum\left\lvert\frac{y_i - \hat y_i}{y_i}\right\rvert$: scale-free and intuitive, but explodes when $y_i \approx 0$ and penalises over-prediction more than under-prediction.

**Example.** $y = (3, 5, 8)$, $\hat y = (2, 5, 10)$. Errors $-1, 0, 2$. MSE $= 5/3 \approx 1.67$, RMSE $\approx 1.29$, MAE $= 1$. $\bar y = 5.33$, $SS_{tot} \approx 12.67$, $SS_{res} = 5$, so $R^2 \approx 0.61$.

## Clustering
Silhouette, Davies–Bouldin, adjusted Rand index, normalized mutual information. See [[Clustering]].

- **Internal** metrics need no labels: **silhouette** $s = \frac{b - a}{\max(a, b)}$ per point, where $a$ is the mean distance to its own cluster and $b$ the mean distance to the nearest other cluster ($s \approx 1$ well placed, $\approx 0$ on a border, $< 0$ probably misassigned). **Davies–Bouldin**: average ratio of within-cluster spread to between-cluster separation; lower is better.
- **External** metrics compare with true labels: **adjusted Rand index** (pair agreement corrected for chance: 0 = random, 1 = identical) and **NMI** (shared information between the two labelings, normalised to $[0,1]$). Both ignore how clusters are named.

## Ranking / retrieval
Precision@k, MAP, NDCG, MRR. For graphs see [[Link Prediction]].

- **Precision@k**: fraction of relevant items in the top $k$.
- **AP** (average precision): mean of precision@k over the ranks $k$ where a relevant item appears; **MAP** averages AP over queries. Relevant at ranks 1 and 3 (two relevant in total): AP $= (1 + \tfrac23)/2 \approx 0.83$.
- **MRR**: mean of $1/\text{rank}$ of the first relevant item. First hits at ranks 1, 3, 2: MRR $= (1 + \tfrac13 + \tfrac12)/3 \approx 0.61$.
- **NDCG@k**: graded relevance, discounted by position: $\text{DCG@k} = \sum_{i=1}^k \frac{rel_i}{\log_2(i+1)}$, normalised by the DCG of the ideal ordering. Relevances $(3, 2, 0, 1)$: DCG $\approx 4.69$, ideal $(3,2,1,0)$ gives $4.76$, NDCG $\approx 0.985$. (A common variant uses gain $2^{rel_i} - 1$.)

> [!warning]
> Accuracy on a 99%/1% split is meaningless. Always check the baseline (majority class).

Splitting strategy: [[Cross-Validation and Model Selection]].

## Common confusions
- **"High ROC-AUC means good precision."** Not under heavy imbalance: AUC can be 0.95 while precision is 0.1. Check PR-AUC.
- **"AUC tells me how well calibrated the probabilities are."** AUC only depends on the ranking; multiplying all scores by 0.5 leaves it unchanged. Use log loss or a calibration plot.
- **"Precision is a property of the model."** It also depends on prevalence; the same model has different precision in a different population.
- **"$R^2$ is between 0 and 1."** On test data it can be negative.
- **"F1 is symmetric in the classes."** It ignores TN completely; MCC does not.

## Check yourself

> [!question]- A cancer screening test should miss as few cancers as possible. Which metric do you prioritise?
> Recall (sensitivity), possibly subject to a minimum precision or specificity to keep false alarms manageable.

> [!question]- What does ROC-AUC = 0.8 mean in plain words?
> If you pick one random positive and one random negative, the model scores the positive higher 80 % of the time.

> [!question]- Model A has log loss 0.40, the base rate is 10 %. Is it useful?
> No: the base-rate predictor already achieves about 0.325. Model A is worse than knowing nothing but the prevalence.

> [!question]- Why can MAPE be misleading when sales are sometimes zero?
> It divides by $y_i$; with $y_i \approx 0$ the relative error explodes (or is undefined).

> [!question]- Silhouette or adjusted Rand index: which needs ground-truth labels?
> Adjusted Rand index (external). Silhouette is internal.

## Practice
[Model Evaluation and Metrics - Exercises](Model%20Evaluation%20and%20Metrics%20-%20Exercises.ipynb)

## Learn more
- [scikit-learn – metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [CS229 cheatsheets](https://stanford.edu/~shervine/teaching/cs-229/)
- [StatQuest videos](https://statquest.org/video_index.html) (look for "ROC and AUC" and "Sensitivity and Specificity")
- [MLU-Explain – ROC and AUC (interactive)](https://mlu-explain.github.io/roc-auc/)
