---
tags: [ml, supervised, probabilistic, kernels]
status: not-started
notebook: not-started
level:
reviewed:
---
# Gaussian Processes

> [!summary] In one sentence
> A Gaussian process is a distribution over functions: $f\sim\mathcal{GP}(m,k)$, any finite set of outputs is jointly Gaussian with covariance from a kernel ([[Kernel Methods]]); conditioning on observed data gives a posterior that predicts a mean *and* an honest error bar at every input.

## Intuition first

Most regression models pick **one** function. A GP keeps track of **all plausible functions at once**, weighted by how believable they are.

Before seeing data, you state a belief about what functions look like: "smooth, wiggling on a length scale of about 1, values usually between −2 and 2". That is the **prior**, and you can draw random functions from it like drawing random numbers from a bell curve. Then each observation acts like a pin: every function that does not pass (near) the pin is thrown away. What survives is the **posterior**. Where many pins are close together, the surviving functions all agree, so uncertainty is small; far from any pin, they fan out again, and uncertainty grows back to the prior's level.

The kernel is the heart of it: $k(x,x')$ says how strongly $f(x)$ and $f(x')$ are correlated. With an RBF kernel, nearby inputs have strongly correlated outputs (smoothness), and far-apart inputs are nearly independent.

**What problem does it solve?** It gives predictions with **calibrated uncertainty** from small datasets, with very few knobs, all of which can be learned from the data. That makes it the tool of choice whenever you must decide *where to measure next*: [[Cross-Validation and Model Selection|hyperparameter tuning]] by Bayesian optimisation, experimental design, active learning, surrogate models of expensive simulations.

![GP prior samples collapsing onto the data as points are added](../../Attachments/ML%20Animations/Gaussian%20Processes%20-%20prior%20to%20posterior.gif)
*Watch the shaded $\pm2$ standard-deviation band pinch to almost nothing at each yellow observation and stay wide where there is no data; the three coloured sample functions are always plausible functions that pass through all observations so far.*

## The math, step by step

### What "a distribution over functions" means
$f\sim\mathcal{GP}(m,k)$ means: for *any* finite set of inputs $x_1,\dots,x_n$, the vector $(f(x_1),\dots,f(x_n))$ is multivariate Gaussian with
- mean $m(x_i)$ (the mean function, usually $0$ after centring $y$),
- covariance $\operatorname{Cov}(f(x_i),f(x_j))=k(x_i,x_j)$.

That is enough to define the process because we only ever evaluate a function at finitely many points. To **draw a sample** on a grid of inputs: build $K=k(X,X)$, take its Cholesky factor $K=LL^\top$ (add a tiny jitter like $10^{-8}I$ for numerical stability), draw $z\sim\mathcal N(0,I)$ and set $f=m+Lz$.

A common kernel with its hyperparameters:
$$k(x,x')=\sigma_f^2\exp\Big(-\frac{(x-x')^2}{2\ell^2}\Big).$$
- $\ell$ (length scale): how far you must move before $f$ changes appreciably. Small $\ell$ = wiggly functions; large $\ell$ = nearly flat or linear ones.
- $\sigma_f^2$ (signal variance): the typical squared amplitude of $f$ around its mean.
- plus the noise variance $\sigma^2$ of the observations $y=f(x)+\varepsilon$, $\varepsilon\sim\mathcal N(0,\sigma^2)$.

### Regression posterior
With noise $\sigma^2$ and $K=k(X,X)$:
$$\mu_*=k_*^\top(K+\sigma^2I)^{-1}y,\qquad \Sigma_*=k_{**}-k_*^\top(K+\sigma^2I)^{-1}k_*$$

Symbols: $X$ are the $N$ training inputs, $y$ their targets, $x_*$ a test input, $k_*=k(X,x_*)$ the vector of covariances between the training points and the test point, and $k_{**}=k(x_*,x_*)$ the prior variance at the test point.

**Where it comes from (Gaussian conditioning).** Under the prior, the noisy training targets and the test value are jointly Gaussian:
$$\begin{pmatrix}y\\f_*\end{pmatrix}\sim\mathcal N\left(0,\begin{pmatrix}K+\sigma^2I&k_*\\k_*^\top&k_{**}\end{pmatrix}\right).$$
For any jointly Gaussian $(a,b)$, $a\mid b\sim\mathcal N\big(\mu_a+\Sigma_{ab}\Sigma_{bb}^{-1}(b-\mu_b),\ \Sigma_{aa}-\Sigma_{ab}\Sigma_{bb}^{-1}\Sigma_{ba}\big)$. With $a=f_*$, $b=y$ this is exactly $\mu_*$ and $\Sigma_*$.

**Reading the formulas in words.**
- $\mu_*=\sum_i\alpha_ik(x_i,x_*)$ with $\alpha=(K+\sigma^2I)^{-1}y$: a weighted sum of kernel bumps centred on the training points, the same as kernel ridge regression with $\lambda=\sigma^2$ ([[Kernel Methods]]).
- $\Sigma_*$ = prior variance $k_{**}$ minus what the data explain. It does **not** depend on $y$, only on *where* you measured. Near data the subtraction is large (small variance); far away $k_*\approx0$, so $\Sigma_*\approx k_{**}$.
- $\Sigma_*$ is the variance of the latent $f_*$. A new noisy *observation* $y_*$ has predictive variance $\Sigma_*+\sigma^2$; use that for prediction intervals on data.
- With $\sigma^2=0$ (and $K$ invertible) the posterior interpolates: at a training input $\mu_*=y_i$ and $\Sigma_*=0$.

**How to compute it stably (Cholesky).** Never invert $K+\sigma^2I$ explicitly. Compute $L=\operatorname{chol}(K+\sigma^2I)$, $\alpha=L^\top\backslash(L\backslash y)$, then $\mu_*=k_*^\top\alpha$; with $v=L\backslash k_*$, $\Sigma_*=k_{**}-v^\top v$.

### Learning the hyperparameters
- Gives **uncertainty** along with predictions.
- Hyperparameters via maximizing the marginal likelihood.

The marginal likelihood is the probability of the observed $y$ with $f$ integrated out, $y\sim\mathcal N(0,K+\sigma^2I)$:
$$\log p(y\mid X)=-\tfrac12y^\top(K+\sigma^2I)^{-1}y-\tfrac12\log|K+\sigma^2I|-\tfrac N2\log2\pi.$$
- First term: **data fit** (large when the model explains $y$ with little "energy").
- Second term: **complexity penalty** (flexible kernels, e.g. tiny $\ell$, spread probability over many datasets, so $|K+\sigma^2I|$ is large).
- Third term: a constant.

Maximising it trades fit against complexity automatically (Occam's razor), so you can tune $\ell,\sigma_f^2,\sigma^2$ by gradient ascent without a validation set; with Cholesky, $\log|K+\sigma^2I|=2\sum_i\log L_{ii}$. It is non-convex, so restart from a few initial values.

### Cost
- Cost $O(N^3)$; sparse/inducing-point approximations.

The Cholesky factorisation of the $N\times N$ matrix costs $O(N^3)$ time and $O(N^2)$ memory, which limits exact GPs to roughly $10^4$ points. **Sparse GPs** summarise the data through $m\ll N$ *inducing points* (pseudo-inputs whose function values carry the information), reducing the cost to $O(Nm^2)$; you lose some accuracy and tend to over-smooth or under-estimate variance far from the inducing points.

### Applications and connections
- Used in Bayesian optimization of hyperparameters ([[Cross-Validation and Model Selection]]). Fit a GP to the (few, expensive) evaluations of validation score vs hyperparameters, then evaluate next where an **acquisition function** is largest, e.g. the upper confidence bound $a(x)=\mu(x)+\kappa\sigma(x)$ or expected improvement. Large $\mu$ = exploit; large $\sigma$ = explore.
- Bayesian linear regression with basis functions is a GP with a finite-rank kernel ([[Bayesian Inference]]). If $f(x)=w^\top\phi(x)$ with $w\sim\mathcal N(0,\alpha^{-1}I)$, then $f$ is Gaussian with mean 0 and $\operatorname{Cov}(f(x),f(x'))=\alpha^{-1}\phi(x)^\top\phi(x')$: a GP whose Gram matrices have rank at most $M=\dim\phi$. The GP view and the weight-space view give identical predictions; the RBF kernel corresponds to infinitely many basis functions.

## Worked example

Kernel $k(x,x')=\exp(-(x-x')^2/2)$ (so $\ell=1$, $\sigma_f^2=1$), noise $\sigma^2=0.25$, one observation $x_1=0$, $y_1=2$. Then $K+\sigma^2I=1.25$.

- At $x_*=0$: $k_*=1$. $\mu_*=\frac{1}{1.25}\cdot2=1.6$ (pulled towards 0 because the observation is noisy); $\Sigma_*=1-\frac{1}{1.25}=0.2$.
- At $x_*=1$: $k_*=e^{-0.5}\approx0.607$. $\mu_*=\frac{0.607}{1.25}\cdot2\approx0.97$; $\Sigma_*=1-\frac{0.368}{1.25}\approx0.71$.
- At $x_*=5$: $k_*=e^{-12.5}\approx0$. $\mu_*\approx0$, $\Sigma_*\approx1$: back to the prior, the observation says nothing this far away.

The predictive variance for a new noisy measurement at $x_*=0$ is $0.2+0.25=0.45$.

## Common confusions
- *"A GP is a neural-network-like model with weights."* → It is non-parametric: the "parameters" are the training data plus a few kernel hyperparameters, and the model grows with $N$.
- *"The band in the plot is where future data will lie."* → The $\mu_*\pm2\sqrt{\Sigma_*}$ band is for the latent $f$; data scatter more, by the noise $\sigma^2$.
- *"Posterior variance depends on the observed values."* → $\Sigma_*$ depends only on the input locations (and hyperparameters), not on $y$, for a fixed kernel.
- *"GPs are only for 1-D curves."* → Inputs can be any space you can put a kernel on (vectors, strings, graphs); 1-D is just easiest to draw.
- *"Maximising the marginal likelihood overfits like maximising training fit."* → The log-determinant term penalises complexity; it can still overfit with many hyperparameters, but far less than tuning to training error.

## Check yourself

> [!question]- What happens to prior samples and to the posterior when $\ell$ is very small? Very large?
> Very small: samples are rough and nearly independent between nearby points; the posterior mean spikes at each observation and returns to 0 between them (overfit). Very large: samples are almost flat/linear; the posterior is too smooth and misses structure (underfit).

> [!question]- Why does the posterior variance not depend on $y$?
> In Gaussian conditioning, the conditional covariance $\Sigma_{aa}-\Sigma_{ab}\Sigma_{bb}^{-1}\Sigma_{ba}$ involves only covariances, which come from the kernel evaluated at the inputs.

> [!question]- What is the GP posterior mean equivalent to?
> Kernel ridge regression with regularisation $\lambda=\sigma^2$: $\mu_*=k_*^\top(K+\sigma^2I)^{-1}y$.

> [!question]- Where does the $O(N^3)$ cost come from?
> Factorising (or inverting) the $N\times N$ matrix $K+\sigma^2I$, needed for the mean, the variance and the marginal likelihood.

> [!question]- In Bayesian optimisation with UCB, why does a large $\kappa$ explore more?
> It rewards high posterior standard deviation, so points in unexplored regions win even if their predicted mean is not the best.

## Practice
[Gaussian Processes - Exercises](Gaussian%20Processes%20-%20Exercises.ipynb): GPs as distributions over functions, reading hyperparameters, GP mean = kernel ridge, the cubic wall; by hand: prior correlations, posteriors from one and two observations, deriving the posterior by conditioning, noise-free interpolation, the log marginal likelihood, Bayesian linear regression as a GP; in code: sampling the prior, GP regression with Cholesky, computing the marginal likelihood, choosing the length scale, checking error-bar calibration, Bayesian optimisation with UCB, BLR = GP numerically.

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 6
- [scikit-learn – Gaussian processes](https://scikit-learn.org/stable/modules/gaussian_process.html)
- [Rasmussen & Williams – Gaussian Processes for Machine Learning (free book)](https://gaussianprocess.org/gpml/): the standard reference; ch. 2 covers everything in this note
- [distill.pub – A Visual Exploration of Gaussian Processes](https://distill.pub/2019/visual-exploration-gaussian-processes/): interactive prior/posterior and kernel playground
