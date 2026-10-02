---
tags: [ml, fundamentals, regularization]
---
# Overfitting and Regularization

> [!summary] In one sentence
> A flexible model can memorise the noise in its training data; regularization deliberately limits that flexibility (by penalising large weights, stopping early, adding noise, …) so the model captures the signal and generalises.

**Overfitting**: the model fits noise in the training set and generalizes poorly. See [[Bias-Variance Tradeoff]].

## Intuition first

Give a student the answers to 13 practice questions. One student learns the *method*; another memorises "question 7 → answer C". Both score 100 % on the practice set, but only the first passes the exam. A degree-12 polynomial through 13 noisy points is the second student: it threads every point exactly by wiggling wildly in between.

How do you spot it? Compare training and validation error:
- **Underfitting**: both errors high (the model is too simple).
- **Good fit**: both low and close together.
- **Overfitting**: training error low, validation error much higher, and the gap grows as training continues or flexibility increases.

**Regularization** is any technique that trades a little training accuracy for much better validation accuracy, usually by expressing a preference for "simpler" solutions: smaller weights, fewer active features, fewer training steps, or robustness to perturbations.

![Ridge regularization smoothing a degree-12 polynomial](../../Attachments/ML%20Animations/Overfitting%20and%20Regularization%20-%20ridge%20smooths%20a%20polynomial.gif)
*Watch the numbers as $\lambda$ grows: train MSE rises steadily, but validation MSE first collapses (wiggles disappear) and then rises again when the curve becomes too flat.*

## Regularizers
| Method | Penalty / mechanism | Effect |
|---|---|---|
| **L2 / Ridge / weight decay** | $\lambda\lVert w\rVert_2^2$ | shrinks weights; Gaussian prior (MAP) |
| **L1 / Lasso** | $\lambda\lVert w\rVert_1$ | sparse weights; Laplace prior |
| **Elastic net** | L1 + L2 | sparse but stable with correlated features |
| **Early stopping** | stop when val loss rises | implicit regularization |
| **Dropout** | randomly zero activations | ensemble-like effect in [[Neural Networks]] |
| **Data augmentation** | transform inputs | more effective data |
| **Pruning / max depth** | limit tree size | see [[Decision Trees]] |
| **Margin maximization** | large margin | see [[Support Vector Machines]] |

**The *why* behind each row.**
- **Ridge** penalises the squared size of the weights. Large weights make the prediction very sensitive to small changes in the input (the wiggles); shrinking them smooths the function.
- **Lasso** penalises absolute values. Its penalty has a corner at $0$, so many weights become **exactly** zero: automatic feature selection.
- **Elastic net** ($\lambda_1\lVert w\rVert_1 + \lambda_2\lVert w\rVert_2^2$): with two nearly identical features, lasso arbitrarily keeps one and drops the other (and may flip between runs); the L2 part makes it share the weight between them, while L1 still zeros out irrelevant features.
- **Early stopping**: gradient descent from small initial weights fits the large, simple patterns first and the noise later. Stopping when validation loss starts rising keeps weights small, similar in effect to L2.
- **Dropout** randomly zeroes each activation with probability $p$ during training, so no unit can rely on a particular other unit; it behaves like averaging an ensemble of thinned networks. *Inverted dropout* scales the kept activations by $\frac{1}{1-p}$ so their expectation is unchanged: $\mathbb{E}[\tilde h] = (1-p)\cdot\frac{h}{1-p} = h$, and nothing needs to change at test time.
- **Data augmentation** (flips, crops, noise) encodes invariances you know to be true and effectively enlarges the dataset. **Adding Gaussian input noise** is even equivalent to ridge for linear least squares (see below).
- **Pruning / max depth** caps how finely a tree can partition the data.
- **Margin maximization**: among all separating boundaries, an SVM picks the one farthest from the data, which corresponds to the smallest $\lVert w\rVert$.

## The math, step by step

### Ridge closed form

**Ridge objective.** $J(w) = \lVert y - Xw\rVert_2^2 + \lambda\lVert w\rVert_2^2$, with $X$ the $N\times d$ design matrix and $y$ the targets.

1. Gradient: $\nabla J = -2X^\top(y - Xw) + 2\lambda w$.
2. Set to zero: $X^\top X w + \lambda w = X^\top y$, i.e. $(X^\top X + \lambda I)w = X^\top y$.
3. Solve for $w$:

$$w = (X^\top X + \lambda I)^{-1}X^\top y$$
Always invertible for $\lambda>0$.

Why: $X^\top X$ is positive *semi*-definite (eigenvalues $d_j^2 \ge 0$, where $d_j$ are the singular values of $X$). Adding $\lambda I$ shifts every eigenvalue to $d_j^2 + \lambda > 0$, so the matrix is positive definite and invertible, even with more features than samples or perfectly collinear features.

**Shrinkage, direction by direction.** In the basis of $X$'s singular vectors, ridge multiplies the least-squares coefficient along direction $j$ by
$$\frac{d_j^2}{d_j^2 + \lambda}.$$
Directions with lots of data variance (large $d_j$) are barely touched; low-variance directions, where the estimate is noisiest, are shrunk hard. Summing these factors gives the **effective degrees of freedom** $\mathrm{df}(\lambda) = \sum_j \frac{d_j^2}{d_j^2+\lambda}$, which falls from $d$ (at $\lambda = 0$) to $0$ (as $\lambda\to\infty$).

**Ridge shrinks, lasso thresholds.** With orthonormal features ($X^\top X = I$) and least-squares solution $\hat w$:
- Ridge: $w_j = \dfrac{\hat w_j}{1+\lambda}$ (proportional shrinkage, never exactly zero).
- Lasso (objective $\lVert y - Xw\rVert_2^2 + \lambda\lVert w\rVert_1$): $w_j = \operatorname{sign}(\hat w_j)\,\big(\lvert\hat w_j\rvert - \tfrac{\lambda}{2}\big)_+$ (soft thresholding: small coefficients become exactly $0$).
- The lasso sets **every** weight to zero once $\lambda \ge \lambda_{max} = 2\lVert X^\top y\rVert_\infty$ (for centred data, this objective).

**Why L1 gives zeros: the geometry.** The penalised problem is equivalent to minimising the loss subject to a budget $\lVert w\rVert \le t$. The loss contours are ellipses around the least-squares solution; the solution is where the growing ellipse first touches the constraint region. The L1 region is a diamond whose corners lie on the axes, and ellipses usually hit a corner first, giving $w_j = 0$. The L2 region is a disc with no corners, so the contact point generically has all coordinates non-zero.

![Loss contours touching the L1 diamond and the L2 disc](../../Attachments/ML%20Animations/Overfitting%20and%20Regularization%20-%20L1%20vs%20L2%20geometry.gif)
*Watch where the red contour first touches each blue region: at the diamond's corner ($w_2 = 0$) for L1, at a generic point for L2.*

**Ridge is MAP with a Gaussian prior.** Assume $y = Xw + \varepsilon$, $\varepsilon\sim\mathcal N(0,\sigma^2 I)$ and prior $w \sim \mathcal N(0, \tau^2 I)$. Then
$$-\log p(w\mid y) = \frac{1}{2\sigma^2}\lVert y - Xw\rVert^2 + \frac{1}{2\tau^2}\lVert w\rVert^2 + \text{const},$$
and multiplying by $2\sigma^2$ gives ridge with $\lambda = \sigma^2/\tau^2$. A tight prior (small $\tau$) means strong regularization. A Laplace prior $p(w_j)\propto e^{-\lvert w_j\rvert/b}$ gives the lasso the same way.

**Noise injection is ridge in disguise.** Train on $\tilde X = X + E$ with independent noise $E_{ij}\sim\mathcal N(0,\sigma^2)$. In expectation,
$$\mathbb{E}\lVert y - \tilde X w\rVert^2 = \lVert y - Xw\rVert^2 + N\sigma^2\lVert w\rVert^2,$$
i.e. ridge with $\lambda = N\sigma^2$.

## Worked example: ridge by hand

1-D, no intercept: $x = (1, 2, 3)$, $y = (2, 3, 7)$. Then $X^\top X = \sum x_i^2 = 14$ and $X^\top y = \sum x_i y_i = 29$, so $w(\lambda) = \frac{29}{14 + \lambda}$:

| $\lambda$ | 0 | 1 | 14 | 100 |
|---|---|---|---|---|
| $w$ | 2.071 | 1.933 | 1.036 | 0.254 |

The coefficient shrinks smoothly towards zero but never reaches it. The lasso with the same data ($X^\top X = 14$, not orthonormal) gives $w = \frac{(29 - \lambda/2)_+}{14}$ for $w>0$, which hits exactly $0$ at $\lambda = 58 = 2\lvert X^\top y\rvert$.

## Choosing $\lambda$
Use [[Cross-Validation and Model Selection]], never the test set.

Typical procedure: try a log-spaced grid ($10^{-4}, 10^{-3}, \dots, 10^{2}$), compute the CV error for each, pick the minimum (or the largest $\lambda$ within one standard error of the minimum, the "one-standard-error rule", for a simpler model). Standardise features first, otherwise the penalty hits features unequally.

**Reading learning curves.** Plot train and validation error against training-set size (or epochs):
- Both high and converged: high bias, so more data will not help; add flexibility or features.
- Large persistent gap: high variance, so more data, more regularization, or a simpler model will help.

## Common confusions
- **"Regularization always improves the test score."** Too much of it underfits (the right end of the animation). $\lambda$ must be tuned.
- **"Ridge performs feature selection."** It shrinks but (almost surely) never zeros weights; that is lasso's job.
- **"The intercept should be penalised too."** Usually not: penalising it makes predictions depend on where you centred $y$.
- **"Dropout is used at test time."** At test time all units are active; inverted dropout already rescaled during training.
- **"Overfitting only happens with neural networks."** Any flexible model (deep trees, high-degree polynomials, k-NN with $k=1$) can overfit.

## Check yourself

> [!question]- Training loss keeps falling while validation loss started rising after epoch 12. What do you do?
> Overfitting: use early stopping (keep the epoch-12 weights), or add regularization / data augmentation.

> [!question]- Why can ridge be solved even when there are more features than samples?
> $X^\top X$ is singular then, but $X^\top X + \lambda I$ has all eigenvalues $\ge\lambda>0$, so it is invertible.

> [!question]- Two features are exact copies of each other. What do lasso and elastic net do?
> Lasso tends to put all the weight on one of them (arbitrarily). Elastic net splits the weight equally between them.

> [!question]- With orthonormal features and $\hat w_j = 0.3$, what does the lasso give at $\lambda = 1$? Ridge?
> Lasso: $(0.3 - 0.5)_+ = 0$. Ridge: $0.3/2 = 0.15$.

> [!question]- A ridge model uses prior variance $\tau^2 = 0.5$ and noise variance $\sigma^2 = 2$. What is $\lambda$?
> $\lambda = \sigma^2/\tau^2 = 4$.

## Practice
[Overfitting and Regularization - Exercises](Overfitting%20and%20Regularization%20-%20Exercises.ipynb)

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 6
- [scikit-learn – linear models (Ridge/Lasso)](https://scikit-learn.org/stable/modules/linear_model.html)
- [StatQuest videos](https://statquest.org/video_index.html) (look for "Ridge Regression", "Lasso Regression")
- [scikit-learn – underfitting vs. overfitting example](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html)
