---
tags: [ml, fundamentals, regularization]
---
# Overfitting and Regularization

**Overfitting**: the model fits noise in the training set and generalizes poorly. See [[Bias-Variance Tradeoff]].

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

## Ridge closed form
$$w = (X^\top X + \lambda I)^{-1}X^\top y$$
Always invertible for $\lambda>0$.

## Choosing $\lambda$
Use [[Cross-Validation and Model Selection]], never the test set.
