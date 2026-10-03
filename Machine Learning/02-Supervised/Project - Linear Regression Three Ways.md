---
tags: [ml, project, linear-regression, regularization]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Linear Regression Three Ways

> [!summary] In one sentence
> Fit linear regression on the diabetes data with the normal equations, gradient descent and scikit-learn, check they agree, then trace the ridge regularisation path.

**Notebook:** [Project - Linear Regression Three Ways](Project%20-%20Linear%20Regression%20Three%20Ways.ipynb) · topic: [[Linear Regression]] · all projects: [[Projects Overview]]

## What you build
1. `fit_normal`: $(X^\top X+\lambda I)^{-1}X^\top y$ via `solve`.
2. `fit_gd`: gradient descent on the same objective.

## Reference results (solution, laptop CPU)
Normal equations match scikit-learn to 1e-6 (OLS and ridge); GD within 0.5. OLS test MSE **3083**; best ridge λ = 100 gives **3018**. Largest OLS coefficients: s5 (34.1), bmi (27.5), s1 (23.6), and s1/s2 are strongly correlated, which is why GD converges slowly.

## Check yourself
> [!question]- Why does ridge help when features are correlated?
> X^TX is nearly singular, so OLS coefficients are huge and unstable (s1 and s2 cancel each other). Adding λI makes the system well-conditioned and shrinks such pairs.

> [!question]- Why standardise before ridge?
> The penalty λ‖w‖² treats all coefficients equally, which only makes sense if the features are on the same scale.

---
Back to [[00 - Machine Learning Index]].
