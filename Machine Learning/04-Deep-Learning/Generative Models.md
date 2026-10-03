---
tags: [ml, deep-learning, generative]
status: not-started
notebook: not-started
level:
reviewed:
---
# Generative Models

> [!summary] In one sentence
> A generative model learns the data distribution $p(x)$ itself, so that it can **sample** new data that looks real or **score** how likely a given example is, and the main families (VAEs, GANs, flows, autoregressive models, diffusion, energy-based models) differ in how they make that hard-to-write-down distribution trainable.

Learn $p(x)$ to sample or score data.

## Intuition first

A classifier learns $p(y\mid x)$: "given this picture, is it a cat?" A generative model learns $p(x)$: "what do pictures of cats look like at all?" That is much harder, because $x$ is high-dimensional (a $256\times256$ RGB image has about 200,000 numbers) and almost every random setting of those numbers is noise. Real images live on a thin, curved "surface" inside that huge space.

All the families share one trick: start from something easy to sample, typically Gaussian noise $z\sim\mathcal N(0,I)$, and learn a mapping that bends it onto the data surface. They differ in how they train that mapping:

- **Autoencoder / VAE**: compress data into a small code $z$ and learn to decode it back. The VAE makes the code space a well-behaved Gaussian so you can sample from it.
- **GAN**: a forger (generator) and a detective (discriminator) play a game until the forgeries are indistinguishable.
- **Normalizing flow**: an invertible, step-by-step reshaping of the Gaussian, so the exact density can be tracked.
- **Autoregressive**: write the data one piece at a time, each piece conditioned on the previous ones (how LLMs write text).
- **Diffusion**: gradually destroy data with noise, then train a network to undo one small step of noise at a time; running the undo from pure noise creates new data.

![Two-moons data dissolving into Gaussian noise under the forward process, then denoised into a new two-moons sample](../../Attachments/ML%20Animations/Generative%20Models%20-%20diffusion%20noising.gif)

*Watch the structure disappear as $\bar\alpha_t$ falls from 1 to 0 (forward, fixed, no learning), then reappear as noise is removed (reverse, learned). The reverse pass ends on a different set of points: it is a new sample, not a copy.*

## The families at a glance

| Family | Idea | Pros / cons |
|---|---|---|
| **Autoencoder** | compress → reconstruct | representation, [[Anomaly Detection]] |
| **VAE** | latent $z$, maximize ELBO $\mathbb E_q\log p(x\mid z)-D_{KL}(q\Vert p)$ | stable, blurry samples ([[Variational Inference]]) |
| **GAN** | generator vs. discriminator minimax | sharp, unstable, mode collapse |
| **Normalizing flows** | invertible maps, exact likelihood | constrained architectures |
| **Autoregressive** | $p(x)=\prod p(x_t\mid x_{<t})$ | [[Transformers]] / LLMs |
| **Diffusion** | learn to denoise gradually noised data | state of the art images, slow sampling |
| **Energy-based** | unnormalized density | hard to sample |

## The math, step by step

### Autoencoder

Encoder $z=e(x)$, decoder $\hat x=d(z)$, trained to minimise reconstruction error $\lVert x-\hat x\rVert^2$. The bottleneck forces a compact **representation**; inputs that reconstruct badly are unusual, which is why autoencoders are used for [[Anomaly Detection]]. A *linear* autoencoder with MSE learns the same subspace as PCA. But it is **not** a generative model on its own: nothing forces the codes of training data to fill any particular region, so decoding a random $z\sim\mathcal N(0,I)$ usually gives garbage.

### VAE and the ELBO

The VAE assumes data is generated as $z\sim p(z)=\mathcal N(0,I)$, then $x\sim p(x\mid z)$ (the decoder). The exact likelihood $\log p(x)=\log\int p(x\mid z)p(z)\,dz$ is intractable, so an encoder $q(z\mid x)=\mathcal N(\mu(x),\mathrm{diag}\,\sigma^2(x))$ approximates the posterior and we maximise a lower bound:

$$\log p(x)=\underbrace{\mathbb E_q[\log p(x\mid z)]-D_{KL}\big(q(z\mid x)\Vert p(z)\big)}_{\text{ELBO}}+\underbrace{D_{KL}\big(q(z\mid x)\Vert p(z\mid x)\big)}_{\ge0}$$

- First ELBO term: **reconstruction**, decode a sampled $z$ and see how well it explains $x$.
- Second ELBO term: **regulariser**, keep each $q(z\mid x)$ close to the prior so the code space has no holes and sampling from $\mathcal N(0,I)$ works.
- The last term is $\ge0$, so the ELBO is a lower bound; it is tight when $q$ equals the true posterior. See [[Variational Inference]].
- For diagonal Gaussians the KL is closed-form: $D_{KL}\big(\mathcal N(\mu,\mathrm{diag}\,\sigma^2)\Vert\mathcal N(0,I)\big)=\tfrac12\sum_j\big(\sigma_j^2+\mu_j^2-1-\log\sigma_j^2\big)$.

**Reparameterization trick**: $z=\mu+\sigma\odot\varepsilon$ makes sampling differentiable. Sampling $z\sim\mathcal N(\mu,\sigma^2)$ directly has no gradient w.r.t. $\mu,\sigma$; writing it as a deterministic function of $\mu,\sigma$ plus outside noise $\varepsilon\sim\mathcal N(0,I)$ lets backprop flow through $\mu$ and $\sigma$. The alternative, the score-function (REINFORCE) estimator, is unbiased too but has much higher variance.

**Why VAE samples are blurry**: with a Gaussian decoder the reconstruction term is an MSE, and when several sharp images are plausible for one $z$, the MSE-optimal output is their *average*, which is blurry.

### GAN

A generator $G(z)$ maps noise to samples; a discriminator $D(x)\in(0,1)$ estimates the probability that $x$ is real. They play the minimax game

$$\min_G\max_D\ \mathbb E_{x\sim p_{data}}[\log D(x)]+\mathbb E_{z}[\log(1-D(G(z)))]$$

- For a fixed generator the best discriminator is $D^*(x)=\frac{p_{data}(x)}{p_{data}(x)+p_g(x)}$; plugging it in, the generator minimises $-\log4+2\,\mathrm{JSD}(p_{data}\Vert p_g)$, a divergence between real and fake distributions.
- In practice $G$ maximises $\log D(G(z))$ instead (**non-saturating loss**): early on, when $D$ easily rejects fakes, $\log(1-D(G(z)))$ is flat and gives almost no gradient.
- **Sharp** samples, because nothing averages over possibilities; but **unstable** (two networks chasing each other) and prone to **mode collapse** (the generator produces only a few kinds of output that fool $D$).
- There is no likelihood, so a GAN can sample but cannot score.

### Normalizing flows

An invertible map $x=f(z)$ with $z\sim p_z$. The change-of-variables formula gives the **exact likelihood**:

$$\log p_x(x)=\log p_z\big(f^{-1}(x)\big)+\log\left|\det\frac{\partial f^{-1}}{\partial x}\right|$$

The determinant accounts for how much $f$ stretches or squeezes volume. The catch: every layer must be invertible with a cheap determinant (e.g. triangular Jacobians), hence **constrained architectures**.

### Autoregressive models

The chain rule of probability, $p(x)=\prod_t p(x_t\mid x_{<t})$, is exact. Model each conditional with a network (a causal [[Transformers|Transformer]] for text, as in LLMs). Exact likelihood and excellent quality; sampling is sequential, one token at a time. Evaluated by **perplexity**, $\exp$ of the average negative log-likelihood per token: "how many choices was the model effectively hesitating between?"

### Diffusion

**Forward process** (fixed): add a little Gaussian noise for $T$ steps, $x_t=\sqrt{1-\beta_t}\,x_{t-1}+\sqrt{\beta_t}\,\varepsilon_t$. With $\bar\alpha_t=\prod_{s\le t}(1-\beta_s)$ you can jump to any step directly:

$$x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon,\qquad\varepsilon\sim\mathcal N(0,I)$$

As $\bar\alpha_t\to0$, $x_t$ becomes pure noise whatever $x_0$ was.

**Reverse process** (learned): a network $\varepsilon_\theta(x_t,t)$ predicts the noise that was added, trained with the simple loss $\mathbb E\,\lVert\varepsilon-\varepsilon_\theta(x_t,t)\rVert^2$ (DDPM). Sampling starts at pure noise and repeatedly removes a little of the predicted noise. State of the art for images, but **slow sampling** (tens to hundreds of network calls per sample).

### Energy-based models

Define $p(x)\propto e^{-E(x)}$ with a learned energy $E$. Very flexible (any network can be an energy), but the normaliser $\int e^{-E(x)}dx$ is intractable: this is an **unnormalized density**, and drawing samples needs MCMC, so it is **hard to sample**.

## Worked example

**Flow likelihood.** $z\sim\mathcal N(0,1)$, $x=f(z)=2z+1$. For $x=3$: $f^{-1}(3)=1$, $\log p_z(1)=-\tfrac12\log2\pi-\tfrac12=-1.419$, and $\frac{df^{-1}}{dx}=\tfrac12$, so $\log p_x(3)=-1.419+\log\tfrac12=-2.112$. The stretch by 2 halves the density.

**VAE KL term.** One latent dimension with $\mu=1$, $\sigma=1$: $\tfrac12(1+1-1-0)=0.5$ nats. With $\mu=0,\sigma=1$ it is 0, so the KL only charges for codes that move away from the prior.

**Perplexity.** A language model gives the four tokens of a sentence probabilities $0.5, 0.25, 0.125, 0.5$. Average negative log-likelihood: $\tfrac14(1+2+3+1)=1.75$ bits, so perplexity $=2^{1.75}\approx3.36$: on average the model is as unsure as a uniform choice among about 3.4 tokens.

**Diffusion jump.** With $\bar\alpha_t=0.25$: $x_t=0.5\,x_0+0.866\,\varepsilon$, so the signal still contributes half its scale, the noise most of the rest.

## Metrics

Metrics: FID, Inception score, perplexity, log-likelihood ([[Model Evaluation and Metrics]]).

- **FID** (Fréchet Inception Distance): embed real and generated images with an Inception network, fit a Gaussian to each set of features, and compute $\lVert\mu_1-\mu_2\rVert^2+\mathrm{Tr}\big(\Sigma_1+\Sigma_2-2(\Sigma_1\Sigma_2)^{1/2}\big)$. Lower is better; it captures both quality and diversity.
- **Inception score**: high when each sample is confidently classified *and* the classes are diverse. Ignores the real data, so weaker than FID.
- **Perplexity / log-likelihood**: only for models with a tractable likelihood (autoregressive, flows; bounds for VAEs and diffusion).

## Common confusions

- "An autoencoder is a generative model." → Not by itself; without the VAE's KL regulariser the code space has holes and random codes decode to junk.
- "The ELBO is the log-likelihood." → It is a lower bound; the gap is $D_{KL}(q(z\mid x)\Vert p(z\mid x))$.
- "GAN mode collapse means training diverged." → The loss can look fine; the generator just covers a few modes of the data. Check sample diversity.
- "Diffusion learns the forward noising process." → The forward process is fixed; only the reverse denoiser is learned.
- "Higher likelihood always means better samples." → Likelihood and perceptual quality can disagree; that is why sample-based metrics such as FID exist.

## Check yourself

> [!question]- Which family would you pick for an exact test-set log-likelihood of an image?
> A normalizing flow (or an autoregressive model): both give exact likelihoods; GANs give none, VAEs only a bound.

> [!question]- Why is the reparameterization trick needed in a VAE?
> Sampling is not differentiable w.r.t. $\mu,\sigma$; writing $z=\mu+\sigma\odot\varepsilon$ moves the randomness into $\varepsilon$, so gradients flow through $\mu$ and $\sigma$ with low variance.

> [!question]- What is the optimal GAN discriminator for a fixed generator?
> $D^*(x)=\frac{p_{data}(x)}{p_{data}(x)+p_g(x)}$; it equals $\tfrac12$ everywhere once $p_g=p_{data}$.

> [!question]- In DDPM, what does the network predict and what loss is used?
> The added noise $\varepsilon$ given $(x_t,t)$, with loss $\lVert\varepsilon-\varepsilon_\theta(x_t,t)\rVert^2$.

> [!question]- Why are VAE samples typically blurrier than GAN samples?
> The Gaussian decoder's reconstruction term is an MSE, which is minimised by averaging over plausible outputs; the GAN discriminator penalises such averages because they do not look real.

## Practice

[Generative Models - Exercises](Generative%20Models%20-%20Exercises.ipynb): choosing a family, blurry VAEs and collapsing GANs, autoencoders vs generative models, the Gaussian KL, deriving the ELBO, the optimal discriminator, change of variables, perplexity and the diffusion forward process by hand, then code for reparameterization vs score-function gradients, the VAE loss, GAN losses from logits, a linear autoencoder that learns PCA, an affine flow, diffusion noise prediction and FID.

## Learn more

- [Understanding Deep Learning – Prince (free)](https://udlbook.github.io/udlbook/) ch. 14–18
- [VAE](https://arxiv.org/abs/1312.6114)
- [GAN](https://arxiv.org/abs/1406.2661)
- [DDPM](https://arxiv.org/abs/2006.11239)
- [Lil'Log – diffusion models](https://lilianweng.github.io/)
- [Lilian Weng – What are Diffusion Models?](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/) (direct link to the post)
- [Calvin Luo – Understanding Diffusion Models: A Unified Perspective](https://arxiv.org/abs/2208.11970)
