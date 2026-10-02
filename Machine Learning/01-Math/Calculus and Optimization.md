---
tags: [ml, math, optimization]
---
# Calculus and Optimization

> [!summary] In one sentence
> Training a model means finding the parameters that minimize a loss; the gradient tells you which way is downhill, the Hessian tells you how the ground curves, convexity tells you whether the bottom you find is *the* bottom, and Lagrange/KKT conditions handle the case where you must stay inside some constraints.

## Intuition first

Imagine standing on a hilly landscape in thick fog, trying to reach the lowest valley. You cannot see the map, but you can feel the slope under your feet.
- The **gradient** is the slope: it points uphill (steepest ascent), so you step the opposite way. That is [[Gradient Descent]].
- The **Hessian** is how the slope changes: are you in a narrow ravine, on a gentle plain, or on a saddle (downhill in one direction, uphill in another)? Using curvature lets you take smarter steps: that is **Newton's method**.
- A **convex** landscape is one big bowl: wherever you end up at the bottom, it is the global bottom. Linear regression, logistic regression and SVMs live in bowls; deep networks live in a mountain range full of saddles.
- **Constraints** are fences ("weights must sum to 1", "stay inside the margin"). At a constrained optimum you are usually pressed against a fence, and the fence pushes back exactly as hard as the slope pulls you: that balance is the Lagrange/KKT condition.

**What problem does it solve?** It turns "learn from data" into a well-defined computation (minimize a function), tells you which algorithm to use, and tells you what guarantees to expect.

## The math, step by step

### Derivatives in many dimensions
- **Gradient** $\nabla f(x)=\big(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_d}\big)^\top$ points to steepest ascent; its length is how steep. The directional derivative along a unit vector $u$ is $\nabla f^\top u$, maximal when $u\parallel\nabla f$.
- **Hessian** $H_{ij}=\partial^2 f/\partial x_i\partial x_j$ gives curvature. It is symmetric (for smooth $f$). Its eigenvectors are the principal curvature directions, its eigenvalues how sharply $f$ bends along them.
- **Second-order Taylor expansion** around $x_0$, the local "bowl" approximation everything else is built on:
$$f(x_0+\Delta)\approx f(x_0)+\nabla f(x_0)^\top\Delta+\tfrac12\Delta^\top H(x_0)\,\Delta.$$
- **Condition number** $\kappa=\lambda_{\max}(H)/\lambda_{\min}(H)$: how elongated the bowl is. Large $\kappa$ = narrow ravine = slow, zig-zagging gradient descent.

### Convexity
- **Convex** $f$: the chord between any two points lies above the graph, $f(tx+(1-t)y)\le tf(x)+(1-t)f(y)$. Consequence: any local minimum is global.
- Check $H\succeq0$ everywhere (1D: $f''\ge0$). Other tools: sums with non-negative weights, pointwise maxima, and compositions with affine maps of convex functions are convex.
- Linear/logistic regression and SVM objectives are convex; deep nets are not. Squared loss has $H=2X^\top X\succeq0$; logistic loss has $H=X^\top SX$ with $S=\mathrm{diag}(\sigma_i(1-\sigma_i))\succeq0$; the SVM hinge loss $\max(0,1-y\,w^\top x)$ is a max of affine functions.

### Stationary points
- **Stationary point** $\nabla f=0$: min, max or saddle. Classify with the Hessian there: all eigenvalues $>0$ → local min; all $<0$ → local max; mixed signs → saddle; some zero → test inconclusive.
- **Saddles dominate in high dimension**: if each of the $d$ eigenvalues were independently positive or negative with probability $\tfrac12$, the chance that all are positive is $2^{-d}$; at $d=1000$ essentially every stationary point is a saddle. Noise in SGD helps escape them.

## Constrained optimization

![Minimizing f on a line: the optimum is where the gradients line up](../../Attachments/ML%20Animations/Calculus%20and%20Optimization%20-%20Lagrange%20multiplier%20tangency.gif)
*Slide along the green constraint and watch the two arrows: $\nabla f$ (red) has a component along the line everywhere except at $(1,1)$, where it becomes parallel to $\nabla g$ (green) and the yellow level circle just touches the line.*

Lagrangian $\mathcal L(x,\lambda)=f(x)+\sum\lambda_i g_i(x)$.

Why it works (equality constraint $g(x)=0$): if $\nabla f$ had any component *along* the constraint surface you could slide along it and decrease $f$. So at the optimum $\nabla f$ must be perpendicular to the surface, i.e. parallel to $\nabla g$: $\nabla f+\lambda\nabla g=0$. That is exactly $\nabla_x\mathcal L=0$, and $\partial\mathcal L/\partial\lambda=0$ gives back the constraint. The multiplier $\lambda$ measures how much the optimal value would change if the constraint were relaxed (the "price" of the fence).

**KKT** conditions, for $\min f(x)$ s.t. inequality constraints $g_i(x)\le0$ (multipliers $\lambda_i$):
1. **Stationarity**: $\nabla f(x)+\sum_i\lambda_i\nabla g_i(x)=0$.
2. **Primal feasibility**: $g_i(x)\le0$ (the point obeys the constraints).
3. **Dual feasibility**: $\lambda_i\ge0$ (a fence can only push, not pull).
4. **Complementary slackness**: $\lambda_i g_i(x)=0$: either the constraint is active ($g_i=0$, you are pressed against the fence) or its multiplier is zero (the fence is irrelevant).

For convex problems (with a mild regularity condition) KKT is necessary and sufficient. KKT is the basis of the dual form of [[Support Vector Machines]]: complementary slackness is why only points on or inside the margin (the support vectors) have $\alpha_i>0$.

**Projected gradient descent** handles simple constraints without multipliers: take a gradient step, then project back onto the feasible set (for a box $l\le x\le u$, just `np.clip`).

## Methods
| Method | Update | Note |
|---|---|---|
| [[Gradient Descent]] | $x\leftarrow x-\eta\nabla f$ | first order |
| Newton | $x\leftarrow x-H^{-1}\nabla f$ | quadratic convergence, costly |
| L-BFGS | quasi-Newton | good for small/medium problems |
| Coordinate descent | one variable at a time | Lasso |
| EM | alternate E and M | [[Gaussian Mixture Models and EM]] |

![Newton's method fitting and jumping to Taylor parabolas](../../Attachments/ML%20Animations/Calculus%20and%20Optimization%20-%20Newton%20method%20parabolas.gif)
*Each yellow curve is the second-order Taylor parabola at the current point; Newton jumps straight to its bottom. Far from the minimum the parabola is a rough guess; close to it the fit is nearly perfect and the error collapses ($x$: $-1\to-0.23\to0.33\to0.74\to0.97$, minimum at $x^*=1$).*

Why each one:
- **Gradient descent**: only needs $\nabla f$ ($O(d)$ per step), but its speed depends on the condition number. See [[Gradient Descent]].
- **Newton**: minimize the Taylor bowl exactly. Setting the gradient of $f(x)+\nabla f^\top\Delta+\frac12\Delta^\top H\Delta$ to zero gives $\Delta=-H^{-1}\nabla f$. It is affine-invariant (does not care about ravines) and converges **quadratically** near the optimum (the number of correct digits roughly doubles per step). On a quadratic it lands on the minimum in **one step**. Cost: forming and solving with $H$ is $O(d^2)$ memory and $O(d^3)$ time, and if $H$ is not PD the step can go uphill.
- **L-BFGS**: builds a low-rank approximation of $H^{-1}$ from the last few gradient differences; Newton-like speed with $O(md)$ memory. scikit-learn's default solver for logistic regression.
- **Coordinate descent**: minimize over one coordinate at a time with the others fixed. For the Lasso each 1D problem has a closed form, the **soft-threshold** $S(z,\lambda)=\mathrm{sign}(z)\max(|z|-\lambda,0)$, which sets small weights exactly to zero.
- **EM**: for latent-variable models, alternate filling in the hidden variables (E) and re-fitting parameters (M); each step never decreases the likelihood. See [[Gaussian Mixture Models and EM]].

Deep learning variants: [[Optimizers]].

## Worked example

**Gradient, Hessian, classification.** $f(x,y)=x^3-3x+y^2$.
1. $\nabla f=(3x^2-3,\;2y)$. Zero at $(1,0)$ and $(-1,0)$.
2. $H=\begin{bmatrix}6x&0\\0&2\end{bmatrix}$.
3. At $(1,0)$: $H=\mathrm{diag}(6,2)\succ0$ → local minimum. At $(-1,0)$: $\mathrm{diag}(-6,2)$, mixed signs → saddle. $f$ is not convex (cubic), so the local minimum is not global ($f\to-\infty$ as $x\to-\infty$).

**Lagrange multipliers** (the animation). Minimize $x^2+y^2$ s.t. $g=x+y-2=0$.
1. $\mathcal L=x^2+y^2+\lambda(x+y-2)$.
2. $\partial_x\mathcal L=2x+\lambda=0$, $\partial_y\mathcal L=2y+\lambda=0$ ⇒ $x=y$.
3. Constraint ⇒ $x=y=1$, $\lambda=-2$, $f^*=2$.

**Newton on a quadratic.** $f(x)=x^2-4x$: $f'=2x-4$, $f''=2$. From $x_0=10$: $x_1=10-\frac{16}{2}=2$, the exact minimum, in one step.

## Common confusions
- **"Gradient zero means minimum."** → It means stationary: could be a max or (in high dimension, usually) a saddle. Check the Hessian.
- **"Non-convex means gradient descent is useless."** → Deep nets are non-convex yet train well: in high dimension most bad critical points are saddles, which noise escapes, and many minima are about equally good.
- **"Newton is always better because it converges faster."** → Per *iteration*, yes; per *second*, often not: $O(d^3)$ steps are impossible for millions of parameters, and far from the optimum (or with indefinite $H$) Newton can diverge.
- **"The sign of $\lambda$ does not matter."** → For equality constraints it can be anything; for inequality constraints in the $g_i\le0$ convention, dual feasibility requires $\lambda_i\ge0$.
- **"Complementary slackness means the constraint is zero."** → It means the *product* $\lambda_ig_i$ is zero: inactive constraints get zero multipliers.

## Check yourself

> [!question]- Is $\log(1+e^{-x})$ convex? What about $x^3$ and $\sin x$?
> Logistic loss: $f''=\sigma(x)(1-\sigma(x))>0$, convex. $x^3$: $f''=6x<0$ for $x<0$, not convex on $\mathbb R$. $\sin x$: $f''=-\sin x$ changes sign, not convex.

> [!question]- Why does Newton's method solve a quadratic in one step?
> Its update minimizes the second-order Taylor model exactly, and for a quadratic that model *is* the function.

> [!question]- In the SVM dual, why are most $\alpha_i$ zero?
> Complementary slackness: $\alpha_i\big(y_i(w^\top x_i+b)-1\big)=0$. Points strictly outside the margin have the constraint inactive, so $\alpha_i=0$; only support vectors carry weight.

> [!question]- A quadratic has Hessian eigenvalues 1 and 100. What does that mean for gradient descent?
> Condition number $\kappa=100$: a long narrow ravine. A step size small enough to be stable along the steep direction ($\eta<2/100$) makes progress along the flat direction painfully slow (factor $\approx1-1/\kappa$ per step).

> [!question]- How does projected gradient descent handle $0\le x\le1$?
> Take the ordinary step $x-\eta\nabla f$, then clip each coordinate to $[0,1]$. The clip is the Euclidean projection onto the box.

## Practice
[Calculus and Optimization - Exercises](Calculus%20and%20Optimization%20-%20Exercises.ipynb): convexity checks, saddle points in high dimension, gradients/Hessians and Taylor approximations by hand, Lagrange and KKT, then from-scratch finite differences, Newton vs GD on Rosenbrock, condition numbers, coordinate descent for the Lasso, L-BFGS and projected gradient descent.

## Learn more
- [Mathematics for ML (free)](https://mml-book.github.io/) ch. 5 & 7
- [3Blue1Brown – Essence of Calculus](https://www.3blue1brown.com/lessons/essence-of-calculus/)
- [Boyd & Vandenberghe – Convex Optimization (free book)](https://web.stanford.edu/~boyd/cvxbook/): the standard reference for convexity, duality and KKT.
