---
tags: [ml, fundamentals, evaluation]
---
# Cross-Validation and Model Selection

## Splits
- **Train** fits parameters · **Validation** tunes hyperparameters · **Test** touched once at the end.

## k-fold CV
Split into $k$ folds; train on $k-1$, validate on 1; average. Typical $k=5$ or $10$.
- **Stratified** — preserve class ratios.
- **Leave-one-out** — $k=N$, low bias, high cost.
- **Group k-fold** — keep related samples (same patient/user) together.
- **Time-series split** — only train on the past. Never shuffle temporal data.

## Nested CV
Outer loop estimates generalization; inner loop tunes hyperparameters. Avoids optimistic bias.

## Hyperparameter search
Grid → random (often better) → Bayesian optimization (Optuna, Hyperopt) → successive halving / Hyperband.

## Information criteria
$\mathrm{AIC}=2k-2\ln\hat L$, $\mathrm{BIC}=k\ln N-2\ln\hat L$ — penalize model complexity.

> [!danger] Data leakage
> Fit scalers, imputers, feature selectors **inside** each fold (use a pipeline). See [[Common Pitfalls]].
