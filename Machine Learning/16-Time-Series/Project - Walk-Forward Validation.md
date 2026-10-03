---
tags: [ml, project, validation, time-series]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Walk-Forward Validation

> [!summary] In one sentence
> Measure how much random K-fold cross-validation lies on time series: a model that knows the date predicts Aalborg's temperature with 1.38 °C error under random CV, 2.28 °C under walk-forward CV, and really 2.96 °C on 2024.

**Notebook:** [Project - Walk-Forward Validation](Project%20-%20Walk-Forward%20Validation.ipynb) · topic: [[Time Series Validation and Features]] · all projects: [[Projects Overview]]

## What you build
1. `walk_forward_splits`: expanding windows with a gap before each test block.
2. `cv_mae`: fit a fresh clone per split.

## Reference results (solution, laptop CPU)
Extra-trees on a time index + season features (2018–2023 development, 2024 holdout):

| estimate | MAE (°C) |
|---|---|
| random 5-fold CV | 1.380 |
| walk-forward CV | 2.277 |
| **true 2024 error** | **2.957** |

Random CV interpolates between neighbouring days it trained on; walk-forward has to extrapolate, like real forecasting.

## Check yourself
> [!question]- Why is even walk-forward a bit optimistic here?
> Its test blocks lie within 2018–2023, while 2024 may be unusual (and the trees can't extrapolate the time index beyond the training range). It's still far closer than random CV.

> [!question]- What is the gap for?
> Lag/rolling features computed near the split boundary overlap train and test; a gap of at least the longest lag removes that leak.

---
Back to [[00 - Machine Learning Index]].
