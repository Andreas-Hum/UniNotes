---
tags: [ml, causality, masters]
---
# Causal Inference

Prediction answers "what will happen?"; causal inference answers "what would happen **if we intervened**?". This matters for recommenders (what would the user have clicked without our recommendation?), A/B tests and policy decisions.

## Two frameworks
- **Potential outcomes (Rubin)**: $Y(1),Y(0)$; average treatment effect $\mathrm{ATE}=\mathbb E[Y(1)-Y(0)]$. We never observe both outcomes for the same unit.
- **Structural causal models (Pearl)**: DAGs + do-operator $p(y\mid do(x))\neq p(y\mid x)$. This extends the [[Probabilistic Graphical Models]] you already know.

## Key tools
| Tool | Use |
|---|---|
| Randomised experiments / A/B tests | gold standard |
| Backdoor adjustment | control for confounders blocking backdoor paths |
| Propensity scores, IPW | reweight observational data; also used in **unbiased recommender evaluation** ([[Evaluating Recommenders]]) |
| Instrumental variables, diff-in-diff, regression discontinuity | quasi-experiments |
| Uplift modelling, meta-learners (T-, S-, X-learner), causal forests | heterogeneous effects with ML |

Classic pitfalls: confounding, collider bias (the "explaining away" effect from d-separation), Simpson's paradox, selection bias.

## Learn more
- [Hernán & Robins — *Causal Inference: What If* (free)](https://miguelhernan.org/whatifbook)
- [Brady Neal — Introduction to Causal Inference (course + book)](https://www.bradyneal.com/causal-inference-course)
- Libraries: DoWhy, EconML, CausalML
