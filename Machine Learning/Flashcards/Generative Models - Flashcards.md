---
tags: [ml, deep-learning, flashcards]
---
#flashcards/ml/deep-learning

Source note: [[Generative Models]]

Which family would you pick for an exact test-set log-likelihood of an image?::A normalizing flow (or an autoregressive model): both give exact likelihoods; GANs give none, VAEs only a bound.

Why is the reparameterization trick needed in a VAE?::Sampling is not differentiable w.r.t. $\mu,\sigma$; writing $z=\mu+\sigma\odot\varepsilon$ moves the randomness into $\varepsilon$, so gradients flow through $\mu$ and $\sigma$ with low variance.

What is the optimal GAN discriminator for a fixed generator?::$D^*(x)=\frac{p_{data}(x)}{p_{data}(x)+p_g(x)}$; it equals $\tfrac12$ everywhere once $p_g=p_{data}$.

In DDPM, what does the network predict and what loss is used?::The added noise $\varepsilon$ given $(x_t,t)$, with loss $\lVert\varepsilon-\varepsilon_\theta(x_t,t)\rVert^2$.

Why are VAE samples typically blurrier than GAN samples?::The Gaussian decoder's reconstruction term is an MSE, which is minimised by averaging over plausible outputs; the GAN discriminator penalises such averages because they do not look real.
