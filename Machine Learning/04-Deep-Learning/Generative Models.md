---
tags: [ml, deep-learning, generative]
---
# Generative Models

Learn $p(x)$ to sample or score data.

| Family | Idea | Pros / cons |
|---|---|---|
| **Autoencoder** | compress → reconstruct | representation, [[Anomaly Detection]] |
| **VAE** | latent $z$, maximize ELBO $\mathbb E_q\log p(x\mid z)-D_{KL}(q\Vert p)$ | stable, blurry samples ([[Variational Inference]]) |
| **GAN** | generator vs. discriminator minimax | sharp, unstable, mode collapse |
| **Normalizing flows** | invertible maps, exact likelihood | constrained architectures |
| **Autoregressive** | $p(x)=\prod p(x_t\mid x_{<t})$ | [[Transformers]] / LLMs |
| **Diffusion** | learn to denoise gradually noised data | state of the art images, slow sampling |
| **Energy-based** | unnormalized density | hard to sample |

Reparameterization trick: $z=\mu+\sigma\odot\varepsilon$ makes sampling differentiable.
Metrics: FID, Inception score, perplexity, log-likelihood ([[Model Evaluation and Metrics]]).

## Learn more
- [Understanding Deep Learning – Prince (free)](https://udlbook.github.io/udlbook/) ch. 14–18
- [VAE](https://arxiv.org/abs/1312.6114)
- [GAN](https://arxiv.org/abs/1406.2661)
- [DDPM](https://arxiv.org/abs/2006.11239)
- [Lil'Log – diffusion models](https://lilianweng.github.io/)
