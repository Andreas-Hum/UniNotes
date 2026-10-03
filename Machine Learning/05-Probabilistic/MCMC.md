---
tags: [ml, probabilistic, sampling]
status: not-started
notebook: not-started
level:
reviewed:
---
# MCMC

> [!summary] In one sentence
> Markov chain Monte Carlo builds a random walk whose long-run visiting frequencies equal the posterior, so you can draw samples from $p(\theta\mid D)$ (and average anything over them) even though you can only evaluate it up to an unknown constant.

## Intuition first

Draw samples from $p(\theta\mid D)\propto p(D\mid\theta)p(\theta)$ without knowing $Z$.

In [[Bayesian Inference]] the posterior is "likelihood × prior, divided by the evidence $Z=p(D)$". The numerator is easy to evaluate at any $\theta$; the denominator is an integral over every possible $\theta$ and usually impossible. MCMC sidesteps $Z$ completely.

**Analogy: a blindfolded hiker mapping a mountain range.** You cannot see the landscape, but at any spot you can measure the altitude $\tilde p(\theta)$ (the *unnormalised* density). The rules:
1. Propose a random step.
2. If the new spot is higher, go there.
3. If it is lower, go there only *sometimes*, with probability equal to the height ratio.

If you write down where you stand after every step, you spend most time on high ground and occasionally wander into valleys, in exactly the proportion that $\tilde p$ dictates. The list of positions *is* a sample from the posterior. And because only **ratios** of heights are ever used, the unknown normaliser $Z$ cancels.

![Random-walk Metropolis exploring a correlated Gaussian](../../Attachments/ML%20Animations/MCMC%20-%20Metropolis%20random%20walk.gif)

*Watch the chain start far away (burn-in), get accepted uphill, sometimes get rejected (red cross, it stays put), and gradually fill the ellipses in proportion to their density.*

## The math, step by step

### Why a Markov chain?

A Markov chain moves $\theta^{(t)}\to\theta^{(t+1)}$ with a transition kernel $T(\theta'\mid\theta)$. Under mild conditions (it can reach everywhere, does not cycle) it forgets where it started and converges to a unique **stationary distribution** $\pi$. We design $T$ so that $\pi$ is our posterior.

A sufficient condition is **detailed balance**:
$$\pi(\theta)\,T(\theta'\mid\theta)=\pi(\theta')\,T(\theta\mid\theta').$$
In words: in equilibrium, probability flow from $\theta$ to $\theta'$ equals the flow back. Summing both sides over $\theta$ gives $\sum_\theta\pi(\theta)T(\theta'\mid\theta)=\pi(\theta')$, i.e. $\pi$ is stationary.

### Metropolis–Hastings

Propose $\theta'\sim q(\theta'\mid\theta)$, then accept with
$$\alpha=\min\!\Big(1,\frac{\tilde p(\theta')q(\theta\mid\theta')}{\tilde p(\theta)q(\theta'\mid\theta)}\Big).$$
If rejected, the chain **stays** at $\theta$ and $\theta$ is recorded *again* (this repetition is essential, not a bug).

- $\tilde p$: unnormalised target, $\tilde p=Z\,p$. Since $\frac{\tilde p(\theta')}{\tilde p(\theta)}=\frac{Zp(\theta')}{Zp(\theta)}$, **$Z$ cancels**.
- $\frac{q(\theta\mid\theta')}{q(\theta'\mid\theta)}$: the **Hastings correction**. If the proposal prefers some directions, this undoes the bias. For a symmetric proposal (e.g. $\theta'=\theta+\varepsilon$, $\varepsilon\sim\mathcal N(0,s^2)$) it equals 1 and you get plain **Metropolis**: $\alpha=\min(1,\tilde p(\theta')/\tilde p(\theta))$.

*Why it satisfies detailed balance:* for $\theta\ne\theta'$, $\pi(\theta)q(\theta'\mid\theta)\alpha(\theta\to\theta')=\min\big(\pi(\theta)q(\theta'\mid\theta),\ \pi(\theta')q(\theta\mid\theta')\big)$, which is symmetric in $\theta,\theta'$.

**Step-size trade-off** (random-walk proposal scale $s$):
- $s$ too small: almost every step accepted, but the chain crawls; successive samples nearly identical.
- $s$ too large: proposals land in low-density regions and get rejected; the chain is stuck.
- Rule of thumb: aim for acceptance ≈ 0.44 in 1-D and ≈ 0.234 in high dimensions.

### The method zoo

| Method | Idea |
|---|---|
| **Metropolis–Hastings** | propose $\theta'\sim q$, accept with $\min\!\big(1,\frac{\tilde p(\theta')q(\theta\mid\theta')}{\tilde p(\theta)q(\theta'\mid\theta)}\big)$ |
| **Gibbs** | sample each variable from its conditional |
| **HMC / NUTS** | use gradients for long informed moves (Stan, PyMC) |
| Langevin dynamics | gradient + noise; links to diffusion models |
| Importance / rejection sampling | simple but poor in high dimensions |

**Gibbs sampling.** Cycle through the coordinates and draw each from its full conditional $p(\theta_i\mid\theta_{-i},D)$. It is MH with acceptance probability exactly 1. It shines when the conditionals are easy (conjugate models, [[Probabilistic Graphical Models]] where each variable only depends on its Markov blanket). Example: for a standard bivariate Gaussian with correlation $\rho$, $x_1\mid x_2\sim\mathcal N(\rho x_2,\,1-\rho^2)$ and symmetrically for $x_2$. When $\rho\to1$ the conditional variance $1-\rho^2$ shrinks, so Gibbs takes tiny axis-aligned steps along a thin diagonal ridge and mixes slowly.

**Hamiltonian Monte Carlo (HMC).** Treat $U(\theta)=-\log\tilde p(\theta)$ as a potential-energy landscape, add a random momentum $p\sim\mathcal N(0,I)$, and simulate a frictionless puck sliding over it with total energy $H(\theta,p)=U(\theta)+\tfrac12p^\top p$. The **leapfrog** integrator does
$$p\leftarrow p-\tfrac\varepsilon2\nabla U(\theta),\quad\theta\leftarrow\theta+\varepsilon p,\quad p\leftarrow p-\tfrac\varepsilon2\nabla U(\theta),$$
repeated $L$ times, then accepts with $\min(1,e^{H_{\text{old}}-H_{\text{new}}})$. Energy is almost conserved, so acceptance stays high while the move travels far: long, informed steps instead of a drunk walk. **NUTS** (No-U-Turn Sampler) picks $L$ automatically; it is the default in Stan and PyMC.

**Langevin dynamics.** $\theta\leftarrow\theta+\tfrac\varepsilon2\nabla\log p(\theta)+\sqrt\varepsilon\,\xi$, $\xi\sim\mathcal N(0,I)$: gradient ascent plus noise. The "score" $\nabla\log p$ is exactly what diffusion/score-based generative models learn, which is why they are linked.

**Not Markov chains, but related.**
- *Rejection sampling*: find $M$ with $Mq(\theta)\ge\tilde p(\theta)$ everywhere, draw $\theta\sim q$, keep it with probability $\tilde p(\theta)/(Mq(\theta))$. Exact independent samples, but $M$ explodes with dimension, so almost everything is rejected.
- *Importance sampling*: draw from $q$ and reweight, $\mathbb E_p[f]\approx\sum_iw_if(\theta_i)/\sum_iw_i$ with $w_i=\tilde p(\theta_i)/q(\theta_i)$. In high dimensions a single weight dominates and the estimate becomes noisy.

## Worked example

Target $\tilde p(\theta)=e^{-\theta^2/2}$ (a standard normal, constant ignored), symmetric proposal, current $\theta=1$.
- Proposal $\theta'=2$: $\alpha=\min(1,e^{-2}/e^{-0.5})=e^{-1.5}\approx0.22$. Draw $u\sim U(0,1)$; move only if $u<0.22$.
- Proposal $\theta'=0.5$: $\alpha=\min(1,e^{-0.125}/e^{-0.5})=\min(1,e^{0.375})=1$. Always move (uphill).

**Hastings correction.** Suppose the proposal from $\theta=1$ to $\theta'=2$ has $q(2\mid1)=0.6$ but the reverse has $q(1\mid2)=0.3$. Then $\alpha=\min\big(1,\,0.22\cdot\frac{0.3}{0.6}\big)=0.11$: the move is made less likely to compensate for the proposal being biased toward it.

## Diagnostics

Trace plots, effective sample size, $\hat R$ (≤ 1.01), burn-in, thinning.

- **Trace plot**: $\theta^{(t)}$ against $t$. Healthy = a "fuzzy caterpillar" with no trend. Long flat stretches mean many rejections; slow drifts mean poor mixing.
- **Burn-in (warm-up)**: discard the first part of the chain, before it reached the typical set (the trail from the corner in the animation).
- **Effective sample size (ESS)**: successive samples are correlated, so $N$ draws are worth fewer independent ones:
  $$\text{ESS}=\frac{N}{1+2\sum_{k\ge1}\rho_k},$$
  where $\rho_k$ is the lag-$k$ autocorrelation. For an AR(1)-like chain with $\rho_k=\rho^k$ this becomes $N\frac{1-\rho}{1+\rho}$; e.g. $\rho=0.9$ turns 10 000 draws into about 526.
- **$\hat R$ (Gelman–Rubin)**: run several chains from dispersed starts. With $W$ the mean within-chain variance and $B/n$ the variance of the chain means, $\hat V=\frac{n-1}{n}W+\frac Bn$ and $\hat R=\sqrt{\hat V/W}$. If chains agree, $\hat R\approx1$; require $\hat R\le1.01$.
- **Thinning**: keep every $k$-th sample. It saves memory but never increases ESS, so it is optional.

## MCMC vs the alternatives

Compared with [[Variational Inference]]: slower but asymptotically exact. VI turns inference into optimisation and is much faster on large data, but its answer is biased by the chosen family of distributions; MCMC's only error is Monte Carlo noise, which shrinks as you run longer. Context: [[Bayesian Inference]], [[Probabilistic Graphical Models]].

## Common confusions

- **"Rejected proposals are thrown away and the step is skipped."** → No: on rejection you record the *current* state again. Dropping it biases the sample toward low-density regions.
- **"High acceptance rate = good sampler."** → A tiny step size gives ~100% acceptance and terrible mixing. Look at ESS, not just acceptance.
- **"MCMC samples are independent."** → They are autocorrelated; that is why ESS < N.
- **"$\hat R\approx1$ proves convergence."** → It can only detect disagreement between chains; all chains could be stuck in the same mode.
- **"I need the normalised posterior."** → Only ratios of $\tilde p$ are used, so $Z$ is never needed.

## Check yourself

> [!question]- Why doesn't MH need the evidence $p(D)$?
> The acceptance probability uses the ratio $\tilde p(\theta')/\tilde p(\theta)$; the normaliser appears in numerator and denominator and cancels.

> [!question]- Target $\tilde p(\theta)=e^{-\theta^2/2}$, current $\theta=0$, symmetric proposal $\theta'=1$. Acceptance probability?
> $\min(1,e^{-1/2}/e^0)=e^{-0.5}\approx0.61$.

> [!question]- A trace plot shows long flat lines. What is wrong and how do you fix it?
> Most proposals are rejected: the step size is too large. Shrink it (or use HMC/NUTS).

> [!question]- An AR(1) chain has autocorrelation $\rho=0.5$ and 1000 draws. ESS?
> $1000\cdot\frac{0.5}{1.5}\approx333$.

> [!question]- Why does Gibbs sampling mix slowly on a strongly correlated Gaussian?
> Each update moves along one axis with conditional variance $1-\rho^2$, which is tiny when $|\rho|\approx1$, so the chain zig-zags in small steps along the diagonal.

## Practice

[MCMC - Exercises](MCMC%20-%20Exercises.ipynb): why the normaliser cancels, reading diagnostics, step-size trade-off, MH and Hastings by hand, detailed balance, Gibbs conditionals, ESS and $\hat R$ by hand, then random-walk Metropolis, Gibbs, rejection/importance sampling and HMC from scratch.

**Project:** [[Project - Bayesian AB Test with MCMC]] – a Bayesian A/B test with your own Metropolis sampler

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 11
- [PyMC docs](https://www.pymc.io/)
- [Statistical Rethinking 2024](https://github.com/rmcelreath/stat_rethinking_2024)
- [Chi Feng – interactive MCMC demos](https://chi-feng.github.io/mcmc-demo/) (watch random-walk MH, Gibbs, HMC and NUTS side by side)
