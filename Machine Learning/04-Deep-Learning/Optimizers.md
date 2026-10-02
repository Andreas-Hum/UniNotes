---
tags: [ml, deep-learning, optimization]
---
# Optimizers

Build on [[Gradient Descent]].

| Optimizer | Key idea |
|---|---|
| SGD + momentum | velocity accumulates gradient |
| Nesterov | gradient at look-ahead point |
| AdaGrad | per-parameter rate $\eta/\sqrt{\sum g^2}$ |
| RMSProp | exponential moving average of $g^2$ |
| **Adam** | momentum + RMSProp with bias correction ($\beta_1=0.9,\beta_2=0.999,\epsilon=10^{-8}$) |
| **AdamW** | Adam with decoupled weight decay (default for Transformers) |
| Lion, Adafactor, LAMB | memory- or large-batch-oriented variants |

## Practical
- Adam: $\eta\approx10^{-3}$ (CNN/MLP), $10^{-4}$ for transformers; SGD+momentum often generalizes better for vision.
- Use warm-up + cosine/linear decay.
- Gradient clipping (norm 1.0) for [[RNN and LSTM]] and [[Transformers]].
