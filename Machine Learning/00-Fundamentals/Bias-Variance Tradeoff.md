---
tags: [ml, fundamentals, theory]
---
# Bias-Variance Tradeoff

For squared loss with $y = f(x) + \varepsilon$, $\mathrm{Var}(\varepsilon)=\sigma^2$, the expected test error at $x$ decomposes as

$$\mathbb{E}\big[(y-\hat f(x))^2\big] = \underbrace{\big(\mathbb{E}[\hat f(x)]-f(x)\big)^2}_{\text{bias}^2} + \underbrace{\mathbb{E}\big[(\hat f(x)-\mathbb{E}\hat f(x))^2\big]}_{\text{variance}} + \underbrace{\sigma^2}_{\text{irreducible}}$$

| | High bias | High variance |
|---|---|---|
| Symptom | train and val error both high | train error low, val error high |
| Cause | model too simple | model too flexible / too little data |
| Fix | richer model, more features | more data, [[Overfitting and Regularization\|regularization]], bagging ([[Ensemble Methods]]) |

> [!note] Modern caveat
> Over-parameterized deep nets show **double descent**: test error can fall again past the interpolation threshold.

Related: [[Cross-Validation and Model Selection]].
