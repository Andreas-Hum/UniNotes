---
tags: [ml, project, autodiff, backprop]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Autodiff from Scratch

> [!summary] In one sentence
> Build the engine behind `loss.backward()`: a `Value` class that records a computation graph and runs reverse-mode automatic differentiation, then train a small neural network with nothing but your own autograd.

**Notebook:** [Project - Autodiff from Scratch](Project%20-%20Autodiff%20from%20Scratch.ipynb) · topic: [[Calculus and Optimization]] · all projects: [[Projects Overview]]

## What you build
1. `Value.__mul__`: forward product and its local gradients (accumulated with `+=`).
2. `Value.backward`: topological sort + chain rule from the output back.

## Reference results (solution, laptop CPU)
Gradients match finite differences on a composite function. A 2 → 8 → 8 → 1 tanh MLP (105 parameters) trained with your engine reaches **95 %** training accuracy on the moons in 60 steps.

## Check yourself
> [!question]- Why must gradients be accumulated with `+=`?
> A value used in several places (like x in xy + x²) receives gradient from every use: the multivariate chain rule sums over paths.

> [!question]- Why reverse mode and not forward mode for neural nets?
> One backward pass gives the gradient with respect to *all* parameters of a scalar loss; forward mode would need one pass per parameter.

---
Back to [[00 - Machine Learning Index]].
