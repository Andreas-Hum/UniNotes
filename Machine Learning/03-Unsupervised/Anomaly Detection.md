---
tags: [ml, unsupervised, anomaly]
status: not-started
notebook: not-started
level:
reviewed:
---
# Anomaly Detection

> [!summary] In one sentence
> Anomaly detection learns what "normal" looks like (a density, a distance, a boundary or a reconstruction) and then flags the rare points that do not fit it, which is hard mainly because anomalies are rare, varied and usually unlabelled.

## Intuition first

Find rare observations that differ from the norm.

A bank sees millions of card transactions a day and a few dozen frauds. Nobody can label every new fraud trick in advance, but the bank knows very well what *normal* spending looks like for you. So instead of learning "what fraud looks like" (supervised), it learns "what you look like" and raises an alarm when something does not fit. That is the core idea: **model normality, flag deviations**.

Every method answers "how unusual is this point?" in a different way:
- **How unlikely is it?** (statistical: a density or a distance from the centre)
- **How easy is it to separate from everything else?** (Isolation Forest)
- **Is it outside the region where normal data live?** (One-class SVM)
- **Is its neighbourhood emptier than its neighbours' neighbourhoods?** (LOF)
- **Can a model of normal data reproduce it?** (reconstruction error)
- **Did the series do something its own past did not predict?** (time series)

Two settings, as scikit-learn names them:
- **Outlier detection**: the training data itself is contaminated; find the odd ones inside it (e.g. a one-off audit of last year's expense claims). Methods must be robust to the outliers they are hunting.
- **Novelty detection**: the training data is clean; decide whether *new* points are abnormal (e.g. a machine known to be healthy, monitored from now on).

![Random axis-aligned cuts isolate an outlier in 2 splits but a central point needs 9](../../Attachments/ML%20Animations/Anomaly%20Detection%20-%20isolation%20forest%20splits.gif)
*Watch the split counter: random cuts trap the lonely red point almost immediately, while the yellow point in the crowd needs many cuts before its box contains it alone.*

## The methods

- **Statistical**: z-score, IQR, Mahalanobis distance, Gaussian density threshold.
- **Isolation Forest**: anomalies are isolated with few random splits.
- **One-class SVM**: boundary around normal data ([[Support Vector Machines]]).
- **Local Outlier Factor**: density relative to neighbours ([[k-Nearest Neighbors]]).
- **Reconstruction error**: [[PCA]] / autoencoders ([[Generative Models]]).
- **Time series**: residuals of forecasting models, change-point detection.

## The math, step by step

### Statistical scores
- **z-score**: $z=\frac{x-\bar x}{s}$; flag $|z|>3$. Assumes roughly Gaussian data. Weakness: the outlier itself inflates $\bar x$ and $s$, so it can hide itself.
- **Robust z-score**: $\frac{x-\text{median}}{1.4826\cdot\text{MAD}}$, where MAD is the median of $|x_i-\text{median}|$. The factor 1.4826 makes it match the standard deviation for Gaussian data. Medians ignore a few extreme values, so this does not get fooled.
- **IQR fences (Tukey)**: with quartiles $Q_1,Q_3$ and $\mathrm{IQR}=Q_3-Q_1$, flag points below $Q_1-1.5\,\mathrm{IQR}$ or above $Q_3+1.5\,\mathrm{IQR}$. Also robust, no Gaussian assumption.
- **Mahalanobis distance**: $d^2(x)=(x-\mu)^\top\Sigma^{-1}(x-\mu)$. It measures distance in units of the data's own spread *in each direction*, so a point that breaks the correlation pattern is far even if it is close in plain Euclidean terms. For Gaussian data $d^2\sim\chi^2_d$, which gives a principled threshold (e.g. the 97.5% quantile).
- **Gaussian density threshold**: fit $\mathcal N(\mu,\Sigma)$ on (mostly) normal training data, flag $p(x)<\varepsilon$, and choose $\varepsilon$ on a labelled validation set (e.g. maximise F1). A [[Gaussian Mixture Models and EM|GMM]] extends this to multi-modal normal data.

**Masking**: a *cluster* of outliers drags the classical mean toward itself and inflates the covariance, so each outlier looks less extreme and they hide each other. The cure is robust estimation: medians/MAD in 1-D, the **Minimum Covariance Determinant** (MCD) in many dimensions, which estimates $\mu,\Sigma$ from the tightest subset of points.

### Isolation Forest
Build many random trees: at each node pick a random feature and a random split value between its min and max, until each point is alone. An anomaly lives in a sparse region, so a random cut is likely to separate it early: its **path length** $h(x)$ is short. Average over trees and normalise:
$$s(x)=2^{-\mathbb E[h(x)]/c(n)},\qquad c(n)=2H(n-1)-\frac{2(n-1)}{n},\quad H(i)\approx\ln i+0.5772$$
- $c(n)$ is the average path length of an unsuccessful search in a binary search tree of $n$ points, a "typical" depth.
- $s\to1$: much shorter than typical, an anomaly. $s\approx0.5$ everywhere: no clear anomalies. $s\ll0.5$: clearly normal.
- Each tree uses a small subsample (e.g. $n=256$), which makes it fast, linear in $N$, and less prone to masking.

### One-class SVM
Map data with a kernel and find the smallest region (a hyperplane separating the data from the origin in feature space, or a hypersphere) that contains most normal points; $\nu$ sets the fraction allowed outside. Flexible boundaries, but sensitive to the kernel bandwidth and scaling, and scales poorly to large $N$. See [[Support Vector Machines]].

### Local Outlier Factor (LOF)
Compares a point's local density with its neighbours' densities ([[k-Nearest Neighbors]]):
- $k\text{-dist}(o)$: distance from $o$ to its $k$-th nearest neighbour.
- Reachability distance: $\text{reach-dist}_k(p,o)=\max\{k\text{-dist}(o),\ d(p,o)\}$ (smooths out tiny distances inside dense groups).
- Local reachability density: $\mathrm{lrd}(p)=1\big/\operatorname{mean}_{o\in N_k(p)}\text{reach-dist}_k(p,o)$.
- $\mathrm{LOF}(p)=\operatorname{mean}_{o\in N_k(p)}\frac{\mathrm{lrd}(o)}{\mathrm{lrd}(p)}$.

$\mathrm{LOF}\approx1$: as dense as its neighbours (normal). $\mathrm{LOF}\gg1$: much sparser than its neighbours (outlier). Because it is **relative**, LOF can catch a point just outside a dense cluster even if a sparse cluster elsewhere has larger absolute distances, which a global distance threshold would miss. The choice of $k$ matters: if a group of anomalies is larger than $k$, they become each other's neighbours and look normal.

### Reconstruction error
Fit a model that compresses and reconstructs *normal* data: [[PCA]] with $k$ components, or an autoencoder ([[Generative Models]]). Score $\lVert x-\hat x\rVert^2$. Normal points lie near the learned subspace/manifold and reconstruct well; anomalies have structure the model never learned and reconstruct badly. With PCA the score is the energy in the discarded components.

### Time series
- **Residuals of forecasting models**: predict $\hat x_t$ from the past (ARIMA, exponential smoothing, or even a rolling median), and flag large residuals $|x_t-\hat x_t|$, e.g. above $5\times1.4826\cdot\text{MAD}$ of the residuals. This removes trend and seasonality, so a value that is normal in December can be anomalous in July.
- **Change-point detection**: find when the *distribution* shifts rather than single spikes. The one-sided **CUSUM** accumulates evidence: $g_t=\max(0,\ g_{t-1}+x_t-\mu_0-\kappa)$, alarm when $g_t>h$. $\kappa$ (slack) ignores small drifts; $h$ trades detection delay against false alarms.

## Evaluation

Evaluate with PR-AUC since classes are extremely imbalanced ([[Model Evaluation and Metrics]]).

Why not accuracy or ROC-AUC?
- With 0.1% anomalies, "everything is normal" scores **99.9% accuracy** while catching nothing.
- ROC-AUC uses the false-positive *rate*, which divides by the huge number of normals. A detector that raises 1000 false alarms per true fraud can still have a tiny FPR and a high ROC-AUC.
- **PR-AUC** (average precision) uses precision, which counts false alarms *relative to true detections*: exactly what an analyst reviewing alerts experiences. A random scorer gets ROC-AUC $=0.5$ but PR-AUC $\approx$ **the anomaly rate** (the prevalence), so always compare against that baseline.

Make sure higher score means more anomalous (scikit-learn's `score_samples` and `negative_outlier_factor_` are "higher = more normal", so negate them).

## Worked example

**z-score is fooled, robust score is not.** Data $10,12,11,13,50$.
- Mean $19.2$; squared deviations $84.64+51.84+67.24+38.44+948.64=1190.8$; population sd $=\sqrt{1190.8/5}\approx15.4$.
- $z(50)=\frac{50-19.2}{15.4}\approx2.0$, **not** flagged by $|z|>3$. The outlier inflated the sd.
- Median $12$; absolute deviations $2,0,1,1,38$, so MAD $=1$. Robust score $=\frac{50-12}{1.4826}\approx25.6$, flagged.

**Mahalanobis vs Euclidean.** $\mu=0$, $\Sigma=\begin{pmatrix}1&0.8\\0.8&1\end{pmatrix}$, $\Sigma^{-1}=\frac{1}{0.36}\begin{pmatrix}1&-0.8\\-0.8&1\end{pmatrix}$.
- $a=(1,1)$: $d^2=\frac{1-0.8-0.8+1}{0.36}=\frac{0.4}{0.36}\approx1.1$, it follows the positive correlation.
- $b=(1,-1)$: $d^2=\frac{1+0.8+0.8+1}{0.36}=10$, it breaks the correlation.
- Same Euclidean norm $\sqrt2$, but $b$ is far more anomalous.

**Isolation Forest score** with $n=256$: $H(255)\approx\ln255+0.5772\approx6.12$, so $c(256)\approx2(6.12)-\frac{2\cdot255}{256}\approx10.24$. A point with $\mathbb E[h]=4$ gets $s=2^{-4/10.24}\approx0.76$ (suspicious). A point with $\mathbb E[h]=c(n)$ gets exactly $2^{-1}=0.5$.

## Which detector, and when
| Method | Assumes normal data… | Fails when… |
|---|---|---|
| z-score / IQR | is 1-D, unimodal | multivariate patterns, masking (z-score) |
| Mahalanobis | is one elliptical blob | multi-modal data; classical version masks |
| Isolation Forest | anomalies are few and separable by axis cuts | anomalies hide in dense regions or need rotated cuts |
| LOF | has local density structure | anomaly groups larger than $k$; high $d$ |
| One-class SVM | lies in a compact kernel region | poorly scaled features, large $N$ |
| PCA / autoencoder | lies near a low-dim subspace/manifold | anomalies also lie in that subspace |

## Common confusions
- *"High ROC-AUC means the detector is useful."* → With extreme imbalance, check PR-AUC against the prevalence baseline.
- *"Train on all data, then detect."* → Fine for outlier detection, but for novelty detection train on clean data only; otherwise anomalies become part of "normal".
- *"An outlier is an error to delete."* → It may be the most interesting point (fraud, a fault, a discovery); investigate before dropping.
- *"Mahalanobis is robust."* → Only with robust estimates of $\mu,\Sigma$ (MCD); the classical version suffers from masking.
- *"Isolation Forest scores near 1 mean normal."* → Opposite: short paths give $s\to1$, which means anomalous (scikit-learn flips the sign in its API).

## Check yourself

> [!question]- A detector on data with 50 anomalies in 10 000 points reports PR-AUC 0.05. Is that good?
> The random baseline is the prevalence, $50/10\,000=0.005$, so 0.05 is 10× better than random but still means most alerts are false. It is weak in absolute terms.

> [!question]- Why does LOF use a ratio of densities instead of the density itself?
> So that it adapts to regions of different density: a point slightly outside a very dense cluster is anomalous relative to its neighbours, even if its absolute density is higher than that of normal points in a sparse cluster.

> [!question]- What is masking and how do you avoid it?
> A group of outliers shifts the mean and inflates the variance/covariance so that none of them looks extreme. Use robust estimators (median/MAD, MCD) or methods that are local or subsample-based.

> [!question]- Healthy-machine sensor logs are available and you will monitor new readings: outlier or novelty detection?
> Novelty detection: the training data are clean and you judge new points. A Gaussian density, One-class SVM or LOF with `novelty=True` fit the setting.

## Practice
[Anomaly Detection - Exercises](Anomaly%20Detection%20-%20Exercises.ipynb): PR-AUC baselines, z-score vs robust scores, IQR fences, Mahalanobis, Isolation Forest scores, LOF from scratch, PCA reconstruction error, time-series spikes and CUSUM.

## Learn more
- [scikit-learn – novelty & outlier detection](https://scikit-learn.org/stable/modules/outlier_detection.html)
- [scikit-learn – precision-recall](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html): why average precision is the right summary for rare positives.
