---
tags: [ml, project, optimization]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Optimizer Race

> [!summary] In one sentence
> Race gradient descent, momentum and Adam down the Rosenbrock banana and a 1:100 ellipse, and see why momentum and per-coordinate step sizes exist.

**Notebook:** [Project - Optimizer Race](Project%20-%20Optimizer%20Race.ipynb) · topic: [[Gradient Descent]] · all projects: [[Projects Overview]]

## What you build
1. `momentum_step`: heavy-ball velocity update.
2. `adam_step`: first/second moments with bias correction.

## Reference results (solution, laptop CPU)
After 2,000 steps Adam ends below plain gradient descent on both landscapes (plots with paths in the notebook). On the ellipse, GD's learning rate is capped at 2/100 by the steep direction, so it crawls along the flat one.

## Check yourself
> [!question]- Why must GD's learning rate stay below 2/λ_max?
> Along an eigen-direction with curvature λ each step multiplies the error by (1 − ηλ); for |1 − ηλ| < 1 you need η < 2/λ. The steepest direction sets the limit for all directions.

> [!question]- Why does Adam's very first step have size ≈ lr, whatever the gradient's scale?
> After bias correction m̂ = g and v̂ = g², so the step is lr·g/|g| = ±lr per coordinate.

---
Back to [[00 - Machine Learning Index]].
