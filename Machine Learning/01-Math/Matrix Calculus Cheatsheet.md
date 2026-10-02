---
tags: [ml, math, cheatsheet]
---
# Matrix Calculus Cheatsheet

Denominator layout, gradients as column vectors.

| $f(x)$ | $\nabla_x f$ |
|---|---|
| $a^\top x$ | $a$ |
| $x^\top A x$ | $(A+A^\top)x$ ($=2Ax$ if symmetric) |
| $\lVert x\rVert^2$ | $2x$ |
| $\lVert Ax-b\rVert^2$ | $2A^\top(Ax-b)$ |
| $\ln\lvert A\rvert$ w.r.t. $A$ | $A^{-\top}$ |
| $\mathrm{tr}(AX)$ w.r.t. $X$ | $A^\top$ |

## Chain rule (vector)
If $z=g(y),\ y=h(x)$: $\nabla_x z = J_h(x)^\top\,\nabla_y z$. This is [[Backpropagation]].

## Common derivatives
- Sigmoid $\sigma'(z)=\sigma(z)(1-\sigma(z))$
- Softmax + cross-entropy: $\partial L/\partial z = \hat p - y$
- $\tanh' = 1-\tanh^2$, ReLU$'=\mathbb 1[z>0]$

Used in [[Linear Regression]], [[Logistic Regression]], [[Neural Networks]].
