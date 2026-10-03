---
tags: [ml, project, monitoring, drift]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Drift Detective

> [!summary] In one sentence
> Be on call for a DK1 price model trained on Oct 2023 – Jun 2024: measure input drift (PSI) and performance decay month by month, write an alert rule, and show that monthly retraining pays off.

**Notebook:** [Project - Drift Detective](Project%20-%20Drift%20Detective.ipynb) · topic: [[MLOps Overview]] · all projects: [[Projects Overview]]

## What you build
1. `psi`: the Population Stability Index against training deciles.
2. `alerts`: page on drift or on MAE decay.

Then a frozen vs. monthly-retrained model comparison.

## Reference results (solution, laptop CPU)
| | result |
|---|---|
| live MAE, frozen model | 23.07 EUR/MWh |
| live MAE, retrained monthly | **21.32 EUR/MWh** |
| alerts | almost every month (seasonality!) |

The alert rule fires constantly because wind and solar are seasonal: comparing July with an autumn–winter training set always looks like drift. That's alert fatigue, a real MLOps problem.

## Check yourself
> [!question]- PSI says the inputs drifted, but MAE barely moved. Is that a problem?
> Not necessarily. Data drift is an early warning, not a verdict. The model may extrapolate fine (e.g. more sun → lower prices it already understands). Act on performance when labels arrive; use drift when they don't.

> [!question]- How do you monitor a model whose labels arrive months later (e.g. loan defaults)?
> Input/prediction drift, proxy labels, and delayed evaluation cohorts.

## Learn more
- Data: [[Danish Electricity Prices]] · [Energi Data Service](https://www.energidataservice.dk/)

---
Back to [[00 - Machine Learning Index]].
