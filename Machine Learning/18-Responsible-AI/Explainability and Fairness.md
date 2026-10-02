---
tags: [ml, responsible-ai]
---
# Explainability and Fairness

## Explainability
| Method | Scope | Idea |
|---|---|---|
| Intrinsically interpretable models | global | [[Linear Regression]], [[Decision Trees]], GAMs |
| Permutation importance | global | drop in score when a feature is shuffled |
| Partial dependence / ICE | global/local | effect of a feature on predictions |
| **LIME** | local | fit a simple surrogate around one prediction |
| **SHAP** | local + global | Shapley values from game theory; TreeSHAP is fast |
| Saliency / Grad-CAM / integrated gradients | local (deep nets) | gradient-based attribution ([[CNN]]) |
| Counterfactual explanations | local | smallest change that flips the decision |

## Fairness
- Sources of bias: historical data, sampling, labels, proxies, feedback loops ([[Recommender Systems Overview]]).
- Criteria: demographic parity, equalised odds, equal opportunity, calibration — generally **cannot all hold at once**.
- Mitigation: pre-processing (reweighting), in-processing (constraints), post-processing (group thresholds).
- Tools: Fairlearn, AIF360, SHAP.

## Resources
- [Molnar — *Interpretable Machine Learning* (free)](https://christophm.github.io/interpretable-ml-book/)
- [Barocas, Hardt, Narayanan — *Fairness and Machine Learning* (free)](https://fairmlbook.org/)
