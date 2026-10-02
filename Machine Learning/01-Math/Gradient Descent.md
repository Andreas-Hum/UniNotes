---
tags: [ml, math, optimization]
---
# Gradient Descent

$$\theta_{t+1}=\theta_t-\eta\,\nabla_\theta L(\theta_t)$$

| Variant | Gradient computed on | Trade-off |
|---|---|---|
| Batch | all $N$ samples | exact, slow |
| **Stochastic (SGD)** | 1 sample | noisy, cheap, escapes bad minima |
| **Mini-batch** | $B$ samples (32–512) | standard; GPU friendly |

## Learning rate
- Too large → diverges/oscillates; too small → slow.
- For quadratics, stable if $\eta<2/\lambda_{max}(H)$.
- Schedules: step decay, cosine, warm-up, 1-cycle.

## Momentum
$v\leftarrow\beta v+\nabla L,\ \theta\leftarrow\theta-\eta v$ — smooths noise, accelerates along ravines. Adaptive variants in [[Optimizers]].

## Convergence
Convex + L-smooth: $O(1/t)$; strongly convex: linear rate. SGD needs decaying $\eta$.

## Debugging
Overfit a tiny batch first; check loss goes down; gradient-check numerically. See [[Training Tricks]].
