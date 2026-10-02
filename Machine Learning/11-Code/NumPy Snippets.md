---
tags: [ml, code, numpy]
---
# NumPy Snippets

> [!summary] In one sentence
> A handful of vectorized NumPy one-liners (least squares, ridge, standardization, stable softmax, logistic-regression GD, PCA via SVD, pairwise distances, k-means) implement most classic ML algorithms; they all rest on two ideas: matrix products replace loops over samples, and broadcasting lines up arrays of different shapes without copying.

## Intuition first

Python loops are slow (each iteration is interpreted); NumPy operations run in compiled C over whole arrays. So the skill is to *think in arrays*: instead of "for each sample, compute its prediction", write "predictions = data matrix times weights", `X @ w`, and let one call do $n$ dot products.

When arrays have different shapes, **broadcasting** stretches the size-1 axes so they match, like a spreadsheet formula dragged across a row or down a column. That is how you subtract a mean vector from every row, or compute an $n\times m$ table of distances from two lists of points, in one line.

**Shape discipline** is the whole game. Before running a line, say the shapes out loud: `X` is `(n, d)` (rows = samples), `w` is `(d,)`, so `X @ w` is `(n,)`. Most bugs are shape bugs that broadcasting silently "fixed".

## Broadcasting: the rule behind half the snippets

![Broadcasting a column of shape (3,1) with a row of shape (1,4)](../../Attachments/ML%20Animations/NumPy%20Snippets%20-%20broadcasting%20a%20column%20plus%20a%20row.gif)
*Watch the blue column get stretched across 4 columns and the green row down 3 rows; only then are they added element by element into a $(3,4)$ result. NumPy does this without actually copying (stride 0).*

Rule: align the shapes from the **right**. Two axes are compatible if they are equal or one of them is 1; a size-1 axis (or a missing leading axis) is stretched to match.

| Left | Right | Result |
|---|---|---|
| `(n, d)` | `(d,)` | `(n, d)`: subtract a per-feature mean from every row |
| `(n, 1)` | `(1, m)` | `(n, m)`: all pairs (outer sum) |
| `(n, 1, d)` | `(1, k, d)` | `(n, k, d)`: every point minus every centre |
| `(n, d)` | `(n,)` | **error** (aligned from the right: `d` vs `n`), or silently wrong if $n=d$; use `v[:, None]` to make it `(n, 1)` |

`None` (same as `np.newaxis`) inserts a size-1 axis: `a[:, None]` turns `(n,)` into `(n, 1)`; `a[None]` turns `(k, d)` into `(1, k, d)`. `keepdims=True` keeps a reduced axis as size 1 so the result broadcasts back against the input.

## The snippets, explained

```python
import numpy as np

# Least squares (rows = samples) -> Linear Regression
w = np.linalg.lstsq(X, y, rcond=None)[0]
# Ridge
w = np.linalg.solve(X.T @ X + lam * np.eye(X.shape[1]), X.T @ y)
```
- **Least squares** solves $\min_w\lVert Xw-y\rVert^2$ via an SVD-based solver; `[0]` takes the solution from the returned tuple (solution, residuals, rank, singular values). It works even when $X^\top X$ is singular (returns the minimum-norm solution), and avoids forming an explicit inverse. Add a column of ones to `X` if you want an intercept.
- **Ridge** solves the normal equations $(X^\top X+\lambda I)w=X^\top y$ (derived in [[Matrix Calculus Cheatsheet]]). `np.linalg.solve` is faster and more accurate than `inv(...) @ ...`. Adding $\lambda I$ makes the matrix positive definite, so it is always solvable. Shapes: `X.T @ X` is `(d, d)`, `X.T @ y` is `(d,)`.

```python
# Columns = samples layout (see the lecture cheat sheet)
W = T @ X.T @ np.linalg.inv(X @ X.T)
pred = np.argmax(W @ X, axis=0)
```
- Here `X` is `(d, n)` (one sample per **column**) and `T` is `(K, n)` one-hot targets. We want $WX\approx T$; least squares gives $W=TX^\top(XX^\top)^{-1}$, shape `(K, d)`. This is the same normal equation, transposed.
- `W @ X` is `(K, n)`: one column of class scores per sample, so the predicted class is the row index of the maximum in each column: `argmax(..., axis=0)`. Getting the axis wrong is the classic bug when switching layouts.

```python
# Standardize with training statistics only
mu, sd = X_tr.mean(0), X_tr.std(0) + 1e-8
X_tr, X_te = (X_tr - mu) / sd, (X_te - mu) / sd
```
- `mean(0)` / `std(0)` reduce over axis 0 (the samples), giving one number per feature, shape `(d,)`. Broadcasting `(n, d) - (d,)` applies them to every row.
- `+ 1e-8` avoids division by zero for constant features.
- **Training statistics only**: the test set is transformed with the *training* mean and std. Computing them on all data leaks test information into training (see [[scikit-learn Recipes]] for the pipeline version).
- The right-hand side is evaluated before assigning, so using the old `X_tr` for both is safe.

```python
# Numerically stable softmax / log-sum-exp
def softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)
```
- Softmax is unchanged by subtracting a constant from each row ($\frac{e^{z_k-m}}{\sum_je^{z_j-m}}=\frac{e^{z_k}}{\sum_je^{z_j}}$). Subtracting the row max makes the largest exponent $e^0=1$: no overflow (`exp(1000) = inf`), and the denominator is at least 1.
- `keepdims=True` keeps shape `(n, 1)` so it broadcasts against `(n, K)`; without it, `(n,)` would try to align with `K` and fail or, if $n=K$, silently divide the wrong way.
- Log-sum-exp uses the same trick: $\log\sum_je^{z_j}=m+\log\sum_je^{z_j-m}$, and then cross-entropy from logits is `-z[np.arange(n), y] + lse` ([[Information Theory]]).

```python
# Sigmoid + logistic regression gradient descent
sigmoid = lambda z: 1 / (1 + np.exp(-z))
for _ in range(1000):
    p = sigmoid(X @ w)
    w -= 0.1 * X.T @ (p - y) / len(y)
```
- Initialize `w = np.zeros(X.shape[1])` first. `X @ w` gives all $n$ logits at once; `p` holds predicted probabilities, shape `(n,)`.
- The gradient of the mean binary cross-entropy is $\frac1nX^\top(p-y)$: "prediction minus target", weighted by the inputs ([[Matrix Calculus Cheatsheet]]). `X.T @ (p - y)` sums $x_i(p_i-y_i)$ over samples in one product. This is plain batch [[Gradient Descent]] with $\eta=0.1$.
- For large negative `z`, `np.exp(-z)` can overflow and warn; it still returns the right limit 0, or use `scipy.special.expit`.

```python
# PCA via SVD
Xc = X - X.mean(0)
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
Z = Xc @ Vt[:k].T
```
- PCA needs **centred** data (otherwise the first component just points at the mean).
- The rows of `Vt` are the principal directions sorted by singular value; `Vt[:k].T` is `(d, k)`, so `Z` is `(n, k)`: the coordinates of each sample along the top $k$ components. Equivalently `Z = U[:, :k] * S[:k]`.
- Explained variance of component $i$: `S**2 / (n - 1)`; the fraction is `S**2 / (S**2).sum()`. `full_matrices=False` returns the thin SVD (no huge unused `U`). See [[PCA]] and [[Linear Algebra for ML]].

```python
# Pairwise squared distances (kNN, kernels, k-means)
D2 = (A**2).sum(1)[:, None] + (B**2).sum(1)[None] - 2 * A @ B.T
K = np.exp(-gamma * D2)            # RBF kernel matrix
```
- Expansion trick: $\lVert a-b\rVert^2=\lVert a\rVert^2+\lVert b\rVert^2-2a^\top b$. With `A` `(n, d)` and `B` `(m, d)`: `(n, 1) + (1, m) - (n, m)` → `(n, m)`, the broadcasting picture above. Memory is $O(nm)$ instead of $O(nmd)$ for the naive `A[:, None] - B[None]`, and the heavy part is one fast matrix product.
- Round-off can make tiny entries slightly negative: wrap in `np.maximum(D2, 0)` before a `sqrt`.
- `K` is the Gaussian/RBF kernel $k(a,b)=e^{-\gamma\lVert a-b\rVert^2}$ ([[Kernel Methods]]). For kNN, `np.argsort(D2, axis=1)[:, :k]` gives each query's nearest neighbours.

```python
# k-means
C = X[np.random.choice(len(X), k, replace=False)]
for _ in range(100):
    a = ((X[:, None] - C[None]) ** 2).sum(-1).argmin(1)
    C = np.stack([X[a == j].mean(0) for j in range(k)])
```
- Initialization: $k$ distinct random data points as centres.
- **Assignment step**: `X[:, None]` is `(n, 1, d)`, `C[None]` is `(1, k, d)`; their difference is `(n, k, d)`, summing squares over the last axis gives `(n, k)` squared distances, and `argmin(1)` picks each point's nearest centre, shape `(n,)`.
- **Update step**: each centre moves to the mean of its points (boolean mask `a == j`). The two steps alternate until assignments stop changing ([[Clustering]]).
- **Bug to know**: if a cluster ends up empty, `X[a == j].mean(0)` is the mean of nothing: NaN plus a warning, and that centre is dead forever. Fix: keep the old centre (or reseed it with a far-away point):
  ```python
  C = np.stack([X[a == j].mean(0) if np.any(a == j) else C[j] for j in range(k)])
  ```
- The `(n, k, d)` intermediate can be large; for big data use the distance-expansion trick above.

### More idioms the exercises use
- **Views vs copies**: basic slicing (`X[:10]`, `X[:, 0]`) returns a *view* sharing memory, so writing to it changes `X`; fancy/boolean indexing (`X[[0, 2]]`, `X[X > 0]`) returns a *copy*. In-place ops (`X -= mu`) modify the original array everywhere it is referenced. Use `.copy()` when in doubt.
- **One-hot in one line**: `Y = np.eye(K)[y]` (row $y_i$ of the identity), shape `(n, K)`.
- **`einsum`** names axes explicitly: `'ij,jk->ik'` is a matrix product, `'ij,ij->i'` row-wise dot products, and Mahalanobis distances are `np.einsum('ij,jk,ik->i', D, S_inv, D)` with `D = X - mu`.
- **Moving average with `cumsum`**: `c = np.cumsum(np.insert(x, 0, 0)); ma = (c[w:] - c[:-w]) / w`, $O(n)$ for any window `w`.
- **Group-by without pandas**: `np.bincount(g, weights=v) / np.bincount(g)` gives per-group means for integer group ids `g`.

Related: [[Linear Regression]], [[Logistic Regression]], [[PCA]], [[Clustering]], [[Kernel Methods]].

## Worked example

Pairwise distances by hand. `A = [[0, 0], [1, 1]]`, `B = [[1, 0]]`.
1. Row norms: `(A**2).sum(1) = [0, 2]` → `[:, None]` gives `[[0], [2]]`; `(B**2).sum(1) = [1]` → `[None]` gives `[[1]]`.
2. `A @ B.T = [[0], [1]]`.
3. `D2 = [[0], [2]] + [[1]] - 2 * [[0], [1]] = [[1], [1]]`. Check: $\lVert(0,0)-(1,0)\rVert^2=1$ and $\lVert(1,1)-(1,0)\rVert^2=1$. ✓

Stable softmax: `z = [1000, 1001]`. Naive `exp` overflows to `inf/inf = nan`. Shifted: `[-1, 0]` → `exp = [0.368, 1]` → softmax `[0.269, 0.731]`.

## Common confusions
- **"`(n, d) - (n,)` subtracts a per-row value."** → Broadcasting aligns from the right, so `(n,)` is matched against `d`. Use `v[:, None]`.
- **"`mean()` without an axis is fine."** → It averages over *everything* and returns a scalar. Specify `axis=0` (per feature) or `axis=1` (per sample).
- **"`np.linalg.inv` is the way to solve a system."** → Use `solve` or `lstsq`: faster, more accurate, and they handle near-singular cases better.
- **"`a[mask] = 0` and `b = a[mask]; b[:] = 0` do the same thing."** → The first writes into `a`; the second modifies a copy.
- **"`X.std(0)` is the sample standard deviation."** → NumPy's default `ddof=0` divides by $n$; pandas and many textbooks use $n-1$ (`ddof=1`). It rarely matters for scaling but matters for statistics.

## Check yourself

> [!question]- What shape does `np.ones((5, 1, 3)) + np.ones((4, 1))` have?
> Align right: `(5, 1, 3)` vs `(1, 4, 1)` → `(5, 4, 3)`.

> [!question]- Why subtract the max in softmax rather than, say, the mean?
> Subtracting the max guarantees every exponent is $\le0$ (no overflow) and at least one is exactly $e^0=1$ (the denominator cannot underflow to 0). The mean guarantees neither.

> [!question]- In the k-means snippet, what are the shapes of `X[:, None] - C[None]` and of `a`?
> `(n, k, d)` and `(n,)`.

> [!question]- Why must the scaler use training statistics only?
> Test data must be treated as unseen. Using its mean/std in preprocessing leaks information and gives an optimistic test score.

> [!question]- When does `X_te -= mu` behave differently from `X_te = X_te - mu`?
> The in-place version modifies the existing array (and every view of it, e.g. if `X_te` is a slice of a bigger array) and fails for an integer array with float `mu`; the second creates a new array.

## Practice
[NumPy Snippets - Exercises](NumPy%20Snippets%20-%20Exercises.ipynb): predicting broadcast shapes, views vs copies, training-only standardization, stable softmax, pairwise distances and einsum strings by hand, then drills: indexing, one-hot, RBF/kNN, least squares in both layouts, vectorized logistic regression, PCA via SVD, k-means without the empty-cluster bug, Mahalanobis distances, moving averages and group-by.

## Learn more
- [NumPy docs](https://numpy.org/doc/stable/)
- [NumPy user guide – Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
