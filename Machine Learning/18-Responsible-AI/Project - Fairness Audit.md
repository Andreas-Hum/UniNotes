---
tags: [ml, project, fairness]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Fairness Audit

> [!summary] In one sentence
> Audit an income classifier on the Adult census data for demographic parity, equal opportunity and equalised odds between men and women, then close the TPR gap with group thresholds and see what it costs.

**Notebook:** [Project - Fairness Audit](Project%20-%20Fairness%20Audit.ipynb) · topic: [[Explainability and Fairness]] · all projects: [[Projects Overview]]

## What you build
1. `group_rates`: selection rate, TPR and FPR per group.
2. `equal_opportunity_thresholds`: per-group thresholds that hit the same TPR.

## Reference results (solution, laptop CPU)
| | women | men |
|---|---|---|
| base rate (>50K) | 11.1 % | 30.4 % |
| selection / TPR / FPR, threshold 0.5 | 0.082 / 0.579 / 0.020 | 0.257 / 0.665 / 0.079 |
| after group thresholds (0.257 / 0.398) | 0.135 / **0.75** / 0.058 | 0.320 / **0.75** / 0.133 |

Accuracy 0.874 → 0.861. The TPR gap closes, but selection and FPR gaps remain: when base rates differ you can't satisfy every definition at once.

## Check yourself
> [!question]- Sex wasn't a feature. How can the model still treat the groups differently?
> Proxies: relationship ("husband"/"wife"), occupation and hours correlate with sex. Removing a column doesn't remove the information (fairness through unawareness fails).

> [!question]- Why is it impossible to have calibration, equal TPR and equal FPR together when base rates differ?
> Kleinberg et al. (2016) and Chouldechova (2017) proved these conditions are only compatible with a perfect predictor or equal base rates.

## Learn more
- [Kleinberg, Mullainathan, Raghavan – Inherent Trade-Offs in the Fair Determination of Risk Scores](https://arxiv.org/abs/1609.05807)
- IT-ret link: GDPR art. 22 on automated decisions in [[Lektion 3 - Behandlingsgrundlag og de registreredes rettigheder]]

---
Back to [[00 - Machine Learning Index]].
