---
tags: [ml, supervised, classification]
---
# Linear Models for Classification

> [!summary] In one sentence
> A linear classifier splits input space with a flat hyperplane $w^\top x+w_0=0$, and the different methods (least squares, perceptron, Fisher, LDA/QDA, logistic regression) are just different recipes for choosing where that hyperplane goes.

## Intuition first

Picture two kinds of fruit scattered on a table according to weight and colour. A linear classifier is a ruler laid across the table: everything on one side is called "apple", everything on the other "pear". In more dimensions the ruler becomes a plane, then a hyperplane, but the idea is the same: compute a **score** $y(x) = w^\top x + w_0$ and look at its **sign**.

- $w$ is the direction the ruler *faces* (its normal vector): moving along $w$ increases the score fastest.
- $w_0$ slides the ruler without rotating it.
- The size of the score tells you how far you are from the boundary: the signed distance is $y(x)/\|w\|$.

Why bother with such a simple shape? Linear models are fast, need little data, are easy to interpret, and are the building blocks of more powerful methods: [[Kernel Methods]] and [[Neural Networks]] are, at heart, linear classifiers applied to cleverly transformed features.

The interesting question is *how to choose the ruler*. Each method answers it differently:
- **Least squares**: pretend the labels are numbers and fit a regression.
- **Perceptron**: start anywhere, nudge the ruler whenever it gets a point wrong.
- **Fisher**: pick the direction where, after projecting, the classes are far apart and tight.
- **Generative (LDA/QDA)**: model what each class looks like (a Gaussian blob), then use Bayes' rule.
- **Discriminative**: model $p(\text{class}\mid x)$ directly ([[Logistic Regression]]).

![Perceptron rotating its decision boundary after each mistake](../../Attachments/ML%20Animations/Linear%20Models%20for%20Classification%20-%20perceptron%20updates.gif)
*Watch the green weight vector $\mathbf w$: each misclassified point (red ring) adds $y_i\mathbf x_i$ to it, the boundary (always perpendicular to $\mathbf w$) swings round, and after three updates every point is on its correct side.*

## The big picture

Decision surfaces are hyperplanes $y(x)=w^\top x+w_0$. See your lectures in [[8-semester/ML/Lecture Notes 1-12|Lecture Notes]] and [[8-semester/ML/cheetsheet|the cheat sheet]].

| Approach | Idea | Issue |
|---|---|---|
| Least squares on 1-of-K targets | regress indicator targets | not robust to outliers, masking |
| **Perceptron** | update on mistakes $w\leftarrow w+yx$ | converges only if separable |
| **Fisher LDA** | maximize between/within class scatter | projects to $K-1$ dims |
| Probabilistic generative (LDA/QDA) | Gaussian class-conditionals | assumption-heavy |
| Probabilistic discriminative | [[Logistic Regression]] | needs iterative fit |
| One-vs-Rest / One-vs-One | combine binary classifiers | ambiguous regions with hard votes |

**Which one when?** Need probabilities and robustness → logistic regression. Few samples and roughly Gaussian classes with similar spread → LDA. Classes with clearly different spreads and plenty of data → QDA. Want a low-dimensional projection for visualisation → Fisher. Streaming data / teaching the idea of online learning → perceptron. Least squares is mostly a cautionary tale.

## The math, step by step

### Least squares on 1-of-K targets
Encode class $k$ as a one-hot target vector $t$ (e.g. $(0,1,0)$), fit a linear regression from $x$ to $t$ (closed form $W = (X^\top X)^{-1}X^\top T$ with a bias column in $X$), then predict $\arg\max_k y_k(x)$.
- **Why it breaks:** squared error punishes points that are *too correct* (far on the right side), so outliers drag the boundary.
- **Masking:** with $K\ge 3$ classes lined up along one direction, the middle class's fitted indicator is a straight line that is never the largest; the middle class gets "masked" and is never predicted.

### Perceptron
For labels $y_i\in\{-1,+1\}$ (bias folded into $w$ via a constant feature), predict $\operatorname{sign}(w^\top x)$. Cycle through the data:
$$\text{if } y_i\,w^\top x_i \le 0:\quad w\leftarrow w+y_ix_i.$$
- In words: if point $i$ is on the wrong side (or on the line), add it to $w$ if it is positive, subtract it if it is negative. That rotates $w$ towards positive mistakes and away from negative ones.
- Why it helps: after the update, $y_i w_{\text{new}}^\top x_i = y_i w^\top x_i + \|x_i\|^2$, so the score of that point moves towards the correct sign.
- **Convergence theorem (Novikoff):** if some unit vector $w^*$ separates the data with margin $\gamma$ ($y_i w^{*\top}x_i \ge \gamma$) and all $\|x_i\|\le R$, the perceptron makes at most $(R/\gamma)^2$ mistakes. If the data are *not* separable it never settles; it cycles forever.
- It is stochastic gradient descent on the "perceptron loss" $\max(0, -y\,w^\top x)$.

### Fisher's linear discriminant
Project every point onto a line, $z = w^\top x$. A good direction makes the projected class means far apart *relative to* the spread within each class. For two classes with means $m_1, m_2$:
$$J(w) = \frac{(w^\top m_2 - w^\top m_1)^2}{s_1^2 + s_2^2} = \frac{w^\top S_B w}{w^\top S_W w},$$
where $S_B = (m_2 - m_1)(m_2 - m_1)^\top$ is the **between-class scatter** and $S_W = \sum_k\sum_{i\in k}(x_i - m_k)(x_i - m_k)^\top$ the **within-class scatter**.
- Setting the derivative to zero gives $w \propto S_W^{-1}(m_2 - m_1)$.
- Intuition: just joining the means ($w \propto m_2 - m_1$) ignores the shape of the clouds. $S_W^{-1}$ down-weights directions in which the classes are spread out and up-weights directions where they are tight.
- Fisher gives a *direction*, not a classifier; you still pick a threshold on $z$.
- With $K$ classes, $S_B$ has rank at most $K-1$, so Fisher projects to at most $K-1$ dims.

### Probabilistic generative models: LDA and QDA
Model each class as a Gaussian, $p(x\mid k) = \mathcal N(x\mid\mu_k, \Sigma_k)$ with prior $\pi_k$, and classify by the largest $\log\big(\pi_k\,p(x\mid k)\big)$.

Shared covariance ⇒ linear boundary; separate covariances ⇒ quadratic (QDA).
$$\delta_k(x)=x^\top\Sigma^{-1}\mu_k-\tfrac12\mu_k^\top\Sigma^{-1}\mu_k+\log\pi_k$$

**Derivation of $\delta_k$.**
1. $\log \pi_k p(x\mid k) = -\tfrac12(x-\mu_k)^\top\Sigma^{-1}(x-\mu_k) - \tfrac12\log|2\pi\Sigma| + \log\pi_k$.
2. Expand the quadratic: $-\tfrac12 x^\top\Sigma^{-1}x + x^\top\Sigma^{-1}\mu_k - \tfrac12\mu_k^\top\Sigma^{-1}\mu_k$.
3. With a shared $\Sigma$, the terms $-\tfrac12x^\top\Sigma^{-1}x$ and $-\tfrac12\log|2\pi\Sigma|$ are the same for every class, so they cannot change the argmax. Drop them and what remains is $\delta_k(x)$, **linear in $x$**.
4. With class-specific $\Sigma_k$ (QDA), the $x^\top\Sigma_k^{-1}x$ term differs between classes and stays, together with $-\tfrac12\log|\Sigma_k|$, so boundaries are **quadratic** (ellipses, parabolas, hyperbolas).

Fitting is just computing class frequencies (priors), class means and the (pooled) covariance. LDA has fewer parameters ($\Sigma$ shared) → lower variance; QDA is more flexible but needs $K\cdot D(D+1)/2$ covariance parameters.

For two classes the LDA posterior is exactly $\sigma(w^\top x + w_0)$, the same form as logistic regression; the two differ in *how* $w$ is estimated (fit the Gaussians vs. maximise conditional likelihood).

### Multiclass from binary: OvR and OvO
- **One-vs-Rest:** $K$ classifiers, "class $k$ vs everything else". With hard votes, some regions are claimed by several classifiers or by none.
- **One-vs-One:** $K(K-1)/2$ classifiers, one per pair, then majority vote. Each is trained on less data, but ties and ambiguous regions can still occur.
- Fix for both: compare continuous scores and take $\arg\max_k y_k(x)$, which always gives a single answer and connected, convex decision regions.

## Linear separability
XOR is not linearly separable → use features $\phi(x)$, [[Kernel Methods]] or [[Neural Networks]].

XOR: points $(0,0),(1,1)$ are class A and $(0,1),(1,0)$ class B. Any line that puts both A-corners on one side must also put at least one B-corner there (the two diagonals cross). But add the feature $\phi_3 = x_1x_2$ (or use $\phi = (x_1, x_2, (x_1 - x_2)^2)$): in the lifted space a plane separates them. That is the whole idea behind basis functions, kernels and hidden layers.

## Worked example

**Perceptron, two updates.** Start at $w=(0,0)$ (no bias, for simplicity).
1. $x_1 = (1,2),\ y_1=+1$: $y_1 w^\top x_1 = 0 \le 0$ → mistake, $w = (1,2)$.
2. $x_2 = (2,-1),\ y_2=-1$: $w^\top x_2 = 2 - 2 = 0$, so $y_2 w^\top x_2 = 0 \le 0$ → mistake, $w = (1,2) - (2,-1) = (-1,3)$.
3. Check: $w^\top x_1 = 5 > 0$ ✓, $w^\top x_2 = -5 < 0$ ✓. Converged; the boundary is $-x_1 + 3x_2 = 0$.

**Fisher with numbers.** Class means $m_1 = (1,1)$, $m_2 = (3,2)$, within-class scatter $S_W = \operatorname{diag}(2, 0.5)$.
$w \propto S_W^{-1}(m_2 - m_1) = (2/2,\ 1/0.5) = (1, 2)$. Although the means differ more along feature 1, feature 2 gets *twice* the weight because the classes are much tighter in that direction.

**LDA in 1-D.** $\mu_0 = 0$, $\mu_1 = 2$, $\sigma^2 = 1$. Then $\delta_k(x) = x\mu_k - \mu_k^2/2 + \log\pi_k$.
- Equal priors: $\delta_1 > \delta_0 \iff 2x - 2 > 0 \iff x > 1$, the midpoint.
- With $\pi_1 = 0.2$: $2x - 2 + \log 0.2 > \log 0.8 \iff x > 1 + \tfrac12\log 4 \approx 1.69$. The rarer class has to "earn" its region: the boundary moves towards it.

**Counting classifiers.** $K = 5$ classes: OvR trains 5 classifiers, OvO trains $5\cdot4/2 = 10$.

## Common confusions
- *"Fisher LDA and Gaussian LDA are different things."* → For two classes they give the same direction $\Sigma^{-1}(m_2-m_1)$; Fisher derives it without any Gaussian assumption.
- *"The perceptron finds the best separating line."* → It finds *a* separating line, depending on initialisation and order. The maximum-margin one is the [[Support Vector Machines|SVM]].
- *"LDA is for dimensionality reduction only."* → It is both: a classifier (generative model) and, via Fisher, a projection to $K-1$ dims.
- *"Linear models cannot learn non-linear boundaries."* → They can, in a transformed feature space $\phi(x)$; the boundary is linear in $\phi$ but curved in $x$.
- *"QDA is always better since it is more flexible."* → It has far more parameters; with little data its covariance estimates are noisy and LDA often generalises better (bias–variance).

## Check yourself

> [!question]- Why does the shared-covariance assumption make the LDA boundary linear?
> The quadratic term $-\tfrac12x^\top\Sigma^{-1}x$ is identical for every class, so it cancels when comparing classes; only terms linear in $x$ remain.

> [!question]- What does the perceptron do on data that are not linearly separable?
> It never converges: there is always a misclassified point, so $w$ keeps changing. Use a pocket algorithm, averaging, or a soft-margin method instead.

> [!question]- What is Fisher's optimal direction, and what does $S_W^{-1}$ do to it?
> $w\propto S_W^{-1}(m_2-m_1)$. $S_W^{-1}$ shrinks directions of large within-class spread and stretches directions where classes are compact.

> [!question]- How many binary classifiers do OvR and OvO need for $K = 10$ classes?
> OvR: 10. OvO: $10\cdot 9/2 = 45$.

> [!question]- Give one feature that makes XOR linearly separable.
> $x_1x_2$ (or $(x_1-x_2)^2$): in the new 3-D space a plane separates the two classes.

## Practice
[Linear Models for Classification - Exercises](Linear%20Models%20for%20Classification%20-%20Exercises.ipynb): choosing a method, masking, XOR, OvR vs OvO counts, perceptron by hand and its convergence bound, Fisher's criterion with numbers, deriving and evaluating LDA discriminants, then coding the perceptron, Fisher, LDA, QDA, an XOR feature map and one-vs-rest from scratch.

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 4
- [Elements of Statistical Learning (free)](https://hastie.su.domains/ElemStatLearn/) ch. 4
- [Stanford CS231n – linear classification](https://cs231n.github.io/linear-classify/): the "template matching" and geometric view of linear scores
