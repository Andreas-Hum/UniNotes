---
tags: [ml, time-series, evaluation, features]
status: not-started
level:
reviewed:
---
# Time Series Validation and Features

> [!summary] In one sentence
> Time series must be validated by **training on the past and testing on the future** (rolling-origin backtests), and when you turn forecasting into a tabular ML problem the features (lags, rolling statistics, calendar) must only use information available at prediction time.

## Intuition first
In ordinary ML, rows are independent, so random cross-validation is fine. In time series, yesterday tells you a lot about today. If the model trains on Wednesday and is tested on Tuesday, it has "seen the future": scores look great and production performance collapses. Every rule below comes from one principle: **at prediction time, you only know the past.**

## Validation schemes
| Scheme | How | When |
|---|---|---|
| **Single holdout** | train on everything before date $T$, test after | quick check |
| **Expanding window** (rolling origin) | train on $[0,T_k]$, test on $(T_k,T_k+H]$ for several origins $T_1<T_2<\dots$ | standard; uses all history |
| **Sliding window** | fixed-length training window that moves forward | when old data is no longer representative |
| **Gap / embargo** | leave a gap between train and test | when features use long windows or labels overlap in time |
`sklearn.model_selection.TimeSeriesSplit` implements the expanding window. Report the **average over origins**, per horizon step if possible – errors usually grow with the horizon.

## Metrics
| Metric | Formula | Notes |
|---|---|---|
| MAE | $\frac1n\sum|y-\hat y|$ | scale-dependent; optimal forecast = median |
| RMSE | $\sqrt{\frac1n\sum(y-\hat y)^2}$ | punishes large errors; optimal = mean |
| MAPE | $\frac{100}{n}\sum\left|\frac{y-\hat y}{y}\right|$ | undefined at $y=0$; asymmetric |
| sMAPE | $\frac{100}{n}\sum\frac{2|y-\hat y|}{|y|+|\hat y|}$ | bounded, still awkward near 0 |
| **MASE** | $\dfrac{\text{MAE}}{\frac1{T-m}\sum_{t=m+1}^T|y_t-y_{t-m}|}$ | scaled by in-sample seasonal-naive error; < 1 beats seasonal naive; comparable across series |
| Pinball / CRPS | quantile / full-distribution loss | probabilistic forecasts |
| Coverage | share of actuals inside the prediction interval | should match the nominal level (e.g. 80 %) |

## Forecasting as supervised learning
To use LightGBM/XGBoost (the winners of the M5 competition), build one row per (series, time) with target $y_{t+h}$ and features known at time $t$:
- **Lags:** $y_{t},y_{t-1},y_{t-7},y_{t-364}$ (same day last week/year).
- **Rolling statistics:** mean, std, min, max over the last 7/28 days – computed on data **up to $t$** (shift before rolling!).
- **Calendar:** day of week, month, holiday flags, days to the next holiday, payday. Cyclic encoding: $\sin(2\pi\cdot\text{dow}/7),\cos(2\pi\cdot\text{dow}/7)$.
- **Known future covariates:** price, planned promotions, weather forecasts.
- **Static:** store, category, series id (target-encode carefully, inside folds).
- **Trend:** time index, or train on differences/ratios – trees cannot extrapolate beyond the target range they saw.

```python
df = df.sort_values(["id", "date"])
g = df.groupby("id")["y"]
df["lag_7"] = g.shift(7)
df["roll_mean_28"] = g.transform(lambda s: s.shift(1).rolling(28).mean())  # shift first!
df["dow"] = df["date"].dt.dayofweek
```

## Common leakage traps
- **Rolling features without shifting** include the current target.
- **Scaling/imputing on the full series** before splitting uses future statistics.
- **Random K-fold** on time-ordered rows.
- **Features not available at prediction time** (actual weather instead of the forecast; final sales figures that arrive a week late).
- **Horizon mismatch:** a lag-1 feature is unusable if you must forecast 7 days ahead – use lags ≥ horizon (or a direct model per horizon).

## Worked example: MASE
Seasonal-naive in-sample MAE ($m=7$) is 20 units. Your model's test MAE is 15. MASE $=15/20=0.75$ → 25 % better than seasonal naive. A MASE of 1.2 would mean the model is worse than simply repeating last week.

## Common confusions
- **"MAPE is the most intuitive metric, so use it."** → It explodes near zero and favours under-forecasting; prefer MASE or a weighted MAPE (sum of errors / sum of actuals).
- **"More history is always better."** → Structural breaks (COVID, a new pricing policy) can make old data harmful; try a sliding window.
- **"Trees can forecast trends."** → They predict within the range seen in training; detrend or add linear models.

## Check yourself
> [!question]- You forecast 14 days ahead. Can you use $y_{t-1}$ as a feature in a direct model?
> No – at forecast time $y_{t-1}$ for the later days is unknown. Use lags of at least 14, or a recursive/multi-model approach.

> [!question]- Why shift by 1 before computing a rolling mean feature?
> Otherwise the window includes the current value, i.e. the target – leakage.

> [!question]- What does a MASE of exactly 1 mean?
> The model's error equals the in-sample error of seasonal naive.

## Learn more
- [Hyndman & Athanasopoulos — *Forecasting: Principles and Practice*, ch. 5 (evaluation)](https://otexts.com/fpp3/)
- Makridakis, Spiliotis & Assimakopoulos (2022), *M5 accuracy competition: Results, findings, and conclusions*, International Journal of Forecasting
- `sklearn.model_selection.TimeSeriesSplit`, `sktime`, `mlforecast`

See [[Time Series Forecasting]], [[Cross-Validation and Model Selection]], [[Feature Engineering]], [[Common Pitfalls]].
