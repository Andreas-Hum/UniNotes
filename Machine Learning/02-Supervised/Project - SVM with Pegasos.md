---
tags: [ml, project, svm, optimization]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - SVM with Pegasos

> [!summary] In one sentence
> Train a linear SVM with Pegasos, stochastic sub-gradient descent on the hinge loss, match scikit-learn's LinearSVC on breast-cancer data, and see which points are support vectors.

**Notebook:** [Project - SVM with Pegasos](Project%20-%20SVM%20with%20Pegasos.ipynb) · topic: [[Support Vector Machines]] · all projects: [[Projects Overview]]

## What you build
1. `svm_objective`: $\frac\lambda2\lVert w\rVert^2+$ mean hinge loss.
2. `pegasos`: step size $1/(\lambda t)$, margin-violation updates.

## Reference results (solution, laptop CPU)
| λ = 0.1, 20 epochs | Pegasos | LinearSVC |
|---|---|---|
| objective | 0.1221 | 0.1187 |
| test accuracy | 0.953 | 0.959 |

65 of 398 training points are support vectors (margin ≤ 1). With λ = 0.01 Pegasos needs ~100 epochs to get close to the optimum.

## Check yourself
> [!question]- Why does Pegasos' convergence depend on λ?
> Its step size is 1/(λt): small λ means huge early steps and a slow 1/(λT) convergence rate. Strong convexity (λ) is what makes it fast.

> [!question]- Why do only support vectors matter?
> Points with margin > 1 have zero hinge loss and zero sub-gradient: moving them (without crossing the margin) doesn't change w.

---
Back to [[00 - Machine Learning Index]].
