---
tags: [ml, supervised, classification]
---
# Logistic Regression

$$p(y=1\mid x)=\sigma(w^\top x+b)=\frac1{1+e^{-(w^\top x+b)}}$$

Decision boundary $w^\top x+b=0$ is a hyperplane.

## Loss
Negative log-likelihood (binary cross-entropy):
$$L=-\sum_i y_i\log\hat p_i+(1-y_i)\log(1-\hat p_i)$$
Convex; gradient $\nabla_w=X^\top(\hat p-y)$. No closed form → [[Gradient Descent]] or IRLS (Newton).

## Multiclass
**Softmax** $p_k=\frac{e^{z_k}}{\sum_j e^{z_j}}$ with cross-entropy; gradient $\hat p-y$.

## Notes
- Perfectly separable data ⇒ weights diverge; add L2 ([[Overfitting and Regularization]]).
- Coefficients = log-odds change per unit feature.
- Calibrated probabilities out of the box (unlike [[Support Vector Machines]]).
- It is a single-neuron [[Neural Networks|neural network]].

See also [[Linear Models for Classification]], [[Information Theory]].
