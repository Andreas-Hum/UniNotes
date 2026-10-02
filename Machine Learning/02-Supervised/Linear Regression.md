---
tags: [ml, supervised, regression]
---
# Linear Regression

> [!summary] In one sentence
> Linear regression draws the straight line (or flat plane) through the data that makes the total squared vertical error as small as possible, and that line can be found either in one shot with linear algebra or step by step with gradient descent.

## Intuition first

Imagine you have a scatter of points: house size on the $x$-axis, price on the $y$-axis. You want a rule "price ≈ something × size + something" so you can guess the price of a house you have not seen. Every candidate line makes some mistakes: for each house, the vertical gap between the true price and the line is a **residual**. Linear regression picks the line whose residuals are, in total, as small as possible.

"In total" is measured by squaring every residual and adding them up (the **sum of squared errors**, SSE). Squaring does two useful things: it makes all errors positive (so over- and under-shooting cannot cancel), and it punishes big misses much more than small ones, so the line is pulled hard towards points that are far away.

A physical picture: attach every data point to a stiff rod (the line) with a vertical spring. Each spring stores energy proportional to the squared stretch. Let go, and the rod settles where the total spring energy is lowest. That resting position is the least-squares line.

**What problem does it solve?** Predicting a continuous number from features, and, just as often, *explaining* how much the output changes when one input changes (each weight is "change in $\hat y$ per unit of that feature, holding the others fixed").

![Gradient descent tilting a line until the squared residuals are minimal](../../Attachments/ML%20Animations/Linear%20Regression%20-%20gradient%20descent%20fit.gif)
*Watch the red residual bars shrink and the SSE counter fall as gradient descent moves $(w,b)$ downhill, then settle at the same line the normal equations would give directly.*

## The math, step by step

### The model and the loss
Model $\hat y=w^\top x+b$. Loss: SSE $\sum(y_i-\hat y_i)^2$.

- $x\in\mathbb R^D$ is one input (a vector of $D$ features), $w\in\mathbb R^D$ the weights, $b$ the bias (intercept), $\hat y$ the prediction.
- In words: the prediction is a weighted sum of the features plus a constant offset.
- **Trick to hide $b$:** append a constant feature $1$ to every $x$ and put $b$ into $w$. Then $\hat y = w^\top x$ and we only have one parameter vector. Stack the $N$ samples as rows of a design matrix $X\in\mathbb R^{N\times (D+1)}$ and the targets into $y\in\mathbb R^N$; the predictions are $\hat y = Xw$ and the loss is $\|y - Xw\|^2$.

> [!note] What "linear" means
> Linear regression is linear **in the parameters $w$**, not necessarily in $x$. $\hat y = w_0 + w_1 x + w_2 x^2$ is still linear regression, because $\hat y$ is a weighted sum of fixed features $(1, x, x^2)$. That is exactly the basis-function idea below.

### Solutions

- **Normal equations**: $w=(X^\top X)^{-1}X^\top y$ (rows = samples). With columns as samples: $W=TX^\top(XX^\top)^{-1}$.
- **Gradient descent**: $\nabla=\frac2N X^\top(Xw-y)$ → [[Gradient Descent]].
- **Ridge**: add $\lambda I$; **Lasso**: L1 → [[Overfitting and Regularization]].

**Deriving the normal equations (rows = samples).**
1. Write the loss as $L(w) = (y - Xw)^\top (y - Xw) = y^\top y - 2w^\top X^\top y + w^\top X^\top X w$.
2. Differentiate: $\nabla_w L = -2X^\top y + 2X^\top X w$.
3. Set to zero: $X^\top X w = X^\top y$. These are the *normal equations*: the residual vector $y - Xw$ must be orthogonal ("normal") to every column of $X$.
4. If $X^\top X$ is invertible, $w = (X^\top X)^{-1}X^\top y$.

Geometric meaning: $Xw$ ranges over the column space of $X$; least squares picks the point in that space closest to $y$, i.e. the orthogonal projection of $y$ onto it.

**Columns-as-samples form.** Some lecture notes store each sample as a *column*: $X\in\mathbb R^{D\times N}$, targets $T\in\mathbb R^{K\times N}$ (possibly $K$ outputs at once) and the model $Y = WX$. Repeating the derivation gives $W=TX^\top(XX^\top)^{-1}$. It is the same formula transposed; just check that the shapes line up ($K\times N \cdot N\times D \cdot D\times D = K\times D$).

**Gradient of the mean squared error.** With $L = \frac1N\|Xw - y\|^2$ the gradient is $\nabla=\frac2N X^\top(Xw-y)$. Read it as: "for each feature, the average of (residual × feature value)", times 2. Gradient descent repeats $w \leftarrow w - \eta\nabla$ with learning rate $\eta$. The loss is a convex bowl, so with a small enough $\eta$ it always reaches the global minimum. Use GD when $D$ is so large that inverting $X^\top X$ ($O(D^3)$) is too expensive, or when data arrive in a stream (stochastic GD).

**Ridge closed form.** Ridge minimises $\|y - Xw\|^2 + \lambda\|w\|^2$. The gradient is $-2X^\top y + 2X^\top X w + 2\lambda w$, so
$$w_{\text{ridge}} = (X^\top X + \lambda I)^{-1}X^\top y.$$
Adding $\lambda I$ makes the matrix invertible even when features are collinear and shrinks the weights towards zero. (In practice the bias is usually not penalised.) **Lasso** uses $\lambda\|w\|_1$ instead; it has no closed form but drives some weights exactly to zero, i.e. it does feature selection.

## Probabilistic view
Assume $y=w^\top x+\varepsilon,\ \varepsilon\sim\mathcal N(0,\sigma^2)$. MLE ⇔ least squares. A Gaussian prior on $w$ gives ridge ([[Bayesian Inference]]).

Why MLE ⇔ least squares, in three lines:
1. Each target has density $p(y_i\mid x_i,w) = \frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\big(-\frac{(y_i - w^\top x_i)^2}{2\sigma^2}\big)$.
2. With independent samples the log-likelihood is $\log p(y\mid X,w) = -\frac N2\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_i (y_i - w^\top x_i)^2$.
3. The first term does not depend on $w$, so maximising the likelihood is the same as minimising $\sum_i (y_i - w^\top x_i)^2$, the SSE.

Adding a prior $w\sim\mathcal N(0,\tau^2 I)$ adds $-\frac{1}{2\tau^2}\|w\|^2$ to the log-posterior; the MAP estimate is then ridge with $\lambda = \sigma^2/\tau^2$. A strong belief that weights are small (small $\tau$) means a large penalty. This is why squared loss is "the right loss" exactly when noise is Gaussian, and why heavy-tailed noise (outliers) calls for other losses (e.g. MAE / Huber).

## Basis functions
$\hat y=w^\top\phi(x)$ with polynomials, RBFs, splines → non-linear fits, still linear in $w$.

$\phi$ maps the raw input to a new feature vector, e.g. $\phi(x) = (1, x, x^2, x^3)$ or Gaussian bumps $\phi_j(x) = \exp(-(x-\mu_j)^2/2s^2)$. Everything above (normal equations, GD, ridge) works unchanged with $\Phi$ (rows $\phi(x_i)^\top$) in place of $X$. The price: more basis functions means more flexibility and more risk of overfitting; a degree-9 polynomial through 10 points fits perfectly and generalises terribly. Regularisation and cross-validation control this.

## Worked example

Four points: $(1,1),\ (2,3),\ (3,2),\ (4,6)$. Fit $\hat y = wx + b$.

1. Means: $\bar x = 2.5$, $\bar y = 3$.
2. For one feature the solution is $w = \frac{\sum(x_i-\bar x)(y_i-\bar y)}{\sum(x_i-\bar x)^2}$, $b = \bar y - w\bar x$.
   - Numerator: $(-1.5)(-2) + (-0.5)(0) + (0.5)(-1) + (1.5)(3) = 3 + 0 - 0.5 + 4.5 = 7$.
   - Denominator: $2.25 + 0.25 + 0.25 + 2.25 = 5$.
   - $w = 1.4$, $b = 3 - 1.4\cdot 2.5 = -0.5$.
3. Same thing via the normal equations with $X = [\mathbf 1, x]$: $X^\top X = \begin{pmatrix}4 & 10\\ 10 & 30\end{pmatrix}$, $X^\top y = \begin{pmatrix}12\\ 37\end{pmatrix}$. The inverse is $\frac1{20}\begin{pmatrix}30 & -10\\ -10 & 4\end{pmatrix}$, giving $b = (360-370)/20 = -0.5$ and $w = (-120+148)/20 = 1.4$. ✓
4. Predictions $0.9,\ 2.3,\ 3.7,\ 5.1$; residuals $0.1,\ 0.7,\ -1.7,\ 0.9$ (they sum to zero, as they always do when there is an intercept).
5. SSE $= 0.01 + 0.49 + 2.89 + 0.81 = 4.2$. Total sum of squares $\sum(y_i - \bar y)^2 = 4+0+1+9 = 14$.
6. Metrics: $R^2 = 1 - 4.2/14 = 0.70$; RMSE $= \sqrt{4.2/4} \approx 1.02$; MAE $= (0.1+0.7+1.7+0.9)/4 = 0.85$.

One gradient step from $w=b=0$ with the MSE gradient: $Xw - y = -y$, so $\nabla = \frac24 X^\top(-y) = -(6,\ 18.5)$ for $(b, w)$. With $\eta = 0.01$ the first step lands at $b = 0.06$, $w = 0.185$, already heading towards $(-0.5, 1.4)$.

## Assumptions to check
Linearity, independent errors, constant variance (homoscedasticity), no strong multicollinearity. Inspect residual plots.

Why each one matters and what it looks like when it fails:
- **Linearity.** If the truth is curved, residuals vs. fitted values show a systematic U or arch. Fix: add basis functions or transform variables.
- **Independent errors.** Time series often have correlated errors (today's error predicts tomorrow's). Estimates stay unbiased, but standard errors and p-values become too optimistic.
- **Homoscedasticity.** A funnel shape in the residual plot (spread growing with $\hat y$) means the noise variance is not constant. Predictions are fine on average but uncertainty statements are wrong; try a log transform or weighted least squares.
- **No strong multicollinearity.** If two features are nearly copies of each other, $X^\top X$ is almost singular, so tiny changes in data swing the individual weights wildly (often with opposite signs) even though predictions barely change. Detect with correlation matrices or variance inflation factors; fix with ridge or by dropping a feature.
- Bonus check: roughly normal residuals (QQ-plot) if you want Gaussian confidence intervals.

## Metrics
RMSE, MAE, $R^2$ → [[Model Evaluation and Metrics]].

- **RMSE** $=\sqrt{\frac1N\sum(y_i-\hat y_i)^2}$: in the units of $y$; sensitive to big errors (it is what least squares optimises).
- **MAE** $=\frac1N\sum|y_i-\hat y_i|$: also in units of $y$; more robust to outliers.
- **$R^2$** $= 1 - \frac{\text{SSE}}{\sum(y_i-\bar y)^2}$: fraction of the variance explained relative to always predicting the mean. $1$ is perfect, $0$ is "no better than the mean", and it can be negative on test data.

## Common confusions
- *"Linear regression can only fit straight lines."* → It is linear in the **weights**; with basis functions it fits curves.
- *"Always use the normal equations, they are exact."* → Inverting $X^\top X$ costs $O(D^3)$ and is numerically fragile when features are collinear; libraries use QR/SVD (`np.linalg.lstsq`), and GD scales to huge data.
- *"A large weight means an important feature."* → Weights depend on feature scale (metres vs. millimetres) and are unstable under multicollinearity. Standardise first before comparing.
- *"High $R^2$ means the model is correct."* → $R^2$ always rises when you add features on training data; check residual plots and test-set metrics.
- *"Least squares assumes $x$ is Gaussian."* → Only the **noise** $\varepsilon$ is assumed Gaussian (for the MLE interpretation), not the inputs.

## Check yourself

> [!question]- Why does the residual vector satisfy $X^\top(y - Xw) = 0$ at the optimum?
> That is the gradient set to zero (the normal equations). Geometrically, the best $Xw$ is the orthogonal projection of $y$ onto the column space of $X$, so the leftover residual is perpendicular to every column.

> [!question]- What changes in the ridge solution compared to OLS, and why does it help with multicollinearity?
> $X^\top X$ becomes $X^\top X + \lambda I$. All eigenvalues increase by $\lambda$, so the matrix is always invertible and well-conditioned, and the weights are shrunk towards zero instead of exploding.

> [!question]- Under which noise assumption is minimising SSE the same as maximum likelihood?
> Independent Gaussian noise with constant variance: $y = w^\top x + \varepsilon$, $\varepsilon\sim\mathcal N(0,\sigma^2)$.

> [!question]- Is $\hat y = w_1 e^{x} + w_2 \sin x$ a linear regression model?
> Yes. It is linear in $w_1, w_2$ with basis functions $\phi(x) = (e^x, \sin x)$, so the normal equations still apply.

> [!question]- A residual plot shows a funnel that widens to the right. Which assumption is violated?
> Homoscedasticity (constant noise variance).

## Practice
[Linear Regression - Exercises](Linear%20Regression%20-%20Exercises.ipynb): concepts (what "linear" means, residual plots, MLE ⇔ least squares), by-hand derivations (normal equations, MSE gradient, ridge), and NumPy implementations (GD, ridge, polynomial features, metrics, multicollinearity, columns-as-samples form).

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 3
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 3
- [scikit-learn – linear models](https://scikit-learn.org/stable/modules/linear_model.html)
- [Stanford CS229 lecture notes](https://cs229.stanford.edu/main_notes.pdf): LMS, normal equations and the probabilistic interpretation (part I)
