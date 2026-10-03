---
tags: [ml, project, anomaly-detection]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Price Anomaly Hunter

> [!summary] In one sentence
> Hunt anomalies in 2024 DK1 electricity prices with a robust rolling z-score and an Isolation Forest, measure precision and recall on planted glitches, and learn that the right feature matters more than the detector.

**Notebook:** [Project - Price Anomaly Hunter](Project%20-%20Price%20Anomaly%20Hunter.ipynb) · topic: [[Anomaly Detection]] · all projects: [[Projects Overview]]

## What you build
1. `robust_z`: rolling median + MAD z-score.
2. `precision_recall` for a set of flagged hours.

## Reference results (solution, laptop CPU)
30 planted glitches, budget of 30 flags:

| detector | precision = recall |
|---|---|
| robust z on the price level | 0.37 |
| Isolation Forest (price, diffs, hour) | 0.63 |
| **robust z on spikiness** (hour minus neighbours' mean) | **0.70** |

On the real data, the extreme hours are genuine market events (e.g. 936 EUR/MWh on 12 Dec 2024 16:00 UTC), not errors.

## Check yourself
> [!question]- Why median and MAD instead of mean and standard deviation?
> The anomalies inflate the std and pull the mean, hiding themselves. Median and MAD have a 50 % breakdown point: up to half the window can be outliers.

> [!question]- The detector flagged real negative prices. Is it wrong?
> It found *unusual* hours, which is its job. Whether unusual means *wrong* needs domain knowledge (here: windy Sundays are real).

## Learn more
- Data: [[Danish Electricity Prices]] · [Energi Data Service](https://www.energidataservice.dk/)

---
Back to [[00 - Machine Learning Index]].
