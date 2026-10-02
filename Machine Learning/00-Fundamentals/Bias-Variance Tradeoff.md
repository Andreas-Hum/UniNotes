---
tags: [ml, fundamentals, theory]
---
# Bias-Variance Tradeoff

> [!summary] In one sentence
> The expected test error of a model splits into **bias²** (how wrong it is on average), **variance** (how much it changes when trained on a different sample), and **irreducible noise**; making a model more flexible trades bias for variance.

## Intuition first

Imagine you could rerun history: collect a fresh training set, retrain, and record the prediction at one fixed input $x$. Do that many times and you get a cloud of predictions, like darts thrown at a board whose bull's-eye is the true value $f(x)$.

- **Bias** is how far the *centre* of the cloud is from the bull's-eye. A straight line fitted to a curve misses in the same direction every time, whatever sample you draw: systematic error.
- **Variance** is how *spread out* the cloud is. A wiggly degree-9 polynomial follows each sample's noise, so it lands somewhere different every time.
- **Noise** is the wobble in the targets themselves; even a perfect model cannot predict it.

Simple models: high bias, low variance. Flexible models: low bias, high variance. The best test error is usually in between, at the bottom of the famous U-shaped curve.

![Bias and variance as darts on a board](../../Attachments/ML%20Animations/Bias-Variance%20Tradeoff%20-%20dartboard.gif)
*Each yellow dart is one trained model; watch the red cross (the average dart): its distance to the bull's-eye is the bias, the spread of the darts is the variance.*

![Refitting simple and flexible models on many training sets](../../Attachments/ML%20Animations/Bias-Variance%20Tradeoff%20-%20refitting%20on%20many%20datasets.gif)
*Watch the thin yellow fits pile up: the lines all agree but miss the green sine (bias); the degree-9 curves hug it on average (red) but scatter a lot (variance).*

## The decomposition

For squared loss with $y = f(x) + \varepsilon$, $\mathrm{Var}(\varepsilon)=\sigma^2$, the expected test error at $x$ decomposes as

$$\mathbb{E}\big[(y-\hat f(x))^2\big] = \underbrace{\big(\mathbb{E}[\hat f(x)]-f(x)\big)^2}_{\text{bias}^2} + \underbrace{\mathbb{E}\big[(\hat f(x)-\mathbb{E}\hat f(x))^2\big]}_{\text{variance}} + \underbrace{\sigma^2}_{\text{irreducible}}$$

**Symbols.** $f$ is the true function, $\varepsilon$ zero-mean noise with variance $\sigma^2$, $\hat f$ the model trained on a random training set $\mathcal D$. The expectation is over **both** the random training set (which makes $\hat f$ random) and the noise in the new test target $y$.

## The math, step by step

Fix $x$ and write $\bar f = \mathbb{E}_{\mathcal D}[\hat f(x)]$ for the average prediction.

1. **Add and subtract** $f(x)$ and $\bar f$:
$$y - \hat f = \underbrace{\varepsilon}_{y - f} + \underbrace{(f - \bar f)}_{\text{bias part}} + \underbrace{(\bar f - \hat f)}_{\text{variance part}}.$$
2. **Square and take expectations.** The three squares give $\mathbb{E}[\varepsilon^2] = \sigma^2$, $(f - \bar f)^2$ (a constant), and $\mathbb{E}[(\bar f - \hat f)^2]$.
3. **The cross terms vanish.**
   - $\mathbb{E}[\varepsilon\,(f-\bar f)] = (f-\bar f)\,\mathbb{E}[\varepsilon] = 0$.
   - $\mathbb{E}[\varepsilon\,(\bar f - \hat f)] = \mathbb{E}[\varepsilon]\,\mathbb{E}[\bar f - \hat f] = 0$, because the test noise is independent of the training set.
   - $\mathbb{E}[(f-\bar f)(\bar f - \hat f)] = (f - \bar f)\,(\bar f - \mathbb{E}\hat f) = 0$ by definition of $\bar f$.
4. What remains is bias² + variance + $\sigma^2$. Averaging over $x$ gives the overall expected test MSE.

**Two classic examples.**
- **k-NN regression**: $\hat f(x_0) = \frac1k\sum_{\ell\in N_k(x_0)} y_\ell$. With the inputs fixed, $\mathrm{Var} = \frac{\sigma^2}{k}$ (average of $k$ independent noises), while $\text{bias} = f(x_0) - \frac1k\sum_\ell f(x_\ell)$ grows as $k$ pulls in farther neighbours. Small $k$: low bias, high variance; large $k$: the opposite.
- **1-D ridge** $y_i = w x_i + \varepsilon_i$, $\hat w = \frac{\sum x_i y_i}{S + \lambda}$ with $S = \sum x_i^2$: $\mathbb{E}\hat w = \frac{S}{S+\lambda}w$, so $\text{bias} = -\frac{\lambda}{S+\lambda}w$, and $\mathrm{Var}(\hat w) = \frac{\sigma^2 S}{(S+\lambda)^2}$. Increasing $\lambda$ raises the bias and lowers the variance.

**A biased estimator that wins.** Estimate a mean $\mu$ by $c\,\bar x$ from $n$ samples with variance $\sigma^2$. Its MSE is $(1-c)^2\mu^2 + c^2\sigma^2/n$. The unbiased choice $c = 1$ gives $\sigma^2/n$, but the optimum is $c^* = \frac{\mu^2}{\mu^2 + \sigma^2/n} < 1$. With $\mu = 1$, $\sigma^2/n = 1$: $c^* = 0.5$ and MSE $= 0.25 + 0.25 = 0.5$, half that of the unbiased estimator. Shrinkage (accepting a little bias) can buy a lot of variance reduction; ridge does exactly this.

**Bagging and correlation.** Averaging $B$ models, each with variance $\sigma^2$ and pairwise correlation $\rho$:
$$\mathrm{Var}\Big(\frac1B\sum_b \hat f_b\Big) = \rho\,\sigma^2 + \frac{1-\rho}{B}\,\sigma^2.$$
More models kill the second term, but the first remains, which is why random forests also decorrelate the trees (random feature subsets).

## Worked example

At a point $x_0$ the true value is $f(x_0) = 2.5$ and the noise variance is $\sigma^2 = 0.25$. Four training sets give predictions $2.0, 2.4, 1.6, 2.0$.

1. Average prediction: $\bar f = 8.0/4 = 2.0$.
2. Bias²: $(2.0 - 2.5)^2 = 0.25$.
3. Variance: $\frac14\big(0^2 + 0.4^2 + 0.4^2 + 0^2\big) = 0.08$.
4. Expected test error: $0.25 + 0.08 + 0.25 = 0.58$.

Bias dominates here, so a more flexible model or better features would help more than more data.

## Diagnosis and fixes

| | High bias | High variance |
|---|---|---|
| Symptom | train and val error both high | train error low, val error high |
| Cause | model too simple | model too flexible / too little data |
| Fix | richer model, more features | more data, [[Overfitting and Regularization\|regularization]], bagging ([[Ensemble Methods]]) |

**Which way do the knobs turn?**

| Knob | Bias | Variance |
|---|---|---|
| More flexible model (higher degree, deeper tree, smaller $k$ in k-NN) | ↓ | ↑ |
| Stronger regularization (larger $\lambda$) | ↑ | ↓ |
| More training data | ≈ unchanged | ↓ |
| Bagging | ≈ unchanged | ↓ |
| Boosting | ↓ | can ↑ |

**Learning curves** make the diagnosis visible: with high bias, train and validation error converge quickly to a high plateau (more data will not help); with high variance, there is a large gap that slowly closes as data grow.

**Irreducible error** is a floor: no model, however good, beats $\sigma^2$ on average. Reducing it requires better *inputs* (new measurements), not a better model.

> [!note] Modern caveat
> Over-parameterized deep nets show **double descent**: test error can fall again past the interpolation threshold.

What is happening: as the parameter count approaches the number of training points (the *interpolation threshold*), the model can just barely fit every point and is forced into a wild solution, so test error peaks. Beyond it, many interpolating solutions exist and training (e.g. gradient descent from small weights, or the minimum-norm least-squares solution) picks a smooth one, so test error can fall again. The classical U-curve is the left half of this picture; the decomposition itself still holds.

Related: [[Cross-Validation and Model Selection]].

## Common confusions
- **"Bias and variance are properties of one fitted model."** They are properties of the *learning procedure* over random training sets; one fit gives one dart.
- **"More data reduces bias."** Mainly it reduces variance; a straight line stays a straight line.
- **"Low training error means low bias."** It may just mean high variance (memorisation). Bias is about the *average* fit vs. the truth.
- **"The tradeoff is a law."** It describes the typical behaviour of classical models; double descent shows it is not the full story for over-parameterized models.
- **"Noise can be modelled away."** $\sigma^2$ is irreducible given the features you have.

## Check yourself

> [!question]- Train error 2 %, validation error 15 %. Bias or variance problem? Two fixes?
> Variance. More data, stronger regularization, a simpler model, or bagging.

> [!question]- Train error 14 %, validation error 15 %, and the target is 3 %. What now?
> Bias. Use a more flexible model, add features, or reduce regularization.

> [!question]- What happens to the variance of k-NN regression when $k$ goes from 1 to 10 (noise variance $\sigma^2$)?
> It drops from $\sigma^2$ to $\sigma^2/10$, while the bias typically increases.

> [!question]- Why does averaging 1 000 highly correlated trees ($\rho = 0.8$) not remove most of the variance?
> The variance tends to $\rho\sigma^2 = 0.8\sigma^2$, not 0; decorrelating the trees is what helps.

## Practice
[Bias-Variance Tradeoff - Exercises](Bias-Variance%20Tradeoff%20-%20Exercises.ipynb)

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 2
- [Elements of Statistical Learning (free)](https://hastie.su.domains/ElemStatLearn/) ch. 7
- [CS229 cheatsheets](https://stanford.edu/~shervine/teaching/cs-229/)
- [MLU-Explain – The Bias-Variance Tradeoff (interactive)](https://mlu-explain.github.io/bias-variance/)
