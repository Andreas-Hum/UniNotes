---
tags: [ml, probabilistic, vi]
---
# Variational Inference

Approximate $p(z\mid x)$ by $q_\phi(z)$ minimizing $D_{KL}(q\Vert p)$. Equivalent to maximizing the **ELBO**:
$$\log p(x)\ \ge\ \mathbb E_q[\log p(x,z)]-\mathbb E_q[\log q(z)]=\mathbb E_q[\log p(x\mid z)]-D_{KL}(q(z)\Vert p(z))$$
The gap is $D_{KL}(q\Vert p(z\mid x))$ ([[Information Theory]]).

- **Mean-field**: $q(z)=\prod_i q_i(z_i)$; coordinate ascent updates.
- **Stochastic VI / BBVI**: Monte Carlo gradients; reparameterization trick (VAE, [[Generative Models]]).
- Under-estimates posterior variance (mode seeking).
- EM is VI with $q=p(z\mid x,\theta)$ ([[Gaussian Mixture Models and EM]]).
- Tools: Pyro, NumPyro, Stan (ADVI), TensorFlow Probability ([[Tools and Libraries]]).

Alternative: [[MCMC]].

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 10
- [Murphy – Probabilistic ML (free)](https://probml.github.io/pml-book/) vol. 2
- [VAE paper](https://arxiv.org/abs/1312.6114)
