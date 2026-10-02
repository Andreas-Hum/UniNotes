---
tags: [ml, unsupervised, probabilistic, em]
---
# Gaussian Mixture Models and EM

> [!summary] In one sentence
> A Gaussian mixture model says each data point was produced by first secretly picking one of $K$ Gaussian "bells" and then sampling from it, and the EM algorithm fits it by alternating between guessing which bell produced each point (E-step) and refitting each bell to the points it probably produced (M-step).

## Intuition first

You measure the heights of 1000 adults but forget to record anyone's sex. The histogram has a lump that is really two overlapping bell curves (women and men). If you *knew* who was who, fitting two Gaussians would be trivial: compute each group's mean and variance. If you *knew* the two Gaussians, guessing who was who would also be easy: for each height, ask which bell makes it more likely. You know neither. EM breaks this chicken-and-egg problem by **alternating**: guess the groups softly, refit the bells, re-guess, refit, until nothing changes.

Two differences from k-means ([[Clustering]]):
- **Soft assignments**: a point halfway between two bells is "50% each", not forced into one.
- **Shapes**: each component has its own covariance, so clusters can be stretched, tilted ellipses of different sizes, not just round blobs.

You also get a full **density** $p(x)$, which you can sample from, use for anomaly detection ([[Anomaly Detection]]), or compare models with by likelihood.

![EM fitting two Gaussians: dot colours become responsibilities and the ellipses stretch and rotate to fit](../../Attachments/ML%20Animations/Gaussian%20Mixture%20Models%20and%20EM%20-%20EM%20iterations.gif)
*Watch the purple dots between the clusters (they belong partly to both) and the log-likelihood on the right, which only goes up while the ellipses turn into the tilted shape of each cluster.*

## The math, step by step

### The model
$$p(x)=\sum_{k=1}^K\pi_k\,\mathcal N(x\mid\mu_k,\Sigma_k)$$
- $\pi_k\ge0$, $\sum_k\pi_k=1$: **mixing weights**, the prior probability that a point comes from component $k$.
- $\mu_k$: mean (centre) of component $k$; $\Sigma_k$: its covariance (size, shape, orientation of the ellipse).
- $\mathcal N(x\mid\mu,\Sigma)=\frac{1}{(2\pi)^{d/2}|\Sigma|^{1/2}}\exp\!\big(-\tfrac12(x-\mu)^\top\Sigma^{-1}(x-\mu)\big)$.

Latent variable $z$ = component. Generative story: draw $z\sim\text{Categorical}(\pi)$, then $x\mid z=k\sim\mathcal N(\mu_k,\Sigma_k)$. Summing out the unobserved $z$ gives the formula above.

Useful facts: the mixture mean is $\mathbb E[x]=\sum_k\pi_k\mu_k$, and in 1-D its variance is $\operatorname{Var}[x]=\sum_k\pi_k(\sigma_k^2+\mu_k^2)-\big(\sum_k\pi_k\mu_k\big)^2$ ("average within-component variance + spread of the means").

### Why not just maximise the likelihood directly?
$$\log L=\sum_{i=1}^N\log\sum_{k=1}^K\pi_k\,\mathcal N(x_i\mid\mu_k,\Sigma_k)$$
Direct MLE has a log of a sum, no closed form → **EM**. The log cannot pass inside the sum, so the gradient equations for one component involve all the others; setting them to zero gives coupled equations with no closed-form solution. If we knew $z_i$, the log would act on a single Gaussian and everything would decouple into simple per-component averages. EM exploits exactly that.

## EM
- **E-step**: responsibilities $\gamma_{ik}=\frac{\pi_k\mathcal N(x_i\mid\mu_k,\Sigma_k)}{\sum_j\pi_j\mathcal N(x_i\mid\mu_j,\Sigma_j)}$
- **M-step**: with $N_k=\sum_i\gamma_{ik}$:
  $\mu_k=\frac1{N_k}\sum\gamma_{ik}x_i$, $\Sigma_k=\frac1{N_k}\sum\gamma_{ik}(x_i-\mu_k)(x_i-\mu_k)^\top$, $\pi_k=N_k/N$

In words:
- $\gamma_{ik}=p(z_i=k\mid x_i)$ is Bayes' rule: prior $\pi_k$ times likelihood, normalised over components. It is the **probability that component $k$ produced point $i$**; each row sums to 1.
- $N_k$ is the **effective number of points** owned by component $k$ (a soft count).
- The M-step formulas are the ordinary mean, covariance and proportion, but with each point **weighted** by how much the component owns it.

**Deriving the mean update.** Treat the $\gamma_{ik}$ as fixed weights and maximise $\sum_i\sum_k\gamma_{ik}\log\mathcal N(x_i\mid\mu_k,\Sigma_k)$. The only $\mu_k$-dependent part is $-\tfrac12\sum_i\gamma_{ik}(x_i-\mu_k)^\top\Sigma_k^{-1}(x_i-\mu_k)$. Its gradient is $\sum_i\gamma_{ik}\Sigma_k^{-1}(x_i-\mu_k)=0$; multiply by $\Sigma_k$ and solve: $\mu_k=\sum_i\gamma_{ik}x_i/N_k$. The $\pi_k$ update comes the same way with a Lagrange multiplier for $\sum_k\pi_k=1$.

**Numerically stable E-step.** In high dimensions $\mathcal N(x\mid\cdot)$ underflows to 0. Work with logs: $\ell_{ik}=\log\pi_k+\log\mathcal N(x_i\mid\mu_k,\Sigma_k)$, then $\gamma_{ik}=\exp\big(\ell_{ik}-\operatorname{logsumexp}_j\ell_{ij}\big)$, where logsumexp subtracts the maximum before exponentiating.

### Why EM works
The log-likelihood never decreases (it maximizes a lower bound; same ELBO idea as [[Variational Inference]]).

For any distribution $q(z)$ over the latent, Jensen's inequality ($\log$ is concave) gives
$$\log p(x)=\log\sum_z q(z)\frac{p(x,z)}{q(z)}\ \ge\ \sum_z q(z)\log\frac{p(x,z)}{q(z)}=\text{ELBO}(q,\theta),$$
and the gap is exactly $\mathrm{KL}\big(q(z)\,\Vert\,p(z\mid x)\big)\ge0$.
- **E-step**: set $q(z)=p(z\mid x,\theta^{\text{old}})$ (the responsibilities). The KL gap becomes 0, so the bound touches $\log p(x)$ at the current parameters.
- **M-step**: maximise the ELBO over $\theta$. The bound goes up, and $\log p(x)$, which is always at least the bound, goes up at least as much.

So $\log p(x\mid\theta^{\text{new}})\ge\text{ELBO}(\theta^{\text{new}})\ge\text{ELBO}(\theta^{\text{old}})=\log p(x\mid\theta^{\text{old}})$. EM climbs monotonically, but only to a **local** maximum (or saddle point).

## Worked example (1-D, by hand)

Data $\{0,2,4\}$, $K=2$, start with $\pi=(0.5,0.5)$, $\mu=(0,4)$, $\sigma^2=(1,1)$.

**E-step.** Equal priors and variances, so $\gamma_{i1}=\frac{e^{-(x_i-0)^2/2}}{e^{-(x_i-0)^2/2}+e^{-(x_i-4)^2/2}}$:
- $x=0$: $\frac{1}{1+e^{-8}}\approx1.00$
- $x=2$: both exponents equal ($e^{-2}$), so $\gamma=0.5$
- $x=4$: $\approx0.00$

**M-step for component 1.** $N_1\approx1+0.5+0=1.5$.
- $\mu_1=\frac{1\cdot0+0.5\cdot2+0\cdot4}{1.5}\approx0.67$
- $\sigma_1^2=\frac{1\cdot(0-0.67)^2+0.5\cdot(2-0.67)^2}{1.5}=\frac{0.44+0.89}{1.5}\approx0.89$
- $\pi_1=1.5/3=0.5$

The point at 2 pulled the first mean toward it by half a point's worth. By symmetry $\mu_2\approx3.33$.

## Practical
- Local optima: multiple restarts, init with k-means ([[Clustering]]).
- Singularities when a component collapses on one point: regularize $\Sigma$.
- Choose $K$ with BIC ([[Cross-Validation and Model Selection]]).
- k-means = GMM with equal spherical covariances and hard assignments.

Why each matters:
- **Local optima.** The likelihood surface has many peaks (at least the $K!$ relabelings of every solution, plus genuinely different ones). Run EM from several starts and keep the highest likelihood; starting from k-means centres is a cheap, good initialisation.
- **Singularities.** If one component sits exactly on one data point and its variance shrinks to 0, $\mathcal N(x_i\mid x_i,\sigma^2)\propto1/\sigma^d\to\infty$, so the likelihood is **unbounded**: the global "maximum" is a useless spike. Fix by adding a small ridge to the diagonal of every $\Sigma_k$ (`reg_covar` in scikit-learn), using a prior (MAP-EM), or restarting collapsed components.
- **Choosing $K$ with BIC.** $\text{BIC}=-2\log L+p\ln N$, lower is better. The likelihood always rises with more components, and the $p\ln N$ term pays for it. For full covariances in $d$ dimensions,
  $$p=\underbrace{(K-1)}_{\pi}+\underbrace{Kd}_{\mu}+\underbrace{K\tfrac{d(d+1)}{2}}_{\Sigma}.$$
- **Covariance types** trade flexibility for parameters: *full* ($Kd(d+1)/2$ covariance parameters, any ellipse), *tied* (one shared full $\Sigma$), *diag* ($Kd$, axis-aligned ellipses), *spherical* ($K$, circles). With little data or large $d$, prefer the simpler ones.
- **k-means as a special case.** Fix $\Sigma_k=\sigma^2I$ and equal $\pi_k$, and let $\sigma\to0$: the responsibilities become 0/1 (nearest mean wins) and the M-step mean is the cluster average. That is Lloyd's algorithm. Consequently GMM handles **stretched, tilted clusters** that k-means cuts in the wrong place.

## Common confusions
- *"EM finds the maximum-likelihood estimate."* → It finds a local maximum; the global supremum may even be an infinite singular spike.
- *"Responsibilities are the cluster labels."* → They are posterior probabilities; take $\arg\max_k\gamma_{ik}$ only if you need a hard label.
- *"The likelihood went up, so adding a component was right."* → Likelihood always goes up with more parameters; use BIC or held-out likelihood.
- *"EM is only for Gaussian mixtures."* → It is a general recipe for any latent-variable model (HMMs, missing data, probabilistic PCA); GMM is the classic example.
- *"$\pi_k$ is a free parameter like a weight in regression."* → It is a probability vector; the constraint $\sum\pi_k=1$ is why its update is simply $N_k/N$.

## Check yourself

> [!question]- Why does the GMM likelihood have no closed-form maximiser?
> The log sits outside a sum over components, so the stationarity equations for each component depend on all the others through the responsibilities. Only when the component of each point is known does the problem split into independent Gaussian fits.

> [!question]- A point is equally far from two components with equal $\pi$ and equal $\Sigma$. What are its responsibilities?
> 0.5 and 0.5: the numerators are identical.

> [!question]- How many parameters does a full-covariance GMM with $K=3$, $d=2$ have?
> $(3-1)+3\cdot2+3\cdot3=2+6+9=17$.

> [!question]- Why can't the log-likelihood go down during EM?
> The E-step makes the ELBO equal to the log-likelihood at the current parameters; the M-step can only raise the ELBO, and the log-likelihood is always at least the ELBO.

> [!question]- During EM one component's variance heads to zero. What is happening and what do you do?
> It is collapsing onto a single point, sending the likelihood to infinity. Add a covariance regulariser, use a prior, or reinitialise that component; also try other restarts.

## Practice
[Gaussian Mixture Models and EM - Exercises](Gaussian%20Mixture%20Models%20and%20EM%20-%20Exercises.ipynb): E- and M-steps by hand, deriving the mean update, why EM is monotone, a stable log-space E-step, full EM from scratch, collapse, BIC and covariance types.

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 9
- [Mathematics for ML (free)](https://mml-book.github.io/) ch. 11
- [scikit-learn – GMMs](https://scikit-learn.org/stable/modules/mixture.html)
- [StatQuest videos](https://statquest.org/video_index.html): Gaussian distributions and clustering basics.
