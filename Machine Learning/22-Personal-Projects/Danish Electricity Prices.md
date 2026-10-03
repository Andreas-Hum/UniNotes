---
tags: [ml, project, time-series, forecasting]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Danish Electricity Prices

> [!summary] In one sentence
> Forecast tomorrow's hourly spot price in DK1 (Aalborg's price area) from Energinet's open data and discover that price history alone can't beat "same as yesterday", while adding the day-ahead wind and solar forecast cuts the error by a quarter.

**Notebook:** [Danish Electricity Prices - Notebook](Danish%20Electricity%20Prices%20-%20Notebook.ipynb) · part of [[Personal Projects]]

## Intuition first
Denmark gets a large share of its power from wind. When it's windy, cheap wind power floods the market and prices fall, sometimes **below zero** (864 negative hours in our two years). Yesterday's price can't know that tomorrow will be stormy; the wind forecast can. Domain knowledge beats a fancier model.

## What you build (4 TODOs)
1. `add_calendar`: hour/weekday/month in **Danish** time (handles daylight saving time).
2. `add_lags`: price lags of ≥ 24 h only, because the auction closes at noon the day before.
3. `mae`: the metric (EUR/MWh).
4. `add_weather`: pivot Energinet's day-ahead wind (offshore + onshore) and solar forecasts into features.

Plus error analysis (MAE by hour, worst day, negative prices), an extension with **DMI** temperature, and a **live** cell that forecasts tomorrow from today's data.

## Reference results (train Oct 2023 – Dec 2024, test all of 2025)
| model | test MAE (EUR/MWh) |
|---|---|
| same hour last week | 37.71 |
| same hour yesterday | 29.55 |
| gradient boosting, price history + calendar | 29.62 |
| **+ wind & solar day-ahead forecasts** | **21.75** |
| + DMI temperature (Aalborg) | 21.81 |

Temperature didn't help: once you know the wind, it adds little in this market (and we even cheated a bit by using *observed* temperature).

## Data sources (all free, no API key)
- [Energi Data Service](https://www.energidataservice.dk/): [Elspotprices](https://www.energidataservice.dk/tso-electricity/Elspotprices) (hourly, ends 30 Sep 2025), [DayAheadPrices](https://www.energidataservice.dk/tso-electricity/DayAheadPrices) (15-minute, from 1 Oct 2025), [Forecasts_Hour](https://www.energidataservice.dk/tso-electricity/Forecasts_Hour) (wind/solar).
- [DMI frie data](https://www.dmi.dk/frie-data): the `metObs` API, station `06030` = Flyvestation Aalborg.
- Copenhagen's [fixed bike counts](https://www.opendata.dk/city-of-copenhagen/faste-cykeltaellinger) (Excel, 2005–2014): a side project combining them with DMI rain.

## Common confusions
- **Leakage through lags**: `lag1` looks amazing in a backtest but doesn't exist at forecast time (tomorrow's prices are set in one auction). Always ask "what would I know at noon yesterday?"
- **UTC vs. local time**: the API gives both; mixing them shifts the daily pattern by 1–2 hours and breaks twice a year.
- **One MAE number**: errors concentrate in a few volatile days (price spikes, negative prices). Look at the worst day.

## Check yourself
> [!question]- Why is "same hour last week" worse than "same hour yesterday", even though it captures the weekly cycle?
> Weather persists for a few days, so yesterday's price shares tomorrow's weather regime more often than last week's does. The weekly pattern is small next to the wind effect.

> [!question]- The model predicted only 142 of the 411 negative-price hours in 2025. Why is that hard?
> Negative prices come from extreme wind + low demand + export limits, which are rare tails in the training data. Gradient boosting with MAE-like behaviour shrinks towards typical values. A quantile model or a separate "will it go negative?" classifier helps.

## Learn more
- Vault: [[Time Series Forecasting]] · [[Time Series Validation and Features]] · [[Classical Forecasting Models]] · [[Ensemble Methods]]
