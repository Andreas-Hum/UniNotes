---
tags: [ml, probabilistic, vi]
status: not-started
notebook: not-started
level:
reviewed:
---
# Variational Inference

> [!summary] In one sentence
> Instead of computing an intractable posterior exactly, pick a family of simple distributions and use optimisation to find the member $q_\phi(z)$ closest to the posterior, measured by KL divergence, which is the same as maximising the ELBO.

## Intuition first

In [[Bayesian Inference]] we want the posterior over latent variables, $p(z\mid x)=p(x,z)/p(x)$. The joint $p(x,z)$ is easy to evaluate; the evidence $p(x)=\int p(x,z)\,dz$ is not. [[MCMC]] answers this by *sampling*. Variational inference answers it by *fitting*.

**Analogy: a tailor with a fixed set of patterns.** The true posterior is an oddly shaped body. You cannot sew a perfect custom suit, but you have adjustable off-the-rack patterns (e.g. "all Gaussians", parameterised by mean and width). You tweak the knobs $\phi$ until the suit fits as well as it can. The fit will never be perfect if the body is weirder than any pattern, but tweaking knobs is fast: it is just gradient-based optimisation, which we are good at.

What problem does this solve? It turns an **integration** problem (hard) into an **optimisation** problem (easy, scalable to big data with stochastic gradients). This is what makes models like the VAE possible.

The catch: *which* direction of "closeness" you minimise matters, and VI uses the direction that makes $q$ cautious.

![Fitting a Gaussian q to a two-mode posterior](../../Attachments/ML%20Animations/Variational%20Inference%20-%20reverse%20vs%20forward%20KL.gif)

*Watch the yellow Gaussian start wide, then commit to one mode as $D_{KL}(q\Vert p)$ falls; the dashed red curve shows what the other KL direction would give: one broad blob covering both modes and the empty gap between them.*

## The math, step by step

### The objective

Approximate $p(z\mid x)$ by $q_\phi(z)$ minimizing $D_{KL}(q\Vert p)$, where
$$D_{KL}(q\Vert p(z\mid x))=\mathbb E_q\!\left[\log\frac{q(z)}{p(z\mid x)}\right]\ge0.$$
We cannot evaluate this directly because it contains $p(z\mid x)$, the very thing we don't know. Substitute $p(z\mid x)=p(x,z)/p(x)$:
$$D_{KL}(q\Vert p(z\mid x))=\mathbb E_q[\log q(z)]-\mathbb E_q[\log p(x,z)]+\log p(x).$$
Rearranging gives the key identity:
$$\log p(x)=\underbrace{\mathbb E_q[\log p(x,z)]-\mathbb E_q[\log q(z)]}_{\text{ELBO}(q)}+D_{KL}(q\Vert p(z\mid x)).$$

### The ELBO

Minimising $D_{KL}(q\Vert p)$ is equivalent to maximizing the **ELBO** (evidence lower bound):
$$\log p(x)\ \ge\ \mathbb E_q[\log p(x,z)]-\mathbb E_q[\log q(z)]=\mathbb E_q[\log p(x\mid z)]-D_{KL}(q(z)\Vert p(z))$$
The gap is $D_{KL}(q\Vert p(z\mid x))$ ([[Information Theory]]).

Reading it piece by piece:
- $\log p(x)$ is fixed (it does not depend on $q$). So pushing the ELBO up must push the KL gap down. That is why we can optimise the ELBO without knowing $p(x)$.
- Because KL ≥ 0, the ELBO is a **lower bound** on the log evidence; it is tight exactly when $q=p(z\mid x)$.
- Second form: $\mathbb E_q[\log p(x\mid z)]$ is a **reconstruction / data-fit** term ("make $z$ explain $x$"), and $-D_{KL}(q(z)\Vert p(z))$ is a **regulariser** ("don't stray too far from the prior"). This is exactly the VAE loss.
- First form: $\mathbb E_q[\log p(x,z)]$ rewards putting mass where the joint is high; $-\mathbb E_q[\log q]$ is the **entropy** of $q$, rewarding spread. Without the entropy term $q$ would collapse to a spike at the MAP.

### Why reverse KL is mode-seeking

$D_{KL}(q\Vert p)=\int q\log\frac qp$. Wherever $p\approx0$ but $q>0$, $\log\frac qp$ blows up, so $q$ is heavily punished for putting mass where the posterior has none. Where $q\approx0$ it pays nothing, whatever $p$ is. Hence $q$ hides inside one mode (zero-forcing / mode-seeking) and is too narrow. VI **under-estimates posterior variance (mode seeking)**. The forward direction $D_{KL}(p\Vert q)$ does the opposite (mass-covering): for a Gaussian $q$ it is minimised by matching the mean and variance of $p$, which is the dashed curve in the animation.

### Mean-field and coordinate ascent (CAVI)

- **Mean-field**: $q(z)=\prod_i q_i(z_i)$; coordinate ascent updates.

Assume the latent variables are independent under $q$. Holding all other factors fixed, the optimal factor is
$$\log q_j^*(z_j)=\mathbb E_{q_{-j}}[\log p(x,z)]+\text{const}.$$
In words: take the log joint, average out every *other* variable under its current $q$, and exponentiate. Cycle through $j$ until the ELBO stops increasing (each step can only increase it).

Example: target $\mathcal N(\mu,\Lambda^{-1})$ in 2-D with precision matrix $\Lambda$. CAVI gives Gaussian factors
$$q_1(z_1)=\mathcal N\!\big(m_1,\ \Lambda_{11}^{-1}\big),\quad m_1=\mu_1-\Lambda_{11}^{-1}\Lambda_{12}(m_2-\mu_2),$$
and symmetrically for $q_2$. The means converge to the true $\mu$, but the variance $\Lambda_{11}^{-1}$ is the *conditional* variance, which is smaller than the true marginal variance $\Sigma_{11}$ whenever $z_1,z_2$ are correlated. Mean-field throws away the correlations, and that shows up as overconfidence.

### Stochastic and black-box VI

- **Stochastic VI / BBVI**: Monte Carlo gradients; reparameterization trick (VAE, [[Generative Models]]).

When expectations have no closed form, estimate them with samples $z^{(s)}\sim q_\phi$:
$$\text{ELBO}\approx\frac1S\sum_s\big[\log p(x,z^{(s)})-\log q_\phi(z^{(s)})\big].$$
To get gradients w.r.t. $\phi$ there are two estimators:
- **Score function (REINFORCE)**: $\nabla_\phi\mathbb E_q[f(z)]=\mathbb E_q[f(z)\nabla_\phi\log q_\phi(z)]$. Works for any $q$, even discrete, but has high variance.
- **Reparameterization trick**: write $z=g_\phi(\varepsilon)$ with parameter-free noise, e.g. $z=\mu+\sigma\varepsilon$, $\varepsilon\sim\mathcal N(0,1)$. Then $\nabla_\phi\mathbb E_q[f(z)]=\mathbb E_\varepsilon[\nabla_\phi f(g_\phi(\varepsilon))]$: the gradient flows *through* the sample. Much lower variance; this is what the VAE uses.

"Stochastic VI" additionally subsamples data minibatches, so VI scales to millions of points.

### KL between two Gaussians (you will need this)

$$D_{KL}\big(\mathcal N(\mu_1,\sigma_1^2)\,\Vert\,\mathcal N(\mu_2,\sigma_2^2)\big)=\log\frac{\sigma_2}{\sigma_1}+\frac{\sigma_1^2+(\mu_1-\mu_2)^2}{2\sigma_2^2}-\frac12.$$
With $q=\mathcal N(\mu,\sigma^2)$ and prior $\mathcal N(0,1)$ this becomes $\tfrac12(\mu^2+\sigma^2-1)-\log\sigma$, the VAE's closed-form KL term.

## Worked example

Two-state latent $z\in\{0,1\}$ with $p(z=1)=0.5$, $p(x\mid z=1)=0.8$, $p(x\mid z=0)=0.2$ for the observed $x$.
- Evidence: $p(x)=0.5\cdot0.8+0.5\cdot0.2=0.5$, so $\log p(x)=-0.693$.
- True posterior: $p(z=1\mid x)=0.4/0.5=0.8$.
- Try $q(z=1)=0.5$. Joint values: $p(x,z=1)=0.4$, $p(x,z=0)=0.1$.
  $\text{ELBO}=0.5\log0.4+0.5\log0.1-(0.5\log0.5+0.5\log0.5)=-0.458-1.151+0.693=-0.916.$
- Gap: $-0.693-(-0.916)=0.223$. Check directly: $D_{KL}(q\Vert p(z\mid x))=0.5\log\frac{0.5}{0.8}+0.5\log\frac{0.5}{0.2}=-0.235+0.458=0.223$. ✓
- Set $q(z=1)=0.8$ (the true posterior): the KL is 0 and the ELBO equals $\log p(x)=-0.693$ exactly.

**Reparameterization by hand.** $f(z)=z^2$, $q=\mathcal N(\mu,\sigma^2)$. $\mathbb E[z^2]=\mu^2+\sigma^2$, so $\partial/\partial\mu=2\mu$. Via the trick: $\mathbb E_\varepsilon[\partial_\mu(\mu+\sigma\varepsilon)^2]=\mathbb E[2(\mu+\sigma\varepsilon)]=2\mu$. ✓

## Connections

- EM is VI with $q=p(z\mid x,\theta)$ ([[Gaussian Mixture Models and EM]]). The E-step sets $q$ to the exact posterior, closing the gap; the M-step maximises the ELBO in $\theta$. EM works only when that posterior is tractable; VI is the fallback when it isn't.
- Tools: Pyro, NumPyro, Stan (ADVI), TensorFlow Probability ([[Tools and Libraries]]).

Alternative: [[MCMC]]. VI is fast, deterministic and gives a cheap lower bound on the evidence; MCMC is slower but asymptotically exact.

## Common confusions

- **"VI minimises $D_{KL}(p\Vert q)$."** → Standard VI minimises the *reverse* $D_{KL}(q\Vert p)$, because only that direction needs expectations under $q$ (which we can sample) rather than under the unknown $p$.
- **"A higher ELBO means a better model, full stop."** → It is a lower bound on $\log p(x)$; comparing models by ELBO is only fair if the gaps are similar.
- **"Mean-field gets the means wrong."** → Often the means are fine (exactly right in the Gaussian example); it is the variances and correlations that suffer.
- **"The reparameterization trick changes the model."** → It only rewrites *how* a sample is drawn so gradients can pass through it; the distribution is the same.
- **"VI error goes to zero with more iterations."** → Only the optimisation error does. If the true posterior is not in the family, the gap remains.

## Check yourself

> [!question]- Why can we maximise the ELBO even though we cannot compute $\log p(x)$?
> Because $\log p(x)=\text{ELBO}+\text{KL}$ and $\log p(x)$ is constant in $q$: raising the ELBO lowers the KL by the same amount.

> [!question]- Your posterior has two well-separated modes. What does a Gaussian $q$ fitted by reverse KL look like? By forward KL?
> Reverse KL: sits on one mode, too narrow. Forward KL: one broad Gaussian over both modes (matching mean and variance), putting mass in the empty middle.

> [!question]- Compute $D_{KL}(\mathcal N(1,1)\Vert\mathcal N(0,1))$.
> $\log1+\frac{1+1}{2}-\frac12=0.5$.

> [!question]- What does mean-field VI throw away, and what symptom does that cause?
> Correlations between latent variables; it under-estimates posterior variances (over-confidence).

> [!question]- In what sense is EM a special case of VI?
> EM alternates: set $q(z)=p(z\mid x,\theta)$ (gap becomes 0), then maximise the ELBO in $\theta$. That is coordinate ascent on the ELBO with an exact E-step.

## Practice

[Variational Inference - Exercises](Variational%20Inference%20-%20Exercises.ipynb): why maximise the ELBO, mode-seeking vs mass-covering, EM as VI, the ELBO identity, Gaussian KL, a two-state ELBO, the reparameterization trick and mean-field updates by hand, then CAVI, reverse vs forward KL, Monte Carlo ELBOs, BBVI and score-function vs reparameterization gradients in code.

**Project:** [[Project - Variational Inference for Logistic Regression]] – mean-field VI vs. MCMC for Bayesian logistic regression

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 10
- [Murphy – Probabilistic ML (free)](https://probml.github.io/pml-book/) vol. 2
- [VAE paper](https://arxiv.org/abs/1312.6114)
- [Blei, Kucukelbir & McAuliffe – Variational Inference: A Review for Statisticians](https://arxiv.org/abs/1601.00670)
