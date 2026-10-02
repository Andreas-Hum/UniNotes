---
tags: [ml, supervised, kernels]
---
# Kernel Methods

A **kernel** $k(x,x')=\langle\phi(x),\phi(x')\rangle$ computes inner products in feature space without constructing $\phi$ (the kernel trick).

**Mercer**: $k$ is valid iff the Gram matrix $K_{ij}=k(x_i,x_j)$ is PSD for any data ([[Linear Algebra for ML]]).

| Kernel | Formula |
|---|---|
| Linear | $x^\top x'$ |
| Polynomial | $(x^\top x'+c)^d$ |
| RBF / Gaussian | $\exp(-\gamma\lVert x-x'\rVert^2)$ (infinite-dim $\phi$) |
| Laplacian | $\exp(-\gamma\lVert x-x'\rVert_1)$ |
| Graph / string / tree kernels | structured data, see [[Graph ML Overview]] |

Closure: sums, products, positive scalings of kernels are kernels.

## Kernelized algorithms
[[Support Vector Machines]], kernel ridge regression, kernel [[PCA]], [[Gaussian Processes]], kernel k-means.

Scaling: $O(N^2)$ memory, $O(N^3)$ solve; use Nyström or random Fourier features.
