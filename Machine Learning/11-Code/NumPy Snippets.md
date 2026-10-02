---
tags: [ml, code, numpy]
---
# NumPy Snippets

```python
import numpy as np

# Least squares (rows = samples) -> Linear Regression
w = np.linalg.lstsq(X, y, rcond=None)[0]
# Ridge
w = np.linalg.solve(X.T @ X + lam * np.eye(X.shape[1]), X.T @ y)

# Columns = samples layout (see the lecture cheat sheet)
W = T @ X.T @ np.linalg.inv(X @ X.T)
pred = np.argmax(W @ X, axis=0)

# Standardize with training statistics only
mu, sd = X_tr.mean(0), X_tr.std(0) + 1e-8
X_tr, X_te = (X_tr - mu) / sd, (X_te - mu) / sd

# Numerically stable softmax / log-sum-exp
def softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)

# Sigmoid + logistic regression gradient descent
sigmoid = lambda z: 1 / (1 + np.exp(-z))
for _ in range(1000):
    p = sigmoid(X @ w)
    w -= 0.1 * X.T @ (p - y) / len(y)

# PCA via SVD
Xc = X - X.mean(0)
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
Z = Xc @ Vt[:k].T

# Pairwise squared distances (kNN, kernels, k-means)
D2 = (A**2).sum(1)[:, None] + (B**2).sum(1)[None] - 2 * A @ B.T
K = np.exp(-gamma * D2)            # RBF kernel matrix

# k-means
C = X[np.random.choice(len(X), k, replace=False)]
for _ in range(100):
    a = ((X[:, None] - C[None]) ** 2).sum(-1).argmin(1)
    C = np.stack([X[a == j].mean(0) for j in range(k)])
```

Related: [[Linear Regression]], [[Logistic Regression]], [[PCA]], [[Clustering]], [[Kernel Methods]].
