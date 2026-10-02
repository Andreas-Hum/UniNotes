---
tags: [ml, math, cheatsheet]
---
# Matrix Calculus Cheatsheet

> [!summary] In one sentence
> Matrix calculus is ordinary differentiation done for many variables at once: the gradient of a scalar loss with respect to a vector or matrix has the same shape as that vector or matrix, a handful of identities cover almost every ML model, and the vector chain rule (multiply by transposed Jacobians, right to left) *is* backpropagation.

## Intuition first

In 1D you know $\frac{d}{dx}(ax)=a$ and $\frac{d}{dx}x^2=2x$. Matrix calculus is the same idea when $x$ is a vector of a million weights: the gradient $\nabla_xf$ collects all the partial derivatives $\partial f/\partial x_i$ into one vector, so a single expression like $2A^\top(Ax-b)$ replaces a million separate derivatives. The table below is the vector version of the 1D rules: $a^\top x$ is like $ax$, $x^\top Ax$ is like $ax^2$, $\lVert Ax-b\rVert^2$ is like $(ax-b)^2$ whose derivative is $2a(ax-b)$.

Two habits make it painless:
1. **Shape check everything.** The gradient of a scalar with respect to an $m\times n$ matrix is $m\times n$. If your formula's shapes do not chain, it is wrong; this catches most bugs before you run anything.
2. **Use differentials.** Write the small change $df$ caused by a small change $dx$; whatever multiplies $dx$ (after rearranging into $df=g^\top dx$) is the gradient $g$.

**What problem does it solve?** Every gradient-based model needs $\nabla L$ with respect to its parameters. These identities give closed forms (e.g. the normal equations of [[Linear Regression]]) and the chain rule organizes the computation for deep networks ([[Backpropagation]]).

## The math, step by step

Denominator layout, gradients as column vectors.

That means: for scalar $f$ and $x\in\mathbb R^n$, $\nabla_xf\in\mathbb R^n$ has entries $\partial f/\partial x_i$, the same shape as $x$; for a matrix $X$, $(\nabla_Xf)_{ij}=\partial f/\partial X_{ij}$, the same shape as $X$. The defining property: $df=(\nabla_xf)^\top dx$, or $df=\mathrm{tr}\big((\nabla_Xf)^\top dX\big)$ for matrices. (Numerator layout, used in some textbooks, transposes everything; always check which one a source uses.)

| $f(x)$ | $\nabla_x f$ |
|---|---|
| $a^\top x$ | $a$ |
| $x^\top A x$ | $(A+A^\top)x$ ($=2Ax$ if symmetric) |
| $\lVert x\rVert^2$ | $2x$ |
| $\lVert Ax-b\rVert^2$ | $2A^\top(Ax-b)$ |
| $\ln\lvert A\rvert$ w.r.t. $A$ | $A^{-\top}$ |
| $\mathrm{tr}(AX)$ w.r.t. $X$ | $A^\top$ |

Where each one comes from (differential method):
- $a^\top x$: $d(a^\top x)=a^\top dx$, so the gradient is $a$. Linear in $x$ → constant gradient.
- $x^\top Ax$: $d(x^\top Ax)=dx^\top Ax+x^\top A\,dx=x^\top(A^\top+A)dx$ (a scalar equals its transpose). Gradient $(A+A^\top)x$; for symmetric $A$ that is $2Ax$, the vector version of $\frac d{dx}ax^2=2ax$.
- $\lVert x\rVert^2=x^\top Ix$: special case with $A=I$, giving $2x$.
- $\lVert Ax-b\rVert^2$: let $r=Ax-b$, then $d(r^\top r)=2r^\top dr=2r^\top A\,dx$, so the gradient is $2A^\top(Ax-b)$. Setting it to zero gives the normal equations $A^\top Ax=A^\top b$ (least squares, [[Linear Algebra for ML]]).
- $\ln|A|$: $d\ln|A|=\mathrm{tr}(A^{-1}dA)$ (Jacobi's formula), and $\mathrm{tr}(A^{-1}dA)=\mathrm{tr}\big((A^{-\top})^\top dA\big)$, so the gradient is $A^{-\top}=(A^{-1})^\top$; for symmetric $A$ (a covariance) it is $A^{-1}$.
- $\mathrm{tr}(AX)$: $d\,\mathrm{tr}(AX)=\mathrm{tr}(A\,dX)=\mathrm{tr}\big((A^\top)^\top dX\big)$, so the gradient is $A^\top$. Check shapes: if $X$ is $n\times m$ then $A$ is $m\times n$ and $A^\top$ is $n\times m$, the shape of $X$. ✓

## Chain rule (vector)

![Forward pass computes values; backward pass multiplies by Jacobian-transposes](../../Attachments/ML%20Animations/Matrix%20Calculus%20Cheatsheet%20-%20backprop%20as%20chained%20Jacobian-transposes.gif)
*Watch the yellow arrows go forward, caching $x$, $z$ and $a$; then the red arrows carry the gradient backwards, each one multiplying by a local Jacobian-transpose ($\sigma'(z)\odot$, then $W^\top$), and $\partial L/\partial W=\delta x^\top$ comes out with exactly the shape of $W$.*

If $z=g(y),\ y=h(x)$: $\nabla_x z = J_h(x)^\top\,\nabla_y z$. This is [[Backpropagation]].

- The **Jacobian** of $h:\mathbb R^n\to\mathbb R^m$ is the $m\times n$ matrix $J_{ij}=\partial y_i/\partial x_j$. It describes how a small change $dx$ moves the output: $dy=J\,dx$.
- Derivation: $dz=(\nabla_yz)^\top dy=(\nabla_yz)^\top J\,dx=(J^\top\nabla_yz)^\top dx$, so $\nabla_xz=J^\top\nabla_yz$. Shapes: $(n\times m)(m\times1)=n\times1$. ✓
- For a chain $x\to y_1\to\dots\to y_k\to L$ the gradient is $J_1^\top J_2^\top\cdots J_k^\top\nabla_{y_k}L$.
- **Why backprop runs backwards**: the loss is a scalar, so start from the right with a *vector* and do vector–Jacobian products, each about as cheap as a forward step. Going left to right would multiply full Jacobian *matrices* (one pass per input dimension). Reverse mode costs about one extra forward pass, no matter how many parameters there are.
- **One dense layer** $z=Wx+b$, $a=\sigma(z)$, with upstream gradient $\partial L/\partial a$:
  - $\delta=\partial L/\partial z=\sigma'(z)\odot\partial L/\partial a$ (element-wise because $\sigma$ acts element-wise, so its Jacobian is diagonal),
  - $\partial L/\partial W=\delta x^\top$ ($k\times d$, same as $W$), $\partial L/\partial b=\delta$,
  - $\partial L/\partial x=W^\top\delta$ (passed on to the previous layer).
  - With a batch in rows ($X$ is $n\times d$, $Z=XW^\top+b$): $\partial L/\partial W=\Delta^\top X$, $\partial L/\partial X=\Delta W$, $\partial L/\partial b=$ column sums of $\Delta$.

## Common derivatives
- Sigmoid $\sigma'(z)=\sigma(z)(1-\sigma(z))$. Derivation: $\sigma=(1+e^{-z})^{-1}$, so $\sigma'=\frac{e^{-z}}{(1+e^{-z})^2}=\sigma\cdot\frac{e^{-z}}{1+e^{-z}}=\sigma(1-\sigma)$. Max $\frac14$ at $z=0$; tiny for large $|z|$ (saturation → vanishing gradients).
- Softmax + cross-entropy: $\partial L/\partial z = \hat p - y$. Derivation: $\hat p_k=e^{z_k}/\sum_je^{z_j}$ has $\partial\hat p_k/\partial z_j=\hat p_k(\mathbb 1[k=j]-\hat p_j)$; with $L=-\sum_ky_k\log\hat p_k$ and $\sum_ky_k=1$, $\partial L/\partial z_j=-\sum_ky_k(\mathbb 1[k=j]-\hat p_j)=\hat p_j-y_j$. "Prediction minus target": the same form as linear regression's residual. For a batch with mean loss: $(\hat P-Y)/n$.
- $\tanh' = 1-\tanh^2$ (max 1 at 0), ReLU$'=\mathbb 1[z>0]$ (exactly 0 or 1, so no saturation for positive inputs; take 0 at $z=0$).

Used in [[Linear Regression]], [[Logistic Regression]], [[Neural Networks]].

### Two closed forms you can now derive
- **Ridge regression**: $\nabla_w\big(\lVert Xw-y\rVert^2+\lambda\lVert w\rVert^2\big)=2X^\top(Xw-y)+2\lambda w=0\Rightarrow w=(X^\top X+\lambda I)^{-1}X^\top y$.
- **Gaussian MLE**: maximizing $\sum_i\log\mathcal N(x_i\mid\mu,\Sigma)$ with the $\ln|A|$ and trace rules gives $\hat\mu=\frac1n\sum x_i$ and $\hat\Sigma=\frac1n\sum(x_i-\hat\mu)(x_i-\hat\mu)^\top$.

## Worked example

**Quadratic form.** $A=\begin{bmatrix}1&2\\0&3\end{bmatrix}$, $x=(1,1)$. Table: $(A+A^\top)x=\begin{bmatrix}2&2\\2&6\end{bmatrix}\begin{bmatrix}1\\1\end{bmatrix}=(4,8)$. Check by hand: $f=x_1^2+2x_1x_2+3x_2^2$, $\partial_1f=2x_1+2x_2=4$, $\partial_2f=2x_1+6x_2=8$. ✓ (Note $2Ax=(6,6)$ would be wrong: $A$ is not symmetric.)

**Softmax + cross-entropy.** Logits $z=(2,1,0)$, true class 2 ($y=(0,1,0)$).
1. $e^z=(7.39,2.72,1)$, sum $11.11$, so $\hat p\approx(0.665,0.245,0.090)$.
2. $\partial L/\partial z=\hat p-y\approx(0.665,-0.755,0.090)$: push the true logit up, the others down, in proportion to how much probability they stole.

**Numerical check.** Always verify with centred differences: $\frac{f(x+he_i)-f(x-he_i)}{2h}$, $h\approx10^{-5}$, in float64. Relative error $\lVert g_{\text{num}}-g\rVert/(\lVert g_{\text{num}}\rVert+\lVert g\rVert)$ around $10^{-7}$ means correct.

## Common confusions
- **"$\nabla(x^\top Ax)=2Ax$ always."** → Only for symmetric $A$; in general $(A+A^\top)x$.
- **"Gradient and Jacobian are the same shape."** → For scalar $f$, the gradient (denominator layout) is a column $n\times1$; the Jacobian of $f$ is the row $1\times n$. That transpose is exactly the $J^\top$ in the chain rule.
- **"The chain rule multiplies Jacobians left to right."** → For $\nabla_x$ in denominator layout it is $J^\top$ times the upstream gradient; computing right to left (from the loss) is what makes backprop cheap.
- **"Element-wise activations need full Jacobian matrices."** → Their Jacobians are diagonal, so the product is an element-wise multiplication $\sigma'(z)\odot\cdot$.
- **"$\partial L/\partial W=x\delta^\top$."** → Shape-check: $W$ is $k\times d$, $\delta$ is $k\times1$, $x$ is $d\times1$, so it must be $\delta x^\top$.

## Check yourself

> [!question]- What is $\nabla_w\frac12\lVert Xw-y\rVert^2$? What are the shapes if $X$ is $n\times d$?
> $X^\top(Xw-y)$: $(d\times n)(n\times1)=d\times1$, the shape of $w$.

> [!question]- Why is the softmax + cross-entropy gradient so simple?
> The $\log$ in cross-entropy cancels the $\exp$ in softmax, and the derivative reduces to $\hat p-y$ because the one-hot $y$ sums to 1.

> [!question]- Gradient of $\log|\Sigma|$ for a symmetric positive definite $\Sigma$?
> $\Sigma^{-\top}=\Sigma^{-1}$.

> [!question]- Why does reverse-mode differentiation suit neural networks better than forward mode?
> One scalar output and millions of inputs: reverse mode gets all partial derivatives in one backward pass; forward mode would need one pass per parameter.

## Practice
[Matrix Calculus Cheatsheet - Exercises](Matrix%20Calculus%20Cheatsheet%20-%20Exercises.ipynb): layouts and shape checking, why backprop runs backwards, deriving every table entry by hand (linear/quadratic forms, least squares, log-det, trace), activations and softmax + cross-entropy, a layer's chain rule and Gaussian MLE, then verifying everything numerically up to backprop for a two-layer network and ridge regression.

## Learn more
- [The Matrix Cookbook (PDF)](https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf)
- [Mathematics for ML (free)](https://mml-book.github.io/) ch. 5
- [Parr & Howard – The Matrix Calculus You Need For Deep Learning](https://explained.ai/matrix-calculus/)
