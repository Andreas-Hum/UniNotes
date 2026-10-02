---
tags: [ml, time-series]
---
# Time Series Forecasting

## Concepts
Trend, seasonality, cycles, noise; **stationarity** (ADF/KPSS tests, differencing); autocorrelation (ACF/PACF).

## Models
| Family | Examples |
|---|---|
| Baselines | naive, seasonal naive, moving average — always compare! |
| Exponential smoothing | SES, Holt, Holt–Winters, ETS |
| ARIMA family | AR, MA, ARIMA, SARIMA(X) |
| Decomposition | STL, Prophet |
| ML with lag features | LightGBM/XGBoost on lags, rolling stats, calendar features ([[Ensemble Methods]]) |
| Deep | [[RNN and LSTM]], TCN, N-BEATS, DeepAR, Temporal Fusion Transformer, PatchTST |
| State space | Kalman filters ([[Probabilistic Graphical Models]]) |

## Evaluation
Rolling-origin / time-series CV — never shuffle ([[Cross-Validation and Model Selection]]). Metrics: MAE, RMSE, MAPE, sMAPE, MASE; probabilistic: pinball loss, CRPS.

## Resources
- [Hyndman & Athanasopoulos — *Forecasting: Principles and Practice* (free)](https://otexts.com/fpp3/)
- Libraries: statsmodels, Prophet, sktime, Darts, Nixtla (statsforecast/neuralforecast), GluonTS
