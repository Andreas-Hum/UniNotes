---
tags: [ml, project, deep-learning, forecasting]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Global Neural Forecaster

> [!summary] In one sentence
> Forecast tomorrow's hourly prices in six price areas with one global model, and test the note's claims on real data: global beats local, RevIN handles different price levels, a quantile TCN gives intervals (which need calibrating), and a linear model is a tough baseline.

**Notebook:** [Project - Global Neural Forecaster](Project%20-%20Global%20Neural%20Forecaster.ipynb) · topic: [[Deep Learning for Time Series]] · all projects: [[Projects Overview]]

## What you build
1. `revin`: per-window instance normalisation.
2. `CausalConv1d.forward`: left padding so the convolution never sees the future.
3. `pinball_loss`: summed quantile losses for P10/P50/P90 outputs.

## Reference results (solution, laptop CPU)
Six areas (DK1, DK2, SE3, SE4, NO2, DE), 451 training days each (Oct 2023 – Dec 2024), test = 2025:

| model | MAE (EUR/MWh) |
|---|---|
| **global linear + RevIN** | **22.28** |
| global TCN + RevIN (median) | 23.52 |
| seasonal naive (yesterday) | 25.74 |
| local linear (one model per area) | 30.96 |
| seasonal naive (last week) | 33.53 |

The TCN's "80 %" interval covers only **62 %** of 2025 prices, so it needs calibrating. Pooling the six areas helps the same linear model more than switching to a neural net does.

## Check yourself
> [!question]- Why does the local linear model do so badly?
> 169 × 24 weights from 451 examples per area: it overfits. Pooling six areas gives six times the data for the same weights, which only works because RevIN puts all areas on a common scale.

> [!question]- Why would quantile intervals under-cover on 2025?
> They were learned on 2023–24; if 2025 is more volatile (distribution shift) or the model is over-confident from overfitting, the true spread is wider than learned. Conformal calibration on recent data fixes coverage.

## Learn more
- [Zeng et al. – Are Transformers Effective for Time Series Forecasting? (DLinear)](https://arxiv.org/abs/2205.13504)
- Data: [[Danish Electricity Prices]]

---
Back to [[00 - Machine Learning Index]].
