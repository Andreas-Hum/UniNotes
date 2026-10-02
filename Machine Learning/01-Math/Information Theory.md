---
tags: [ml, math, information-theory]
---
# Information Theory

- **Entropy** $H(p)=-\sum p\log p$ — uncertainty. Used for split criteria in [[Decision Trees]].
- **Cross-entropy** $H(p,q)=-\sum p\log q$ — the classification loss in [[Logistic Regression]] and [[Neural Networks]].
- **KL divergence** $D_{KL}(p\Vert q)=\sum p\log\frac pq\ge0$, asymmetric. Minimizing cross-entropy = minimizing KL to the data distribution.
- **Mutual information** $I(X;Y)=H(X)-H(X\mid Y)$ — feature selection ([[Feature Engineering]]).
- **ELBO** in [[Variational Inference]] and VAEs ([[Generative Models]]) is built from KL.
- **Jensen–Shannon** divergence: symmetric, used in original GAN analysis.

Information gain $=H(\text{parent})-\sum\frac{n_k}{n}H(\text{child}_k)$.

## Learn more
- [Murphy – Probabilistic ML (free)](https://probml.github.io/pml-book/)
- [Deep Learning book – Goodfellow et al.](https://www.deeplearningbook.org/) ch. 3
