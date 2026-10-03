---
tags: [ml, project, neural-networks, backprop]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Neural Net in Pure NumPy

> [!summary] In one sentence
> Write the forward pass and backpropagation of a 2-layer ReLU network by hand in NumPy, verify every gradient against finite differences, and train it to separate the two moons.

**Notebook:** [Project - Neural Net in Pure NumPy](Project%20-%20Neural%20Net%20in%20Pure%20NumPy.ipynb) · topic: [[Backpropagation]] · all projects: [[Projects Overview]]

## What you build
1. `forward`: linear → ReLU → linear → stable softmax.
2. `backward`: gradients of the mean cross-entropy via the chain rule.

## Reference results (solution, laptop CPU)
Analytic and numerical gradients agree to a relative error below 1e-5; after 3,000 full-batch steps the 32-unit network separates the moons with > 95 % training accuracy (decision-boundary plot in the notebook).

## Check yourself
> [!question]- Why is the gradient of softmax + cross-entropy simply p − onehot(y)?
> The softmax Jacobian and the log in cross-entropy cancel: ∂L/∂z_k = p_k − 1[k = y]. That's why frameworks fuse them.

> [!question]- Why subtract the row max before exp?
> exp(1000) overflows to inf. Softmax is invariant to adding a constant per row, so subtracting the max changes nothing mathematically but keeps the numbers finite.

---
Back to [[00 - Machine Learning Index]].
