---
tags: [ml, project, forecasting, classical]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Forecasting Aalborg Temperature

> [!summary] In one sentence
> Forecast the daily temperature in Aalborg 1, 3 and 7 days ahead from 7 years of DMI data, and beat both persistence and climatology with climatology plus an AR(1) decaying anomaly.

**Notebook:** [Project - Forecasting Aalborg Temperature](Project%20-%20Forecasting%20Aalborg%20Temperature.ipynb) · topic: [[Classical Forecasting Models]] · all projects: [[Projects Overview]]

## What you build
1. `climatology`: smoothed day-of-year normals (circular 31-day window).
2. `forecast`: $\text{clim}_{\text{target}}+\phi^h(x_{\text{today}}-\text{clim}_{\text{today}})$.

## Reference results (solution, laptop CPU)
Test MAE in °C, 2023–2024 (train 2018–2022, fitted φ = 0.80):

| horizon | persistence | climatology | **clim + AR(1)** |
|---|---|---|---|
| 1 day | 1.35 | 2.33 | **1.32** |
| 3 days | 2.33 | 2.33 | **2.02** |
| 7 days | 2.93 | 2.33 | **2.27** |

## Check yourself
> [!question]- Why does persistence win at 1 day but lose at 7?
> Weather anomalies last a few days (φ = 0.8 per day), so tomorrow resembles today; after a week only 0.8⁷ ≈ 0.21 of today's anomaly is left, and the normal for the date is a better guess.

> [!question]- How is this related to ARIMA?
> It's an AR(1) model on the deseasonalised series, with a deterministic seasonal component, which is a special case of seasonal ARIMA.

## Learn more
- [DMI frie data](https://www.dmi.dk/frie-data) · related: [[Danish Electricity Prices]]

---
Back to [[00 - Machine Learning Index]].
