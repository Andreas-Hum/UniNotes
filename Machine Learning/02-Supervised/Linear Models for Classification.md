---
tags: [ml, supervised, classification]
---
# Linear Models for Classification

Decision surfaces are hyperplanes $y(x)=w^\top x+w_0$. See your lectures in [[8-semester/ML/Lecture Notes 1-12|Lecture Notes]] and [[8-semester/ML/cheetsheet|the cheat sheet]].

| Approach | Idea | Issue |
|---|---|---|
| Least squares on 1-of-K targets | regress indicator targets | not robust to outliers, masking |
| **Perceptron** | update on mistakes $w\leftarrow w+yx$ | converges only if separable |
| **Fisher LDA** | maximize between/within class scatter | projects to $K-1$ dims |
| Probabilistic generative (LDA/QDA) | Gaussian class-conditionals | assumption-heavy |
| Probabilistic discriminative | [[Logistic Regression]] | needs iterative fit |
| One-vs-Rest / One-vs-One | combine binary classifiers | ambiguous regions with hard votes |

## Linear separability
XOR is not linearly separable → use features $\phi(x)$, [[Kernel Methods]] or [[Neural Networks]].

## LDA
Shared covariance ⇒ linear boundary; separate covariances ⇒ quadratic (QDA).
$$\delta_k(x)=x^\top\Sigma^{-1}\mu_k-\tfrac12\mu_k^\top\Sigma^{-1}\mu_k+\log\pi_k$$

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 4
- [Elements of Statistical Learning (free)](https://hastie.su.domains/ElemStatLearn/) ch. 4
