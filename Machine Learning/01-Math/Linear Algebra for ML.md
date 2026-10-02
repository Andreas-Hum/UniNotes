---
tags: [ml, math, linear-algebra]
---
# Linear Algebra for ML

## Essentials
- Dot product $a^\top b=\lVert a\rVert\lVert b\rVert\cos\theta$; norms $\lVert x\rVert_1,\lVert x\rVert_2,\lVert x\rVert_\infty$.
- Matrix product $(AB)_{ij}=\sum_k A_{ik}B_{kj}$, not commutative; $(AB)^\top=B^\top A^\top$.
- Rank, null space, column space; invertible ⇔ full rank ⇔ $\det\neq0$.
- **Positive semi-definite** $A\succeq0$: $x^\top Ax\ge0$ ∀x. Covariance and kernel matrices are PSD ([[Kernel Methods]]).

## Eigen & SVD
- $Av=\lambda v$. Symmetric $A=Q\Lambda Q^\top$ with orthonormal $Q$.
- **SVD**: $X=U\Sigma V^\top$. Best rank-$k$ approximation: keep top $k$ singular values (Eckart–Young). Basis of [[PCA]].

## Least squares
Minimize $\lVert Xw-y\rVert^2$ → normal equations $X^\top Xw=X^\top y$ → $w=X^+y$ (pseudo-inverse). See [[Linear Regression]].

## Projection
Projection onto col($X$): $P=X(X^\top X)^{-1}X^\top$.

## Useful identities
- $\mathrm{tr}(AB)=\mathrm{tr}(BA)$, $\mathrm{tr}(A)=\sum\lambda_i$, $\det A=\prod\lambda_i$
- $(A+UCV)^{-1}$ Woodbury lemma: cheap updates of inverses
- Gradients: [[Matrix Calculus Cheatsheet]]

## Learn more
- [Mathematics for ML (free)](https://mml-book.github.io/) ch. 2–4
- [3Blue1Brown – Essence of Linear Algebra](https://www.3blue1brown.com/lessons/eola-preview/)
- [MIT 18.06 – Strang](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)
