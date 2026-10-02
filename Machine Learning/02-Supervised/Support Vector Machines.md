---
tags: [ml, supervised, svm]
---
# Support Vector Machines

> [!summary] In one sentence
> Find the hyperplane with **maximum margin** $2/\lVert w\rVert$: among all lines that separate the two classes, an SVM picks the one with the widest empty "street" around it, and the result depends only on the few points touching the street (the support vectors).

## Intuition first

Picture two groups of houses on a map and you must build a straight road between them. Many roads would avoid every house, but the sensible one is the **widest road** you can build, running down the middle of the gap. Why? If new houses appear (new data), they are likely near the old ones, and a wide safety margin means they still end up on the correct side. A road that scrapes past a house is fragile.

Two more observations make SVMs special:
- The road's position is determined only by the houses **touching its edges**: the *support vectors*. Move or delete any other house and nothing changes. The solution is *sparse*.
- When no straight road exists (classes overlap), we allow a few houses to sit inside or across the road but **charge a penalty** $C$ for each violation (the *soft margin*).
- When the boundary should be curved, we never build a curved road: we **lift the data into a richer feature space** where a straight road works, and the *kernel trick* lets us do this without ever computing the lifted coordinates ([[Kernel Methods]]).

**What problem does it solve?** It is a linear classifier with a principled choice among the infinitely many separating hyperplanes (the [[Linear Models for Classification|perceptron]] just stops at the first one it finds), with strong generalisation guarantees, and, through kernels, a flexible non-linear classifier that was the state of the art before deep learning on small/medium datasets.

![A separating line rotating until its margin is maximal, support vectors circled](../../Attachments/ML%20Animations/Support%20Vector%20Machines%20-%20maximum%20margin.gif)
*Watch the margin number grow as the yellow boundary rotates: it stops when the street touches three points (circled, the support vectors). Moving a far-away point afterwards leaves the boundary untouched.*

## The math, step by step

### Geometry of a hyperplane
A linear classifier predicts $\operatorname{sign}(f(x))$ with $f(x)=w^\top x+b$. Here $w\in\mathbb R^d$ is the normal vector (perpendicular to the boundary) and $b$ shifts it.
- The signed distance from a point $x$ to the hyperplane $w^\top x+b=0$ is $\dfrac{w^\top x+b}{\lVert w\rVert}$.
- For a labelled point $(x_i,y_i)$ with $y_i\in\{-1,+1\}$, the **functional margin** is $y_i(w^\top x_i+b)$ (positive iff correctly classified) and the **geometric margin** is $y_i(w^\top x_i+b)/\lVert w\rVert$ (the actual distance).

Scaling $w,b$ by any constant does not move the hyperplane, so we fix the scale ("canonical form") by demanding that the closest points have functional margin exactly 1: $\min_iy_i(w^\top x_i+b)=1$. Then the closest points on each side lie on $w^\top x+b=\pm1$, each at distance $1/\lVert w\rVert$, and the street is $2/\lVert w\rVert$ wide.

### Hard margin
Maximising $2/\lVert w\rVert$ is the same as minimising $\lVert w\rVert$, or the smoother $\frac12\lVert w\rVert^2$:

$\min\frac12\lVert w\rVert^2$ s.t. $y_i(w^\top x_i+b)\ge1$.

In words: the smallest-norm $w$ (widest street) such that every point is on the correct side and outside the street. This is a convex quadratic program with a unique solution, and it only exists if the data are linearly separable.

### Soft margin
Introduce a **slack** $\xi_i\ge0$ per point: how far it is allowed to violate the margin.

$$\min\ \tfrac12\lVert w\rVert^2+C\sum_i\xi_i,\quad y_i(w^\top x_i+b)\ge1-\xi_i$$

- $\xi_i=0$: on or outside the margin, correct side.
- $0<\xi_i\le1$: inside the street but still correctly classified.
- $\xi_i>1$: misclassified.

At the optimum each slack is as small as allowed: $\xi_i=\max(0,1-y_if(x_i))$. Substituting gives the unconstrained form

$$\min_{w,b}\ \tfrac12\lVert w\rVert^2+C\sum_i\max\big(0,1-y_i(w^\top x_i+b)\big).$$

Equivalent to hinge loss $\max(0,1-y f(x))$ + L2. Dividing by $CN$ shows it is "average hinge loss + $\lambda\lVert w\rVert^2$" with $\lambda=\frac1{2CN}$, i.e. regularised empirical risk minimisation like [[Logistic Regression]], only with a different loss. Large $C$ → low bias; small $C$ → wide margin.
- **Large $C$**: violations are expensive, so the street narrows to classify every training point: low bias, high variance (approaches the hard margin).
- **Small $C$**: violations are cheap, the street widens and many points become support vectors: higher bias, lower variance.

### Dual
Using Lagrange multipliers $\alpha_i\ge0$ for the margin constraints (and $\mu_i\ge0$ for $\xi_i\ge0$) and setting the derivatives of the Lagrangian to zero gives
- $\partial/\partial w$: $w=\sum_i\alpha_iy_ix_i$ (the weight vector is a combination of training points),
- $\partial/\partial b$: $\sum_i\alpha_iy_i=0$,
- $\partial/\partial\xi_i$: $C-\alpha_i-\mu_i=0$, hence $0\le\alpha_i\le C$.

Substituting back eliminates $w,b,\xi$:

$$\max_\alpha\sum\alpha_i-\tfrac12\sum\alpha_i\alpha_jy_iy_jx_i^\top x_j,\quad 0\le\alpha_i\le C$$

(together with $\sum_i\alpha_iy_i=0$). Predictions become $f(x)=\sum_i\alpha_iy_i\,x_i^\top x+b$.

Only **support vectors** have $\alpha_i>0$. Data enters only via dot products ⇒ replace by a kernel ([[Kernel Methods]]). Derived with KKT ([[Calculus and Optimization]]).

**Reading the KKT conditions** (complementary slackness) tells you where each point sits:
- $\alpha_i=0$ ⇒ $y_if(x_i)\ge1$: outside the street; irrelevant to the solution.
- $0<\alpha_i<C$ ⇒ $y_if(x_i)=1$: exactly on the margin (use these to compute $b=y_i-w^\top x_i$).
- $\alpha_i=C$ ⇒ $y_if(x_i)\le1$: inside the street or misclassified.

**Primal or dual?** The primal has $d+1$ variables, the dual $N$. With many points and few features (and a linear kernel), solve the primal (e.g. `LinearSVC`, subgradient descent on the hinge objective). The dual is needed for kernels, but it touches the $N\times N$ Gram matrix: $O(N^2)$ memory and roughly $O(N^2)$–$O(N^3)$ time.

## Worked example

**A two-point hard-margin SVM.** $x_+=(3,4)$ with $y=+1$, $x_-=(0,0)$ with $y=-1$. By symmetry $w$ points from $x_-$ to $x_+$: $w=c\,(3,4)$. Both points are support vectors, so
- $w^\top x_-+b=-1\Rightarrow b=-1$,
- $w^\top x_++b=1\Rightarrow 25c-1=1\Rightarrow c=0.08$, so $w=(0.24,0.32)$, $\lVert w\rVert=0.4$.

Margin $2/\lVert w\rVert=5$, exactly the distance between the two points, and the boundary $0.24x_1+0.32x_2=1$ is their perpendicular bisector (it passes through the midpoint $(1.5,2)$). Dual check: $w=\alpha(x_+-x_-)$ gives $\alpha=0.08$ for both points, and $\sum\alpha_iy_i=0$.

**Hinge losses.** Three points with scores $f(x)$: $(y=+1,f=1.5)\to\max(0,1-1.5)=0$ (safe); $(y=+1,f=0.3)\to0.7$ (inside the street, correct side); $(y=-1,f=0.2)\to\max(0,1+0.2)=1.2$ (wrong side, $\xi>1$).

## Kernels & hyperparameters
RBF $k(x,x')=\exp(-\gamma\lVert x-x'\rVert^2)$: tune $C$ and $\gamma$ on a log grid; scale features first.

With a kernel the decision function is $f(x)=\sum_{i\in SV}\alpha_iy_ik(x_i,x)+b$: a weighted sum of similarities to the support vectors (scikit-learn stores $\alpha_iy_i$ in `dual_coef_`). For the RBF kernel:
- $\gamma$ is an inverse length scale. **Large $\gamma$**: each support vector influences only a tiny neighbourhood, so boundaries become islands around points (overfitting). **Small $\gamma$**: very smooth, almost linear boundaries (underfitting).
- $C$ and $\gamma$ interact, so search them jointly over powers of 10 (e.g. $C\in\{10^{-2},\dots,10^3\}$, $\gamma\in\{10^{-2},\dots,10^2\}$) with [[Cross-Validation and Model Selection|cross-validation]].
- **Scale features first** ([[Data Preprocessing]]): the kernel depends on distances, so a feature in large units dominates; put the scaler inside a pipeline so it is fitted only on training folds.

![Two rings lifted into 3D by x1²+x2², split by a plane, giving a circle back in 2D](../../Attachments/ML%20Animations/Kernel%20Methods%20-%20lifting%20to%203D.gif)
*The kernel idea behind non-linear SVMs: watch the rings become separable by a flat plane after lifting, and the plane turn into a circular boundary when projected back.*

Also: SVR (ε-insensitive regression), one-class SVM ([[Anomaly Detection]]).
- **SVR** fits a tube of half-width $\varepsilon$ around the regression function and ignores errors inside it, using the loss $\max(0,|y-f(x)|-\varepsilon)$; points outside the tube become support vectors. Larger $\varepsilon$ → fewer support vectors and a flatter fit.
- **One-class SVM** separates the data from the origin in feature space with maximum margin, so it learns a boundary around "normal" data; points outside are anomalies.

## Common confusions
- *"SVMs output probabilities."* → They output a score $f(x)$; probabilities need an extra calibration step (Platt scaling, `probability=True`), unlike [[Logistic Regression]].
- *"Large $C$ means more regularisation."* → The opposite: $C$ multiplies the data-fit term, so large $C$ = *less* regularisation (narrow margin).
- *"All training points shape the boundary."* → Only support vectors ($\alpha_i>0$) do; hinge loss is exactly zero for points beyond the margin. (Logistic loss is never exactly zero, so every point has some influence there.)
- *"The kernel trick makes SVMs scale to big data."* → Kernel SVMs need the $N\times N$ Gram matrix and are slow beyond ~$10^5$ points; use a linear SVM or kernel approximations instead.
- *"The margin is $1/\lVert w\rVert$."* → That is the distance from the boundary to *one* side; the full street is $2/\lVert w\rVert$.

## Check yourself

> [!question]- A canonical hyperplane has $w=(6,8)$. How wide is the margin?
> $\lVert w\rVert=10$, so $2/\lVert w\rVert=0.2$.

> [!question]- In the dual solution, a point has $\alpha_i=C$. What can you say about it?
> It is a support vector with $y_if(x_i)\le1$: inside the margin or misclassified (its slack is positive unless it lies exactly on the margin).

> [!question]- Why can only the dual use the kernel trick?
> In the dual, training and prediction touch the data only through inner products $x_i^\top x_j$ and $x_i^\top x$, which can be replaced by $k(x_i,x_j)$. The primal works with $w$ explicitly, which would live in the (possibly infinite-dimensional) feature space.

> [!question]- What happens to the number of support vectors as $C$ decreases?
> It grows: the margin widens, so more points fall inside it and get $\alpha_i>0$.

> [!question]- An RBF SVM has 100% training accuracy and poor test accuracy. Which way should you move $\gamma$ and $C$?
> Decrease $\gamma$ (smoother kernel) and/or decrease $C$ (more regularisation), chosen by cross-validation on a log grid.

## Practice
[Support Vector Machines - Exercises](Support%20Vector%20Machines%20-%20Exercises.ipynb): why the maximum margin, reading $C$ and $\gamma$, SVM vs logistic regression, primal vs dual; by hand: margins and distances, a two-point hard margin, hinge loss, soft margin = hinge + L2, deriving the dual, reading KKT conditions, recovering $w$ and $b$; in code: primal subgradient descent, solving the dual QP, kernel predictions by hand, tuning $C$ and $\gamma$, support vectors vs $C$, SVR's ε-tube.

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 9
- [scikit-learn – SVMs](https://scikit-learn.org/stable/modules/svm.html)
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 7
- [Stanford CS229 lecture notes](https://cs229.stanford.edu/): the SVM notes derive the margin, the dual and SMO carefully
- [StatQuest videos](https://statquest.org/video_index.html): "Support Vector Machines" main ideas and the polynomial/RBF kernel episodes
