---
tags: [ml, math, probability]
---
# Probability for ML

> [!summary] In one sentence
> Probability is the bookkeeping of uncertainty: two rules (sum and product) give you Bayes' theorem, and fitting a model is just choosing parameters that make the observed data probable (MLE), optionally tempered by prior beliefs (MAP), which is where familiar losses and regularizers come from.

## Intuition first

Every ML model is uncertain about something: which class an email belongs to, what tomorrow's price will be, what the "true" weights are. Probability gives a consistent way to represent that uncertainty and update it when data arrives.

An everyday analogy: you think a coin is probably fair. You flip it 20 times and get 15 heads. You do not throw away your belief, and you do not ignore the data either: you **update**. Your belief shifts toward "biased to heads", and the more flips you see, the more confident (narrower) your belief becomes. That update is Bayes' theorem, and the animation below is exactly this story.

**What problem does it solve?**
- It explains *why* we use the losses we use: squared error is what you get from assuming Gaussian noise; cross-entropy from assuming Bernoulli/categorical labels.
- It explains regularization: an L2 penalty is a Gaussian prior belief that weights are small.
- It gives guarantees: the law of large numbers and concentration bounds say when an average over a finite sample (your test accuracy!) can be trusted.

![Sequential Bayesian updating of a coin's bias](../../Attachments/ML%20Animations/Probability%20for%20ML%20-%20Bayesian%20updating.gif)
*Watch the posterior over the coin's bias $\theta$: it starts flat (Beta(1,1)), jumps around after the first few flips, then settles and narrows around $\approx0.73$ as heads and tails accumulate. More data means less uncertainty.*

## The math, step by step

### Rules
- **Sum rule** (marginalization): $p(x)=\sum_y p(x,y)$. To forget about $y$, add up over all its values (integrate for continuous $y$).
- **Product rule**: $p(x,y)=p(y\mid x)p(x)$. The chance of both = chance of $x$ times chance of $y$ given $x$.
- **Bayes**: apply the product rule both ways ($p(\theta,D)=p(D\mid\theta)p(\theta)=p(\theta\mid D)p(D)$) and divide:
$$p(\theta\mid D)=\frac{p(D\mid\theta)\,p(\theta)}{p(D)}\qquad\text{posterior}=\frac{\text{likelihood}\times\text{prior}}{\text{evidence}}.$$
  $p(D)=\sum_\theta p(D\mid\theta)p(\theta)$ (sum rule) just normalizes. → [[Bayesian Inference]]
- **Independence**: $p(x,y)=p(x)p(y)$, i.e. knowing $x$ tells you nothing about $y$. **Conditional independence** $x\perp y\mid z$: $p(x,y\mid z)=p(x\mid z)p(y\mid z)$. The two are different: two symptoms are dependent (both signal the disease) but can be independent *given* the disease. Conditional independence underlies [[Naive Bayes]] (features independent given the class) and [[Probabilistic Graphical Models]] (the graph encodes which conditional independences hold).

### Moments
- **Expectation** $\mathbb E[X]=\sum_x x\,p(x)$: the long-run average.
- **Variance** $\mathrm{Var}(X)=\mathbb E[(X-\mathbb E X)^2]=\mathbb E[X^2]-\mathbb E[X]^2$: average squared distance from the mean.
- **Covariance** $\mathrm{Cov}(X,Y)=\mathbb E[XY]-\mathbb E[X]\mathbb E[Y]$: do $X$ and $Y$ move together? Independent ⇒ covariance 0 (the converse is false).
- **Linearity of expectation always holds**: $\mathbb E[aX+bY]=a\,\mathbb E[X]+b\,\mathbb E[Y]$, even when $X,Y$ are dependent. Variance is *not* linear: $\mathrm{Var}(aX+bY)=a^2\mathrm{Var}X+b^2\mathrm{Var}Y+2ab\,\mathrm{Cov}(X,Y)$. In vector form, $\mathrm{Cov}(Ax)=A\Sigma A^\top$.

### Key distributions
| Name | Use |
|---|---|
| Bernoulli / Binomial | binary outcomes, coin flips |
| Categorical / Multinomial | class labels, word counts |
| Gaussian $\mathcal N(\mu,\Sigma)$ | continuous noise, [[Gaussian Processes]] |
| Beta / Dirichlet | priors over probabilities (conjugate) |
| Poisson | counts |
| Exponential family | unifying form; GLMs |

Notes on the table:
- Bernoulli: $p(x\mid\theta)=\theta^x(1-\theta)^{1-x}$; Binomial counts heads in $n$ Bernoulli flips. Categorical/Multinomial are the $K$-class versions.
- Multivariate Gaussian: $\log p(x)=-\tfrac12(x-\mu)^\top\Sigma^{-1}(x-\mu)-\tfrac12\log|\Sigma|-\tfrac d2\log2\pi$. To sample with covariance $\Sigma$: factor $\Sigma=LL^\top$ (Cholesky), draw $z\sim\mathcal N(0,I)$, return $\mu+Lz$ (because $\mathrm{Cov}(Lz)=LL^\top$).
- **Conjugate** prior: posterior is in the same family as the prior. Beta prior + Bernoulli likelihood → Beta posterior: Beta($\alpha,\beta$) after $h$ heads and $t$ tails becomes Beta($\alpha+h,\beta+t$). Updating is just counting, which is why the animation is so simple. Dirichlet plays the same role for categorical data.
- Exponential family: $p(x\mid\eta)=h(x)\exp(\eta^\top T(x)-A(\eta))$. Bernoulli, Gaussian, Poisson, … all fit; GLMs (linear/logistic/Poisson regression) are "linear model for $\eta$".

### Estimation
- **MLE**: $\hat\theta=\arg\max\sum\log p(x_i\mid\theta)$: the parameters under which the observed data are most probable. We maximize the *log* because products of many small probabilities underflow, and logs turn products into sums.
  - Gaussian → least squares: if $y=w^\top x+\varepsilon$ with $\varepsilon\sim\mathcal N(0,\sigma^2)$, then $-\log p(y\mid x,w)=\frac1{2\sigma^2}(y-w^\top x)^2+\text{const}$, so maximizing likelihood = minimizing squared error.
  - Bernoulli → cross-entropy: $-\log p(y\mid\hat p)=-[y\log\hat p+(1-y)\log(1-\hat p)]$ ([[Information Theory]]).
  - Gaussian MLE of the variance, $\frac1n\sum(x_i-\bar x)^2$, is **biased**: its expectation is $\frac{n-1}n\sigma^2$, which is why the sample variance divides by $n-1$.
- **MAP**: MLE + log prior, $\hat\theta=\arg\max\big[\sum\log p(x_i\mid\theta)+\log p(\theta)\big]$. Gaussian prior ⇒ L2, Laplace ⇒ L1 ([[Overfitting and Regularization]]). Concretely, $w\sim\mathcal N(0,\tau^2I)$ adds $\frac1{2\tau^2}\lVert w\rVert^2$ to the loss (ridge with $\lambda=\sigma^2/\tau^2$); a Laplace prior $p(w)\propto e^{-|w|/b}$ adds $\frac1b\lVert w\rVert_1$ (Lasso).
- **Full Bayes** keeps the whole posterior instead of a point: e.g. the posterior mean, plus a measure of uncertainty.

### Limits
- **Law of large numbers**: the sample mean $\bar X_n\to\mathbb E[X]$ as $n\to\infty$. Why Monte Carlo and empirical risk work.
- **CLT**: for i.i.d. $X_i$ with variance $\sigma^2$, $\bar X_n$ is approximately $\mathcal N(\mu,\sigma^2/n)$, whatever the original distribution. Error bars shrink like $1/\sqrt n$.
- **Hoeffding bound** (used in PAC arguments): for i.i.d. $X_i\in[0,1]$, $P(|\bar X_n-\mu|\ge\varepsilon)\le2e^{-2n\varepsilon^2}$. Solving for $n$: to be within $\varepsilon$ with probability $\ge1-\delta$ you need $n\ge\frac{\ln(2/\delta)}{2\varepsilon^2}$. Unlike the CLT it is exact for every $n$, not just asymptotic.

See [[Information Theory]].

### Sampling
- **Inverse CDF**: draw $u\sim\text{Uniform}(0,1)$ and return the first category whose cumulative probability exceeds $u$ (`np.searchsorted(np.cumsum(p), u)`). Works for any distribution whose CDF you can invert.

## Worked example

**Bayes and the base-rate fallacy.** A disease has prevalence 1%. A test detects it 99% of the time and gives a false positive 5% of the time. You test positive. Probability you are ill?
1. $p(+)=0.99\cdot0.01+0.05\cdot0.99=0.0099+0.0495=0.0594$ (sum rule).
2. $p(D\mid+)=\frac{0.0099}{0.0594}\approx0.17$. Only 17%: the healthy population is so much larger that its false positives outnumber the true positives.

**Coin: MLE vs MAP vs posterior mean.** Data: 3 heads, 1 tail. Prior Beta(2,2) (mild belief in fairness).
1. MLE: $\hat\theta=3/4=0.75$.
2. Posterior: Beta($2+3,2+1$) = Beta(5,3).
3. MAP (mode): $\frac{5-1}{5+3-2}=\frac46\approx0.67$. Posterior mean: $\frac5{8}=0.625$. The prior pulls the estimate toward 0.5; with more data the pull fades.

**Hoeffding.** To estimate an accuracy within $\varepsilon=0.05$ with 95% confidence ($\delta=0.05$): $n\ge\frac{\ln40}{2\cdot0.0025}\approx\frac{3.69}{0.005}\approx738$ test examples.

## Common confusions
- **$p(A\mid B)=p(B\mid A)$.** → Not in general: Bayes multiplies by $p(A)/p(B)$. Confusing them is the base-rate fallacy.
- **"Uncorrelated means independent."** → Zero covariance only rules out *linear* dependence. $X\sim\mathcal N(0,1)$, $Y=X^2$ are uncorrelated but completely dependent.
- **"Independent implies conditionally independent (or vice versa)."** → Neither direction holds. Two independent causes of an alarm become dependent once you observe the alarm ("explaining away").
- **"A likelihood is a probability distribution over $\theta$."** → $p(D\mid\theta)$ as a function of $\theta$ does not integrate to 1; only after multiplying by a prior and normalizing do you get a distribution over $\theta$.
- **"MAP is Bayesian, so it captures uncertainty."** → MAP is still a single point. It only differs from MLE by the regularizer.

## Check yourself

> [!question]- Why does the posterior in the animation get narrower with every flip?
> Beta($\alpha,\beta$) has variance $\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$, which shrinks roughly like $1/n$ as counts grow. Each observation adds evidence, so fewer values of $\theta$ remain plausible.

> [!question]- Compute $\mathrm{Var}(X-Y)$ if $\mathrm{Var}X=4$, $\mathrm{Var}Y=1$, $\mathrm{Cov}(X,Y)=1$.
> $4+1-2\cdot1=3$. (Use $a=1,b=-1$ in the formula.)

> [!question]- Which prior gives L1 regularization, and why does L1 give sparse weights?
> A Laplace prior. Its density has a sharp peak at 0, so the MAP solution often sits exactly at 0 for weakly useful features; geometrically, the L1 ball has corners on the axes.

> [!question]- What does the CLT say about a classifier's accuracy measured on $n$ test points?
> Each prediction is a Bernoulli($a$) variable, so the measured accuracy is approximately $\mathcal N(a,\,a(1-a)/n)$. With $a=0.9$, $n=1000$ the standard error is about $0.0095$.

> [!question]- Is the MLE of a Gaussian's variance unbiased?
> No: $\mathbb E[\frac1n\sum(x_i-\bar x)^2]=\frac{n-1}n\sigma^2$. Using $\bar x$ instead of the true $\mu$ makes the spread look slightly too small; dividing by $n-1$ fixes it.

## Practice
[Probability for ML - Exercises](Probability%20for%20ML%20-%20Exercises.ipynb): sum/product rules on joint tables, base rates, moments, Bernoulli MLE/MAP/posterior mean, Gaussian MLE bias, Hoeffding sample sizes, and simulations (inverse-CDF sampling, CLT, multivariate Gaussian density and sampling, sequential Bayesian updating).

## Learn more
- [Mathematics for ML (free)](https://mml-book.github.io/) ch. 6
- [Murphy – Probabilistic ML (free)](https://probml.github.io/pml-book/)
- [StatQuest videos](https://statquest.org/video_index.html): short, clear videos on MLE, Bayes, the CLT and distributions.
- [Seeing Theory (Brown University)](https://seeing-theory.brown.edu/): interactive visualizations of probability, Bayesian inference and the CLT.
