---
tags: [ml, supervised, kernels]
---
# Kernel Methods

> [!summary] In one sentence
> A **kernel** $k(x,x')=\langle\phi(x),\phi(x')\rangle$ computes inner products in feature space without constructing $\phi$ (the kernel trick), so any algorithm that only needs inner products can become non-linear for the price of a similarity function.

## Intuition first

Many datasets are not linearly separable in the space you measured them in: think of a ring of red points around a blue blob. No straight line separates them. But add one new feature, the squared distance from the centre $x_1^2+x_2^2$, and suddenly the blue points sit low and the red ones high: a flat plane separates them. **Linear methods in a richer feature space = non-linear methods in the original space.**

The catch: rich feature spaces are huge. All polynomial features of degree 3 of a 100×100 image already number in the millions, and the feature space of the Gaussian (RBF) kernel is infinite-dimensional. The **kernel trick** escapes this: if an algorithm only ever uses inner products $\langle\phi(x),\phi(x')\rangle$, we can replace them by a cheap function $k(x,x')$ evaluated in the *original* space and never build $\phi(x)$ at all.

A second, very practical way to think about it: a kernel is a **similarity measure**. Kernel methods predict with "a weighted sum of similarities to the training points", $f(x)=\sum_i\alpha_ik(x_i,x)$. With an RBF kernel, each training point contributes a little bump, and the model is the sum of bumps.

![Ring data lifted into 3D with phi(x) = (x1, x2, x1² + x2²), separated by a plane](../../Attachments/ML%20Animations/Kernel%20Methods%20-%20lifting%20to%203D.gif)
*Watch the 2D rings rise onto a paraboloid: the inner (blue) points stay low, the outer (orange) ones climb, a flat plane slips between them, and dropping back to 2D turns that plane into a circular boundary.*

## The math, step by step

### Feature maps and the kernel trick
A feature map $\phi:\mathcal X\to\mathcal H$ sends an input to a (possibly very high-dimensional) vector. A kernel is the inner product there: $k(x,x')=\langle\phi(x),\phi(x')\rangle$.

**Example (polynomial, degree 2, in 2D).** For $x,z\in\mathbb R^2$,
$$(x^\top z+1)^2=x_1^2z_1^2+x_2^2z_2^2+2x_1x_2z_1z_2+2x_1z_1+2x_2z_2+1=\phi(x)^\top\phi(z),$$
with $\phi(x)=(x_1^2,\ x_2^2,\ \sqrt2x_1x_2,\ \sqrt2x_1,\ \sqrt2x_2,\ 1)$. Computing $k$ costs one 2D dot product and a square; computing $\phi$ explicitly costs 6 coordinates, and in general the kernel $(x^\top z+c)^p$ corresponds to all $\binom{n+p}{p}$ monomials of degree $\le p$ in $n$ variables (for $n=2,p=2$: $\binom42=6$, matching $\phi$ above). That number explodes with $n$ and $p$, while the kernel stays $O(n)$.

### Which functions are valid kernels? (Mercer)
**Mercer**: $k$ is valid iff the Gram matrix $K_{ij}=k(x_i,x_j)$ is PSD for any data ([[Linear Algebra for ML]]).

In words: for every finite set of points and every vector $c$, $c^\top Kc=\lVert\sum_ic_i\phi(x_i)\rVert^2\ge0$. A symmetric matrix with a negative eigenvalue (or a negative diagonal entry, or $|K_{12}|>\sqrt{K_{11}K_{22}}$) cannot come from inner products. The popular "sigmoid kernel" $\tanh(a\,x^\top z+c)$ is *not* PSD in general.

### The standard kernels

| Kernel | Formula |
|---|---|
| Linear | $x^\top x'$ |
| Polynomial | $(x^\top x'+c)^d$ |
| RBF / Gaussian | $\exp(-\gamma\lVert x-x'\rVert^2)$ (infinite-dim $\phi$) |
| Laplacian | $\exp(-\gamma\lVert x-x'\rVert_1)$ |
| Graph / string / tree kernels | structured data, see [[Graph ML Overview]] |

Reading them:
- **Linear**: plain dot product, $\phi(x)=x$; recovers the original linear method.
- **Polynomial**: all feature interactions up to degree $d$; $c\ge0$ trades off lower- vs higher-order terms.
- **RBF**: $k(x,x)=1$ and $k\to0$ as points move apart, so it is a similarity that decays with distance. $\gamma=1/(2\ell^2)$ sets the length scale $\ell$: large $\gamma$ = very local, wiggly models (every point is its own island); small $\gamma$ = smooth, nearly linear models. Its feature space is infinite-dimensional (expand the exponential as a power series).
- **Laplacian**: like RBF but with the L1 distance and no square: sharper peak, rougher functions.
- **Structured kernels**: count shared substrings, subtrees, or random-walk patterns, so you can run an SVM on strings, trees or graphs without turning them into fixed-length vectors first.

### Building new kernels
Closure: sums, products, positive scalings of kernels are kernels.
- $a\,k_1$ ($a>0$): feature map $\sqrt a\,\phi_1$.
- $k_1+k_2$: concatenate the feature maps $(\phi_1,\phi_2)$.
- $k_1k_2$: all pairwise products of features (the tensor product $\phi_1\otimes\phi_2$); Gram-wise, the elementwise (Schur) product of PSD matrices is PSD.

These rules let you combine kernels for different feature types, e.g. RBF on numeric columns + a string kernel on text.

### Geometry for free
Distances in feature space also only need kernels:
$$\lVert\phi(x)-\phi(z)\rVert^2=k(x,x)+k(z,z)-2k(x,z).$$
For RBF this is $2-2k(x,z)$, between 0 and 2.

## Kernelized algorithms
[[Support Vector Machines]], kernel ridge regression, kernel [[PCA]], [[Gaussian Processes]], kernel k-means.

**Why these work (representer theorem, informally).** If you minimise a loss on the training points plus an L2 penalty $\lambda\lVert w\rVert^2$ in feature space, the optimal $w$ lies in the span of the training features: $w=\sum_i\alpha_i\phi(x_i)$. Any component orthogonal to all $\phi(x_i)$ does not change the predictions on the data but increases the penalty. So predictions are $f(x)=\sum_i\alpha_ik(x_i,x)$ and you only need to learn $N$ numbers $\alpha$.

**Kernel ridge regression.** Ridge in feature space, with $\Phi$ the $N\times D$ matrix of features:
$$w=(\Phi^\top\Phi+\lambda I)^{-1}\Phi^\top y=\Phi^\top(\Phi\Phi^\top+\lambda I)^{-1}y=\Phi^\top\alpha,\qquad \alpha=(K+\lambda I)^{-1}y,$$
using the push-through identity and $K=\Phi\Phi^\top$. The prediction is $f(x)=\sum_i\alpha_ik(x_i,x)$. Its formula is exactly the [[Gaussian Processes|GP posterior mean]] with $\lambda=\sigma^2$.

![Kernel ridge regression as a sum of weighted RBF bumps, with gamma changing](../../Attachments/ML%20Animations/Kernel%20Methods%20-%20sum%20of%20kernel%20bumps.gif)
*Watch each coloured bump $\alpha_ik(x_i,\cdot)$ appear at its data point and add up to the yellow fit; then large $\gamma$ makes narrow spikes (overfitting) and small $\gamma$ makes broad, smooth bumps.*

**Kernel PCA.** Do [[PCA]] in feature space: centre the Gram matrix ($\tilde K=K-\mathbf 1K-K\mathbf 1+\mathbf 1K\mathbf 1$ with $\mathbf 1=\frac1N\mathbf 1\mathbf 1^\top$, since we cannot subtract the feature-space mean directly), eigendecompose it, and project with the top eigenvectors. With an RBF kernel it can "unroll" concentric circles that linear PCA cannot.

**Kernel k-means** clusters using feature-space distances from the formula above, so clusters can be non-convex.

## Scaling
Scaling: $O(N^2)$ memory, $O(N^3)$ solve; use Nyström or random Fourier features.

The Gram matrix has $N^2$ entries (at $N=10^5$, float64: $8\times10^{10}$ bytes = 80 GB) and solving with $K+\lambda I$ costs $O(N^3)$. Two classic escapes, both turning the kernel back into an explicit, *finite* feature map so you can use fast linear methods:
- **Nyström**: pick $m\ll N$ landmark points, compute $C=K(X,\text{landmarks})$ ($N\times m$) and $W=K(\text{landmarks},\text{landmarks})$, and approximate $K\approx CW^{+}C^\top$, a rank-$m$ approximation. Data-dependent: good when the spectrum decays fast; quality depends on landmark choice.
- **Random Fourier features** (Rahimi & Recht): for shift-invariant kernels, Bochner's theorem writes $k$ as an expectation over random frequencies. For RBF, $z(x)=\sqrt{2/D}\cos(Wx+b)$ with rows of $W\sim\mathcal N(0,2\gamma I)$ and $b\sim U[0,2\pi]$ gives $k(x,x')\approx z(x)^\top z(x')$. Data-independent and trivially parallel, but needs many features $D$ for high accuracy.

## Worked example

**Polynomial kernel both ways.** $x=(1,1)$, $z=(2,0)$, $k(x,z)=(x^\top z+1)^2$.
- Kernel: $x^\top z=2$, so $k=(2+1)^2=9$.
- Feature map: $\phi(x)=(1,1,\sqrt2,\sqrt2,\sqrt2,1)$, $\phi(z)=(4,0,0,2\sqrt2,0,1)$, dot product $4+0+0+4+0+1=9$. ✓

**RBF in feature space.** $x=(0,0)$, $z=(1,1)$, $\gamma=0.5$: $\lVert x-z\rVert^2=2$, $k=e^{-1}\approx0.368$; feature-space squared distance $2-2(0.368)=1.264$.

**Not a kernel.** A "kernel" produces the Gram matrix $\begin{pmatrix}1&3\\3&1\end{pmatrix}$ on two points. Its eigenvalues are $4$ and $-2$; the negative one means it is not PSD, so no feature map can produce it (also $|K_{12}|=3>\sqrt{K_{11}K_{22}}=1$ violates Cauchy–Schwarz).

## Common confusions
- *"The kernel trick means computing $\phi$ efficiently."* → It means *never* computing $\phi$; only $k$ is evaluated.
- *"Any similarity function is a kernel."* → It must be symmetric and give PSD Gram matrices; otherwise SVM/GP optimisation can break (non-convex, negative variances).
- *"A bigger feature space means more overfitting, so RBF must overfit."* → Regularisation (the $\lVert w\rVert^2$ penalty, $C$, $\lambda$) and the length scale control complexity, not the dimension of $\phi$.
- *"Kernels are only for SVMs."* → Any method expressible with inner products can be kernelised: ridge regression, PCA, k-means, GPs, even the perceptron.
- *"Kernel methods scale like linear models."* → Exact ones scale like $O(N^2)$ memory and $O(N^3)$ time; that is why approximations exist.

## Check yourself

> [!question]- What are $k(x,x)$ and $\lim_{\lVert x-x'\rVert\to\infty}k(x,x')$ for the RBF kernel?
> $k(x,x)=1$ (every $\phi(x)$ has unit norm) and the limit is $0$ (far-apart points are orthogonal in feature space).

> [!question]- If $k_1$ and $k_2$ are kernels, is $k_1-k_2$ a kernel?
> Not in general: differences can produce negative eigenvalues (take $k_2=2k_1$). Only sums, products and positive scalings are guaranteed.

> [!question]- What does the representer theorem buy you computationally?
> The solution is $f(x)=\sum_i\alpha_ik(x_i,x)$, so you optimise $N$ coefficients instead of a (possibly infinite) weight vector.

> [!question]- Why must the Gram matrix be centred in kernel PCA?
> PCA needs centred data, but we cannot subtract the mean of the $\phi(x_i)$ explicitly; centring $K$ is the kernel-space equivalent of subtracting the feature-space mean.

> [!question]- How many monomials of degree $\le2$ are there in 3 variables?
> $\binom{3+2}{2}=10$: one constant, three linear, three squares, three cross terms.

## Practice
[Kernel Methods - Exercises](Kernel%20Methods%20-%20Exercises.ipynb): the kernel trick in a paragraph, what RBF measures, which algorithms can be kernelised, kernels at scale; by hand: an explicit feature map, the size of polynomial feature space, evaluating kernels and feature-space distances, valid or not, closure proofs, kernel ridge in dual form; in code: Gram matrices, checking Mercer numerically, kernel ridge regression, kernel PCA, random Fourier features, Nyström.

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 6
- [Elements of Statistical Learning (free)](https://hastie.su.domains/ElemStatLearn/) ch. 5–6
- [scikit-learn – kernel approximation](https://scikit-learn.org/stable/modules/kernel_approximation.html): Nyström and random Fourier features (`RBFSampler`) in practice
- [scikit-learn – kernel ridge regression](https://scikit-learn.org/stable/modules/kernel_ridge.html)
