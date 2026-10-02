---
tags: [ml, supervised, regression]
---
# Linear Regression

Model $\hat y=w^\top x+b$. Loss: SSE $\sum(y_i-\hat y_i)^2$.

## Solutions
- **Normal equations**: $w=(X^\top X)^{-1}X^\top y$ (rows = samples). With columns as samples: $W=TX^\top(XX^\top)^{-1}$.
- **Gradient descent**: $\nabla=\frac2N X^\top(Xw-y)$ → [[Gradient Descent]].
- **Ridge**: add $\lambda I$; **Lasso**: L1 → [[Overfitting and Regularization]].

## Probabilistic view
Assume $y=w^\top x+\varepsilon,\ \varepsilon\sim\mathcal N(0,\sigma^2)$. MLE ⇔ least squares. A Gaussian prior on $w$ gives ridge ([[Bayesian Inference]]).

## Basis functions
$\hat y=w^\top\phi(x)$ with polynomials, RBFs, splines → non-linear fits, still linear in $w$.

## Assumptions to check
Linearity, independent errors, constant variance (homoscedasticity), no strong multicollinearity. Inspect residual plots.

## Metrics
RMSE, MAE, $R^2$ → [[Model Evaluation and Metrics]].

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 3
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 3
- [scikit-learn – linear models](https://scikit-learn.org/stable/modules/linear_model.html)
