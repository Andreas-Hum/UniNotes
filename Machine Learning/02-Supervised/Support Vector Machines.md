---
tags: [ml, supervised, svm]
---
# Support Vector Machines

Find the hyperplane with **maximum margin** $2/\lVert w\rVert$.

## Hard margin
$\min\frac12\lVert w\rVert^2$ s.t. $y_i(w^\top x_i+b)\ge1$.

## Soft margin
$$\min\ \tfrac12\lVert w\rVert^2+C\sum_i\xi_i,\quad y_i(w^\top x_i+b)\ge1-\xi_i$$
Equivalent to hinge loss $\max(0,1-y f(x))$ + L2. Large $C$ → low bias; small $C$ → wide margin.

## Dual
$$\max_\alpha\sum\alpha_i-\tfrac12\sum\alpha_i\alpha_jy_iy_jx_i^\top x_j,\quad 0\le\alpha_i\le C$$
Only **support vectors** have $\alpha_i>0$. Data enters only via dot products ⇒ replace by a kernel ([[Kernel Methods]]). Derived with KKT ([[Calculus and Optimization]]).

## Kernels & hyperparameters
RBF $k(x,x')=\exp(-\gamma\lVert x-x'\rVert^2)$: tune $C$ and $\gamma$ on a log grid; scale features first.

Also: SVR (ε-insensitive regression), one-class SVM ([[Anomaly Detection]]).

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 9
- [scikit-learn – SVMs](https://scikit-learn.org/stable/modules/svm.html)
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 7
