---
tags: [ml, math, optimization]
---
# Calculus and Optimization

- **Gradient** points to steepest ascent; **Hessian** $H_{ij}=\partial^2 f/\partial x_i\partial x_j$ gives curvature.
- **Convex** $f$: any local minimum is global. Check $H\succeq0$. Linear/logistic regression and SVM objectives are convex; deep nets are not.
- **Stationary point** $\nabla f=0$: min, max or saddle (saddles dominate in high dimension).

## Constrained optimization
Lagrangian $\mathcal L(x,\lambda)=f(x)+\sum\lambda_i g_i(x)$.
**KKT** conditions: stationarity, primal/dual feasibility, complementary slackness. Basis of the dual form of [[Support Vector Machines]].

## Methods
| Method | Update | Note |
|---|---|---|
| [[Gradient Descent]] | $x\leftarrow x-\eta\nabla f$ | first order |
| Newton | $x\leftarrow x-H^{-1}\nabla f$ | quadratic convergence, costly |
| L-BFGS | quasi-Newton | good for small/medium problems |
| Coordinate descent | one variable at a time | Lasso |
| EM | alternate E and M | [[Gaussian Mixture Models and EM]] |

Deep learning variants: [[Optimizers]].

## Learn more
- [Mathematics for ML (free)](https://mml-book.github.io/) ch. 5 & 7
- [3Blue1Brown – Essence of Calculus](https://www.3blue1brown.com/lessons/essence-of-calculus/)
