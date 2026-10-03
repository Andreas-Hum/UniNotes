---
tags: [ml, play, leaderboard]
status: not-started
level:
reviewed:
---
# Leaderboard

> [!summary] In one sentence
> Three fixed tasks with fixed splits and metrics, so every score you log is comparable with every earlier one: beat the baseline, then beat yourself.

Kaggle without the crowd. The data, the split and the metric never change, so a better number really means a better model. Log every serious attempt, including the ones that lose: the losers teach as much as the winners.

## Current best
```dataviewjs
const text = await dv.io.load(dv.current().file.path);
const rows = [];
for (const sec of text.split(/^## /m).filter(s => s.startsWith("Task"))) {
  const dir = sec.match(/\((higher|lower) is better\)/), hi = !dir || dir[1] === "higher";
  const entries = sec.split("\n").map(l => l.trim().replace(/^\||\|$/g, "").split("|").map(c => c.trim()))
    .filter(c => c.length >= 3 && /^\d{4}-\d{2}-\d{2}$/.test(c[0]) && !isNaN(parseFloat(c[1])));
  if (!entries.length) continue;
  const base = entries.find(c => /^baseline/i.test(c[2])) || entries[0];
  const best = entries.reduce((a, c) => (hi ? +c[1] > +a[1] : +c[1] < +a[1]) ? c : a);
  const gain = hi ? +best[1] - +base[1] : +base[1] - +best[1];
  rows.push([sec.split("\n")[0].replace(/^Task \d+ · /, ""), `**${best[1]}**`, best[2], best[0],
             (gain > 0 ? "▲ " : "") + (Math.abs(gain) < 1e-12 ? "–" : gain.toFixed(4)), entries.length - 1]);
}
dv.table(["Task", "Best", "Method", "Date", "Better than baseline by", "Attempts"], rows);
```

## How it works
1. Open the task's starter notebook. Run it once as delivered: it downloads the data, checks a **fingerprint** of the split and reproduces the baseline.
2. Write your model in `my_model` and iterate on the **validation** score as often as you like.
3. Run the **test** cell once per idea. It prints ✅/❌ against the baseline and your current best (read from this note), plus a ready-made table row.
4. Paste the row at the bottom of the task's table. The *Current best* table above and the [[00 - Progress Dashboard]] update by themselves.

> [!warning] House rules (all tasks)
> - **Never tune on test.** Choose hyperparameters, epochs and architectures on validation; the test cell is the final exam.
> - Same split, same metric, same official function. If the fingerprint check prints ❌, the score doesn't count.
> - One row per idea, not per random seed. If you report a lucky seed, say so in *Method*.
> - Write *Method* so that future you could reproduce it: model, key hyperparameters, training time if it was long.

---

## Task 1 · MNIST digits
**Metric:** test accuracy (higher is better) · **Notebook:** [Leaderboard - MNIST](Leaderboard%20-%20MNIST.ipynb)

| | |
|---|---|
| **Data** | MNIST, 70 000 grey-scale 28×28 handwritten digits (Keras mirror `mnist.npz`) |
| **Split** | official 60 000 train / 10 000 test; validation = last 10 000 training images |
| **Rules** | no model pre-trained on MNIST · augmentation, ensembles and long training are fine |
| **Baseline** | logistic regression on pixels / 255, scikit-learn defaults, `max_iter=100`: **0.9257** |

```python
def mnist_accuracy(y_pred):            # y_test: the 10 000 official test labels
    y_pred = np.asarray(y_pred).ravel()
    assert y_pred.shape == y_test.shape
    return float((y_pred == y_test).mean())
```

| Date | Score | Method | Notebook |
|---|---|---|---|
| 2026-10-03 | 0.9257 | baseline: logistic regression on raw pixels | [notebook](Leaderboard%20-%20MNIST.ipynb) |

**Reference points** (measured on this setup): kNN with k = 3 on raw pixels reaches 0.9705.
Theory: [[k-Nearest Neighbors]] · [[Support Vector Machines]] · [[CNN]] · [[Training Tricks]]

## Task 2 · MovieLens top-10
**Metric:** full-ranking NDCG@10 (higher is better) · **Notebook:** [Leaderboard - MovieLens](Leaderboard%20-%20MovieLens.ipynb)

| | |
|---|---|
| **Data** | MovieLens `ml-latest-small` (100 836 ratings, 610 users, 9 742 movies): the "100K" dataset used by [[Project - MovieLens Recommender]], not the older `ml-100k` release |
| **Split** | the project's split: ratings ≥ 4 are positives; per user the latest positive is test, the one before is validation, the rest is train |
| **Rules** | use train positives (+ validation positives for the final refit) and movie metadata only · no ratings below 4, no test rows |
| **Baseline** | most popular movies (positives in train + validation): **0.0217** |

A model returns one score per movie. The test movie is ranked against **all** movies except the ones the user is already known to like; ties are broken by movie id so the number is deterministic. Full-ranking scores are much smaller than the project's sampled "1 vs 99" numbers. That is expected, see [[Evaluating Recommenders]].

```python
def ndcg_at_10(score_fn, held_out, known, k=10):
    known = known.groupby("userId").movieId.apply(lambda s: [COL[m] for m in s]).to_dict()
    gains = []
    for u, m in held_out.itertuples(index=False):
        s = np.array(score_fn(u), dtype=float)        # one score per movie, in ITEMS order
        s[known.get(u, [])] = -np.inf                 # hide movies the user already liked
        top = ITEMS[np.argsort(-s, kind="stable")[:k]]
        hit = np.flatnonzero(top == m)
        gains.append(1 / np.log2(hit[0] + 2) if len(hit) else 0.0)
    return float(np.mean(gains))
# official score: ndcg_at_10(model_fitted_on_train_val, test, known=train_val)
```

| Date | Score | Method | Notebook |
|---|---|---|---|
| 2026-10-03 | 0.0217 | baseline: most popular | [notebook](Leaderboard%20-%20MovieLens.ipynb) |

**Reference points** (measured on this setup): item co-occurrence damped by popularity^0.5 reaches 0.0311; EASE (λ = 200, chosen on validation) reaches 0.0358.
Theory: [[Collaborative Filtering and Matrix Factorization]] · [[Deep Learning Recommenders]] · [[Evaluating Recommenders]]

## Task 3 · M4 Hourly forecasting
**Metric:** mean MASE, m = 24 (lower is better) · **Notebook:** [Leaderboard - M4 Hourly](Leaderboard%20-%20M4%20Hourly.ipynb)

| | |
|---|---|
| **Data** | Hourly subset of the M4 competition: 414 series, 700–960 hours each ([M4-methods repository](https://github.com/Mcompetitions/M4-methods)) |
| **Split** | official M4 holdout: the 48 hours after each training series; validation = last 48 hours of each training series |
| **Rules** | forecasts from the training histories only (global models across series are fine) · no external data |
| **Baseline** | seasonal naive, repeat the last 24 hours: **1.1932** |

MASE divides the forecast MAE by the in-sample MAE of the seasonal naive one-day-ahead forecast, so < 1 means "better than repeating yesterday" and series of any scale can be averaged.

```python
def mase(history, actual, forecast, m=24):
    scale = np.mean(np.abs(history[m:] - history[:-m]))   # in-sample seasonal-naive MAE
    return np.mean(np.abs(actual - forecast)) / scale
# official score: mean of mase(train[k], test[k], forecast[k]) over all 414 series
```

| Date | Score | Method | Notebook |
|---|---|---|---|
| 2026-10-03 | 1.1932 | baseline: seasonal naive | [notebook](Leaderboard%20-%20M4%20Hourly.ipynb) |

**Reference points** (measured on this setup): averaging the same hour over the last two days scores 1.3772 and a ridge regression that predicts raw values from lags about 1.73, both *worse* than the baseline. Seasonal naive is hard to beat here; the notebook's example, a global ridge model that predicts the *correction* to seasonal naive, reaches 0.9619.
Theory: [[Time Series Forecasting]] · [[Classical Forecasting Models]] · [[Time Series Validation and Features]] · [[Deep Learning for Time Series]]

---

## Learn more
- Steck (2019), *Embarrassingly Shallow Autoencoders for Sparse Data* (EASE): [arXiv:1905.03375](https://arxiv.org/abs/1905.03375)
- Ferrari Dacrema et al. (2019), *Are We Really Making Much Progress?*: strong simple baselines beat many neural recommenders, [arXiv:1907.06902](https://arxiv.org/abs/1907.06902)
- Hyndman & Koehler (2006), *Another look at measures of forecast accuracy* (introduces MASE): [doi:10.1016/j.ijforecast.2006.03.001](https://doi.org/10.1016/j.ijforecast.2006.03.001)
- Makridakis, Spiliotis & Assimakopoulos (2020), *The M4 Competition: 100,000 time series and 61 forecasting methods*: [doi:10.1016/j.ijforecast.2019.04.014](https://doi.org/10.1016/j.ijforecast.2019.04.014)

Related: [[Break the Model]] · [[Guess the Output]] · [[Playgrounds]] · [[Project - MovieLens Recommender]]
