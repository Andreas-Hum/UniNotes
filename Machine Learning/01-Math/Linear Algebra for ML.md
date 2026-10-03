---
tags: [ml, math, linear-algebra]
status: not-started
notebook: not-started
level:
reviewed:
---
# Linear Algebra for ML

> [!summary] In one sentence
> Linear algebra is the language ML is written in: data are matrices, models are matrix–vector products, and the key tools (eigenvectors, SVD, least squares, projections) tell you which directions in the data matter and how to solve for the best linear fit.

## Intuition first

A dataset with $n$ samples and $d$ features is a table of numbers: a matrix $X\in\mathbb R^{n\times d}$, one row per sample. Almost every model starts by multiplying that matrix by something: a weight vector ([[Linear Regression]]), a weight matrix (a layer of a neural network), or a set of directions ([[PCA]]). So it pays to think of a matrix not as a grid of numbers but as a **machine that moves space around**: it rotates, stretches, squashes and shears every vector you feed it.

Seen this way, the big ideas become geometric:
- **Dot product**: how much two vectors point the same way. Similarity scores, projections and neuron pre-activations are all dot products.
- **Eigenvectors**: the special directions a matrix only stretches, never turns. They are the "natural axes" of the transformation.
- **SVD**: *every* matrix is a rotation, then a stretch along the axes, then another rotation. The stretch factors tell you how much each direction matters; dropping the small ones compresses data (PCA).
- **Least squares**: when $Xw=y$ has no exact solution (more equations than unknowns, plus noise), find the $w$ whose prediction $Xw$ is as close as possible to $y$. Geometrically: drop a perpendicular from $y$ onto the space of all possible predictions.

**What problem does it solve?** It lets you write a whole dataset's computation as one expression ($Xw$ instead of a loop), reason about when a problem has a unique solution (rank, invertibility), and find the important structure in high-dimensional data (eigen/SVD).

## The math, step by step

### Essentials
- **Dot product** $a^\top b=\sum_i a_ib_i=\lVert a\rVert\lVert b\rVert\cos\theta$, where $\theta$ is the angle between $a$ and $b$. Positive: same general direction; zero: orthogonal; negative: opposite. Dividing by the norms gives **cosine similarity** $\cos\theta$.
- **Norms** measure length:
  - $\lVert x\rVert_1=\sum_i|x_i|$ (Manhattan; used in L1/Lasso, encourages sparsity),
  - $\lVert x\rVert_2=\sqrt{\sum_i x_i^2}$ (Euclidean; $\lVert x\rVert_2^2=x^\top x$),
  - $\lVert x\rVert_\infty=\max_i|x_i|$ (the largest coordinate).
- **Matrix product** $(AB)_{ij}=\sum_k A_{ik}B_{kj}$: entry $(i,j)$ is the dot product of row $i$ of $A$ with column $j$ of $B$. Shapes must chain: $(m\times n)(n\times p)\to m\times p$. Geometrically $AB$ means "first apply $B$, then $A$", which is why it is **not commutative** ($AB\neq BA$ in general).
- **Transpose of a product**: $(AB)^\top=B^\top A^\top$ (order reverses, like taking off socks and shoes).
- **Rank** = number of linearly independent columns = dimension of the **column space** (all vectors $Ax$ can reach). The **null space** is all $x$ with $Ax=0$: directions the matrix flattens to nothing. For a square $A$: invertible ⇔ full rank ⇔ $\det\neq0$ ⇔ null space is only $\{0\}$. $\det$ is the factor by which $A$ scales areas/volumes, so $\det=0$ means some dimension is squashed flat and cannot be undone.
- **Positive semi-definite** $A\succeq0$: $x^\top Ax\ge0$ for all $x$ (equivalently, for symmetric $A$, all eigenvalues $\ge0$). Covariance and kernel matrices are PSD ([[Kernel Methods]]). Why: a covariance or Gram matrix has the form $A=B^\top B$, and $x^\top B^\top Bx=\lVert Bx\rVert^2\ge0$. Its quadratic form $x^\top Ax$ is a bowl that never dips below zero.

### Eigen & SVD

![A symmetric matrix transforming the plane: eigenvectors stay on their own line](../../Attachments/ML%20Animations/Linear%20Algebra%20for%20ML%20-%20eigenvectors.gif)
*Watch the yellow and teal arrows: while the grid shears, they stay on their dashed lines and only stretch (by 3 and by 1). The red arrow is knocked off its line, so it is not an eigenvector.*

- $Av=\lambda v$: $v\neq0$ is an **eigenvector** (a direction $A$ does not rotate) and $\lambda$ its **eigenvalue** (the stretch factor; negative means flipped). Find $\lambda$ from $\det(A-\lambda I)=0$, then $v$ from the null space of $A-\lambda I$.
- **Symmetric** $A$ (like covariance matrices): $A=Q\Lambda Q^\top$ with orthonormal $Q$ (columns are perpendicular unit eigenvectors) and real eigenvalues on the diagonal of $\Lambda$. Read right to left: rotate into the eigen-axes ($Q^\top$), stretch each axis by $\lambda_i$ ($\Lambda$), rotate back ($Q$).
- **SVD**: $X=U\Sigma V^\top$ works for *any* $n\times d$ matrix. $V$ (right singular vectors) and $U$ (left singular vectors) are orthonormal, $\Sigma$ is diagonal with **singular values** $\sigma_1\ge\sigma_2\ge\dots\ge0$.
  - Link to eigen: $X^\top X=V\Sigma^2V^\top$ and $XX^\top=U\Sigma^2U^\top$, so $\sigma_i=\sqrt{\lambda_i(X^\top X)}$. Unlike eigendecomposition, SVD exists for non-square and non-symmetric matrices and the singular values are never negative.
  - Number of non-zero $\sigma_i$ = rank of $X$.
- **Best rank-$k$ approximation**: keep the top $k$ singular values and their vectors, $X_k=\sum_{i=1}^k\sigma_iu_iv_i^\top$ (Eckart–Young). No other rank-$k$ matrix is closer; the error is $\lVert X-X_k\rVert_F=\sqrt{\sum_{i>k}\sigma_i^2}$ (and $\sigma_{k+1}$ in spectral norm). This is the basis of [[PCA]]: on centred data, $V$'s columns are the principal directions and $\sigma_i^2/(n-1)$ the variances along them.

![SVD as rotate, stretch, rotate](../../Attachments/ML%20Animations/Linear%20Algebra%20for%20ML%20-%20SVD%20rotate%20stretch%20rotate.gif)
*Follow the unit circle: $V^\top$ rotates $v_1,v_2$ onto the axes, $\Sigma$ stretches them into an ellipse with semi-axes $\sigma_1,\sigma_2$, $U$ rotates the ellipse into place. The dashed orange ellipse (applying $X$ directly) lands exactly on top.*

### Least squares
We want $w$ with $Xw\approx y$. Minimize $\lVert Xw-y\rVert^2$:
1. Expand: $\lVert Xw-y\rVert^2=w^\top X^\top Xw-2w^\top X^\top y+y^\top y$.
2. Gradient (see [[Matrix Calculus Cheatsheet]]): $2X^\top Xw-2X^\top y$.
3. Set it to zero → the **normal equations** $X^\top Xw=X^\top y$.
4. If $X^\top X$ is invertible (full column rank), $w=(X^\top X)^{-1}X^\top y$. In general, $w=X^+y$ with the **pseudo-inverse** $X^+=V\Sigma^+U^\top$ ($\Sigma^+$ inverts the non-zero singular values and leaves zeros as zeros).

When there are more unknowns than samples ($d>n$, under-determined) there are infinitely many exact solutions; $X^+y$ picks the one with the **smallest norm**. In practice use `np.linalg.lstsq` or a QR/SVD solver rather than forming the inverse, because $X^\top X$ squares the condition number. See [[Linear Regression]].

### Projection
The prediction $\hat y=Xw$ is the point of the column space closest to $y$, and the residual $y-\hat y$ is perpendicular to every column ($X^\top(y-\hat y)=0$ is exactly the normal equations). The matrix that does this is the projection onto col($X$):
$$P=X(X^\top X)^{-1}X^\top,\qquad \hat y=Py.$$
Projections are idempotent ($P^2=P$: projecting twice changes nothing) and symmetric.

### Useful identities
- $\mathrm{tr}(AB)=\mathrm{tr}(BA)$ (cyclic; the shapes only need to make both products square), $\mathrm{tr}(A)=\sum\lambda_i$, $\det A=\prod\lambda_i$.
- $(A+UCV)^{-1}$ **Woodbury lemma**: cheap updates of inverses,
  $(A+UCV)^{-1}=A^{-1}-A^{-1}U\,(C^{-1}+VA^{-1}U)^{-1}\,VA^{-1}$.
  If $A^{-1}$ is known and the update is low rank ($U$ is $n\times k$ with small $k$), you only invert a $k\times k$ matrix. The rank-1 case is **Sherman–Morrison**: $(A+uv^\top)^{-1}=A^{-1}-\frac{A^{-1}uv^\top A^{-1}}{1+v^\top A^{-1}u}$. Used for online least squares and in [[Gaussian Processes]]-style kernel algebra.
- Gradients: [[Matrix Calculus Cheatsheet]].

### Algorithms you will implement
- **Gram–Schmidt / QR**: orthonormalize the columns of $X$ one by one (subtract the projections onto the previous ones, normalize), giving $X=QR$ with orthonormal $Q$ and upper-triangular $R$. Least squares then becomes $Rw=Q^\top y$.
- **Power iteration**: repeat $v\leftarrow Av/\lVert Av\rVert$. Each step multiplies the component along eigenvector $i$ by $\lambda_i$, so the dominant eigenvector wins; convergence speed depends on $|\lambda_2/\lambda_1|$. This is how PageRank and many large-scale eigen-solvers work.

## Worked example

Take $A=\begin{bmatrix}2&1\\1&2\end{bmatrix}$ (the matrix in the animation).
1. $\det(A-\lambda I)=(2-\lambda)^2-1=0\Rightarrow\lambda\in\{3,1\}$.
2. $\lambda=3$: $(A-3I)v=0\Rightarrow v_1=\tfrac1{\sqrt2}(1,1)$. $\lambda=1$: $v_2=\tfrac1{\sqrt2}(1,-1)$. They are orthogonal, as promised for a symmetric matrix.
3. Check identities: $\mathrm{tr}A=4=3+1$ and $\det A=3=3\cdot1$. Both eigenvalues are positive, so $A\succ0$.

Projection and least squares with one feature: $X=\begin{bmatrix}1\\1\end{bmatrix}$, $y=\begin{bmatrix}1\\3\end{bmatrix}$.
1. $X^\top X=2$, $X^\top y=4$, so $w=4/2=2$ (the best constant fit is the mean).
2. $P=X(X^\top X)^{-1}X^\top=\tfrac12\begin{bmatrix}1&1\\1&1\end{bmatrix}$, so $\hat y=Py=(2,2)$.
3. Residual $y-\hat y=(-1,1)$, and $X^\top(y-\hat y)=-1+1=0$: perpendicular, as the geometry says.

## Common confusions
- **"$AB=BA$."** → Only in special cases (e.g. both diagonal). Order matters because it is the order in which transformations are applied.
- **"Eigenvalues and singular values are the same thing."** → Only for symmetric PSD matrices. In general $\sigma_i=\sqrt{\lambda_i(X^\top X)}$; singular values are always $\ge0$ and exist for any shape.
- **"Solve least squares with `inv(X.T @ X) @ X.T @ y`."** → Works on paper, but is numerically fragile (squares the condition number) and fails when $X^\top X$ is singular. Use `lstsq`, QR or SVD.
- **"PSD means all entries are positive."** → No: $\begin{bmatrix}1&-1\\-1&1\end{bmatrix}$ is PSD with negative entries, and $\begin{bmatrix}1&2\\2&1\end{bmatrix}$ has positive entries but eigenvalue $-1$.
- **"Rank is the number of non-zero rows."** → It is the number of *linearly independent* rows (or columns); duplicate or combined rows do not count.

## Check yourself

> [!question]- Why is every covariance matrix PSD?
> $\Sigma=\frac1{n-1}X_c^\top X_c$ for centred data $X_c$, so $v^\top\Sigma v=\frac1{n-1}\lVert X_cv\rVert^2\ge0$. In words: $v^\top\Sigma v$ is the variance of the data projected onto $v$, and a variance cannot be negative.

> [!question]- A $3\times3$ matrix has eigenvalues $2,0,5$. Is it invertible? What are its trace and determinant?
> Not invertible: an eigenvalue of 0 means some direction is squashed to zero ($\det=2\cdot0\cdot5=0$). Trace $=2+0+5=7$.

> [!question]- You keep the top 2 of singular values $(5,3,1)$. What is the Frobenius error of the approximation?
> $\sqrt{\sum_{i>2}\sigma_i^2}=\sqrt{1}=1$. The fraction of "energy" kept is $(25+9)/35\approx97\%$.

> [!question]- With $d>n$ (more features than samples), what does $w=X^+y$ return?
> One of infinitely many exact solutions: the one with the smallest $\lVert w\rVert_2$. That is also the limit of ridge regression as $\lambda\to0$.

> [!question]- What does power iteration converge to, and when is it slow?
> To the eigenvector of the largest-magnitude eigenvalue. It is slow when $|\lambda_2|/|\lambda_1|$ is close to 1 (the top two eigenvalues are nearly tied).

## Practice
[Linear Algebra for ML - Exercises](Linear%20Algebra%20for%20ML%20-%20Exercises.ipynb): rank and invertibility, PSD proofs, SVD vs eigendecomposition, projections, Sherman–Morrison, and from-scratch matrix product, Gram–Schmidt QR, power iteration, Eckart–Young and the pseudo-inverse.

## Learn more
- [Mathematics for ML (free)](https://mml-book.github.io/) ch. 2–4
- [3Blue1Brown – Essence of Linear Algebra](https://www.3blue1brown.com/lessons/eola-preview/): the source of the "matrix as a transformation of space" picture; chapters on eigenvectors and change of basis pair well with this note.
- [MIT 18.06 – Strang](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)
- [Stanford CS229 – Linear Algebra Review and Reference (PDF)](https://cs229.stanford.edu/section/cs229-linalg.pdf)
