---
tags: [ml, probabilistic, bayesian]
---
# Bayesian Inference

> [!summary] In one sentence
> Treat the unknown parameters $\theta$ as random variables, start with a **prior** belief, and use Bayes' rule to turn data into a **posterior** distribution, so every prediction carries honest uncertainty instead of a single "best guess".

## Intuition first

Imagine you find a coin on the street and want to know its bias $\theta = P(\text{heads})$. A frequentist "point estimate" approach flips it 3 times, sees 3 heads, and says "$\hat\theta = 1$, this coin always lands heads". That is obviously overconfident.

The Bayesian approach keeps a whole **distribution of beliefs** over $\theta$:

- **Before any data** you hold a *prior*: "most coins are roughly fair, but I'm not sure".
- **Each flip** re-weights every candidate value of $\theta$ by how well it explains what you just saw (the *likelihood*).
- **After the data** you hold a *posterior*: a sharper belief that still remembers how uncertain you are.

Think of it as a detective updating a list of suspects. Each clue does not name the culprit outright; it just makes some suspects more plausible and others less. With few clues the list stays wide; with many clues it narrows to one.

What problem does this solve?
1. **Small data**: the prior stops you from wild conclusions after 3 flips.
2. **Uncertainty**: you get error bars on everything (parameters *and* predictions) for free.
3. **Model choice**: the same machinery tells you which model the data prefer, with a built-in penalty for complexity.

![Beta posterior narrowing as coin flips arrive](../../Attachments/ML%20Animations/Bayesian%20Inference%20-%20Beta%20posterior%20updating.gif)

*Watch the curve: it starts flat (any bias is plausible), lurches after each flip, and after 100 flips becomes a narrow spike near the true value 0.7.*

## The math, step by step

### Bayes' rule

$$\underbrace{p(\theta\mid D)}_{\text{posterior}}=\frac{\overbrace{p(D\mid\theta)}^{\text{likelihood}}\ \overbrace{p(\theta)}^{\text{prior}}}{\underbrace{p(D)}_{\text{evidence}}}$$

- $\theta$: the unknown parameters (coin bias, regression weights, ...).
- $D$: the observed data.
- **Prior** $p(\theta)$: what you believe before seeing $D$.
- **Likelihood** $p(D\mid\theta)$: how probable the data are *if* $\theta$ were the truth. As a function of $\theta$ it is *not* a distribution (it need not integrate to 1).
- **Evidence** (marginal likelihood) $p(D)=\int p(D\mid\theta)p(\theta)\,d\theta$: a single number that normalises the posterior. It does not depend on $\theta$, which is why people often write $p(\theta\mid D)\propto p(D\mid\theta)\,p(\theta)$.
- **Posterior** $p(\theta\mid D)$: your updated belief.

In words: *posterior is proportional to likelihood times prior.* The evidence is the hard part (an integral over all $\theta$), and it is the reason we sometimes need approximate methods.

### Point summaries of the posterior

- **MAP** (maximum a posteriori): $\hat\theta_{\text{MAP}}=\arg\max_\theta p(D\mid\theta)p(\theta)$. With a flat prior it equals the MLE.
- **Posterior mean** $\mathbb E[\theta\mid D]$: minimises expected squared error.
- **Credible interval**: a range that contains $\theta$ with, say, 95% posterior probability. Two common choices: *equal-tailed* (cut 2.5% from each tail) and the *HDI* (highest-density interval, the narrowest such range). They coincide for symmetric posteriors and differ for skewed ones.

### The posterior predictive

- **Predictive**: $p(y_*\mid x_*,D)=\int p(y_*\mid x_*,\theta)p(\theta\mid D)d\theta$ — averages over uncertainty instead of a point estimate.

In words: ask *every* plausible $\theta$ what it predicts and take a vote weighted by posterior probability. The **plug-in** alternative $p(y_*\mid x_*,\hat\theta)$ uses one $\theta$ and ignores parameter uncertainty, so it is overconfident, especially far from the data or with little data.

### Conjugate priors: closed-form updates

- **Conjugate priors** give closed forms: Beta–Bernoulli, Dirichlet–Multinomial, Gaussian–Gaussian.

"Conjugate" means the posterior is in the same family as the prior, so updating is just changing a few numbers.

**Beta–Bernoulli.** Prior $\theta\sim\text{Beta}(a,b)$, observe $h$ heads and $t$ tails:
$$\theta\mid D\sim\text{Beta}(a+h,\ b+t).$$
The prior acts like $a$ "imaginary heads" and $b$ "imaginary tails" (pseudo-counts). Posterior mean $\frac{a+h}{a+b+h+t}$, mode $\frac{a+h-1}{a+b+h+t-2}$. The predictive probability that the next toss is heads equals the posterior mean, $\frac{a+h}{a+b+n}$ with $n=h+t$. For two future heads in a row, $P(HH\mid D)=\frac{(a+h)(a+h+1)}{(a+b+n)(a+b+n+1)}$ (not just the square of the single-toss probability, because the tosses share the uncertain $\theta$).

**Dirichlet–Multinomial.** Prior $\boldsymbol\pi\sim\text{Dir}(\alpha_1,\dots,\alpha_K)$, observe counts $n_k$: posterior $\text{Dir}(\alpha_k+n_k)$, predictive $P(\text{next}=k)=\frac{\alpha_k+n_k}{\sum_j\alpha_j+N}$. With all $\alpha_k=1$ this is exactly **add-one (Laplace) smoothing**, as used in [[Naive Bayes]].

**Gaussian–Gaussian** (unknown mean, known variance $\sigma^2$). Prior $\mu\sim\mathcal N(\mu_0,\tau_0^2)$, $n$ observations with mean $\bar x$:
$$\frac1{\tau_n^2}=\frac1{\tau_0^2}+\frac n{\sigma^2},\qquad \mu_n=\tau_n^2\left(\frac{\mu_0}{\tau_0^2}+\frac{n\bar x}{\sigma^2}\right).$$
Precisions (inverse variances) **add**, and the posterior mean is a **precision-weighted average** of prior mean and data mean. More data ⇒ the data term dominates.

### Bayesian linear regression

- **Bayesian linear regression**: prior $w\sim\mathcal N(0,\alpha^{-1}I)$ ⇒ Gaussian posterior; MAP = ridge ([[Linear Regression]]).

With features $\Phi$, targets $y$, and Gaussian noise of precision $\beta$:
$$p(w\mid D)=\mathcal N(m_N,S_N),\quad S_N^{-1}=\alpha I+\beta\Phi^\top\Phi,\quad m_N=\beta S_N\Phi^\top y.$$
Why MAP = ridge: $-\log p(w\mid D)=\frac\beta2\lVert y-\Phi w\rVert^2+\frac\alpha2\lVert w\rVert^2+\text{const}$, which is the ridge objective with $\lambda=\alpha/\beta$. The prior *is* the regulariser.

The predictive for a new input is also Gaussian, with variance
$$\sigma_*^2(x)=\underbrace{1/\beta}_{\text{noise}}+\underbrace{\phi(x)^\top S_N\phi(x)}_{\text{parameter uncertainty}},$$
and the second term **grows as you move away from the training data**: the model knows where it hasn't looked.

### Model comparison

- **Model comparison** via evidence $p(D\mid M)$ (automatic Occam's razor).

The **Bayes factor** $\frac{p(D\mid M_1)}{p(D\mid M_2)}$ compares two models. Why "automatic Occam's razor"? The evidence is a probability distribution over *all possible datasets*, so it must sum to 1. A very flexible model spreads its probability over many datasets and gives each one a little; a simple model concentrates on few. If the simple model can explain the data, it wins, even though the complex model could fit at least as well with its best parameters. The same idea picks a polynomial degree: evidence rises as the degree becomes adequate and then falls as extra flexibility is "wasted".

## Worked example

**Coin.** Prior $\text{Beta}(1,1)$ (uniform). Observe the 10 flips in the animation: 7 heads, 3 tails.
- Posterior: $\text{Beta}(1+7,\,1+3)=\text{Beta}(8,4)$.
- Posterior mean $8/12\approx0.667$; mode (MAP) $7/10=0.7$, equal to the MLE because the prior is flat.
- Predictive $P(\text{next}=H)=0.667$, slightly pulled toward 0.5 compared with the plug-in 0.7.

**Is it fair? (Bayes factor).** $M_0$: $\theta=0.5$ exactly. $M_1$: $\theta\sim\text{Beta}(1,1)$.
- $p(D\mid M_0)=0.5^{10}=1/1024\approx0.00098$.
- $p(D\mid M_1)=\int\theta^7(1-\theta)^3d\theta=B(8,4)=\frac{7!\,3!}{11!}=1/1320\approx0.00076$.
- Bayes factor $\frac{1320}{1024}\approx1.29$ in favour of the *fair* coin. 7 out of 10 is not surprising enough to justify the extra freedom of $M_1$: Occam at work.

**A positive test.** A disease has prevalence 1%, the test has 99% sensitivity and a 5% false-positive rate.
$$P(\text{ill}\mid +)=\frac{0.99\cdot0.01}{0.99\cdot0.01+0.05\cdot0.99}=\frac{0.0099}{0.0594}\approx0.17.$$
The prior (rarity) matters enormously: a positive result still leaves you probably healthy.

## When the posterior has no closed form

- Intractable posteriors ⇒ [[Variational Inference]] or [[MCMC]].

Outside conjugate pairs the evidence integral cannot be done analytically. Options:
- **Grid approximation**: evaluate prior × likelihood on a grid of $\theta$ values and normalise by the sum. Exact enough in 1–2 dimensions, hopeless in 10+.
- **[[MCMC]]**: draw samples from the posterior; slow but asymptotically exact.
- **[[Variational Inference]]**: fit a simple distribution to the posterior by optimisation; fast but approximate.
- **Laplace approximation**: a Gaussian centred at the MAP.

- Non-parametric: [[Gaussian Processes]] put a prior directly on *functions* rather than on a finite weight vector.

Foundations: [[Probability for ML]].

## Common confusions

- **"The likelihood is the probability of $\theta$."** → No: $p(D\mid\theta)$ is the probability of the *data* for a fixed $\theta$. Only after multiplying by the prior and normalising do you get a distribution over $\theta$.
- **"Bayesian = MAP."** → MAP is still a point estimate. Being Bayesian means using the *whole* posterior, e.g. in the predictive integral.
- **"The prior is cheating / subjective, so results are arbitrary."** → Its influence shrinks as data grow (see the animation: 100 flips swamp the flat prior). And every regulariser is already an implicit prior.
- **"A 95% credible interval is the same as a 95% confidence interval."** → A credible interval says "θ is in here with 95% probability, given the data". A confidence interval is a statement about the procedure over repeated experiments.
- **"Higher likelihood at the best fit ⇒ better model."** → Model comparison uses the evidence, which averages over the prior and so penalises flexibility.

## Check yourself

> [!question]- Name the four terms of Bayes' rule and which one does not depend on $\theta$.
> Posterior $p(\theta\mid D)$, likelihood $p(D\mid\theta)$, prior $p(\theta)$, evidence $p(D)$. The evidence does not depend on $\theta$; it only normalises.

> [!question]- Prior Beta(2, 2), then you see 3 heads and 1 tail. What is the posterior and the predictive probability of heads?
> Beta(5, 3). Predictive $=5/8=0.625$.

> [!question]- Why does the posterior predictive give wider error bars than the plug-in predictive?
> It integrates over parameter uncertainty, adding the term $\phi^\top S_N\phi$ (in linear regression) on top of the noise variance. The plug-in ignores it.

> [!question]- Which prior on the weights makes the MAP estimate equal to ridge regression, and what is $\lambda$?
> $w\sim\mathcal N(0,\alpha^{-1}I)$ with Gaussian noise of precision $\beta$; then $\lambda=\alpha/\beta$.

> [!question]- Why can a complex model have *lower* evidence than a simple model that fits worse?
> The evidence must spread unit probability mass over all datasets the model could generate. A flexible model spreads it thinly, so it assigns less probability to the particular dataset observed.

## Practice

[Bayesian Inference - Exercises](Bayesian%20Inference%20-%20Exercises.ipynb): Bayes' terms, plug-in vs predictive, Beta–Bernoulli and Gaussian–Gaussian by hand, Dirichlet smoothing, MAP = ridge, a Bayes factor, grid posteriors, credible intervals vs HDI, Bayesian linear regression and evidence-based degree selection.

## Learn more
- [Murphy – Probabilistic ML (free)](https://probml.github.io/pml-book/)
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 2–3
- [Statistical Rethinking 2024](https://github.com/rmcelreath/stat_rethinking_2024)
- [3Blue1Brown – Bayes theorem, the geometry of changing beliefs](https://www.youtube.com/watch?v=HZGCoVF3YvM)
