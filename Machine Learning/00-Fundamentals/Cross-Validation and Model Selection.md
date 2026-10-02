---
tags: [ml, fundamentals, evaluation]
---
# Cross-Validation and Model Selection

> [!summary] In one sentence
> Cross-validation estimates how well a model will do on unseen data by repeatedly **training on part of the data and scoring on the rest**, so you can choose models and hyperparameters without ever touching the test set.

## Intuition first

A student who studies only from last year's exam and then "tests" themselves on that same exam will feel brilliant, and fail the real one. To get an honest estimate you must score yourself on questions you did not practise on. That is a **validation set**.

But one validation split is a single, noisy draw: you might get lucky questions. **k-fold cross-validation** fixes that by rotating: split the data into $k$ pieces, let each piece take a turn as the "exam" while you study on the others, and average the $k$ scores. Every example is used for validation exactly once and for training $k-1$ times.

And the real exam, the **test set**, stays in a sealed envelope until the very end.

![5-fold cross-validation rotating the validation fold](../../Attachments/ML%20Animations/Cross-Validation%20and%20Model%20Selection%20-%20k-fold%20rotation.gif)
*Watch the orange validation fold move one step per fit while the test set stays locked; the CV score is the average of the five fold scores.*

## Splits
- **Train** fits parameters · **Validation** tunes hyperparameters · **Test** touched once at the end.

Why three sets? Parameters (weights) are fitted by the learning algorithm on the training set. Hyperparameters ($\lambda$, tree depth, $k$ in k-NN) cannot be fitted on the training set, because training error always prefers the most flexible option, so they are **chosen** on validation data. But choosing among many options on the validation set makes its score optimistic (you picked the luckiest), so a third, untouched set is needed for the final, unbiased report.

## k-fold CV
Split into $k$ folds; train on $k-1$, validate on 1; average. Typical $k=5$ or $10$.

$$\text{CV}(k) = \frac1k\sum_{i=1}^k s_i,$$
where $s_i$ is the score (or loss) of the model trained without fold $i$ and evaluated on fold $i$. The spread of the $s_i$ gives a rough sense of uncertainty, but the folds are **not independent**: any two training sets share a fraction $\frac{k-2}{k-1}$ of their data (for $k = 10$, about 89 %), so the naive standard error underestimates the true uncertainty.

**Choosing $k$.** Small $k$ means each model trains on less data (pessimistic bias) but is cheap. Large $k$ means less bias but more fits and more correlated training sets. $k = 5$ or $10$ is the usual compromise.

- **Stratified**: preserve class ratios.
- **Leave-one-out**: $k=N$, low bias, high cost.
- **Group k-fold**: keep related samples (same patient/user) together.
- **Time-series split**: only train on the past. Never shuffle temporal data.

**Why each variant exists.**
- *Stratified*: with 5 % positives and 5 folds, a random split could put almost no positives in one fold, making its score meaningless. Stratification keeps about 5 % in every fold.
- *Leave-one-out*: each model sees $N-1$ points (almost the full data, so low bias), but you need $N$ fits, and the estimate can have high variance.
- *Group k-fold*: if the same patient appears in train and validation, the model can recognise the patient instead of the disease. The validation score then measures memorisation; grouping measures generalisation to **new** patients.
- *Time-series split*: train on $[1..t]$, validate on $[t+1..t+h]$, then expand the window. Shuffling would let the model "see the future", for example using next week's prices to predict today's.

## Nested CV
Outer loop estimates generalization; inner loop tunes hyperparameters. Avoids optimistic bias.

Step by step:
1. Outer loop: split into $k_{out}$ folds. Hold out outer fold $j$.
2. Inner loop: on the remaining data, run a full k-fold CV for every hyperparameter setting and pick the best.
3. Refit the best setting on all the outer-training data, score it on outer fold $j$.
4. Average the outer scores. This estimates the performance of the **whole procedure** "tune with CV, then fit", not of one lucky configuration.

If you instead report the best inner CV score directly, you report a maximum over many noisy estimates, which is biased upwards; the more configurations you try, the bigger the bias.

## Hyperparameter search
Grid → random (often better) → Bayesian optimization (Optuna, Hyperopt) → successive halving / Hyperband.

- **Grid search** tries every combination. With 3 hyperparameters × 10 values, that is 1 000 configurations, and if only one hyperparameter really matters, grid search tests only 10 distinct values of it.
- **Random search** samples configurations. Each trial tests a *new* value of every hyperparameter, so the important ones are explored much more densely. If the top 5 % of the space counts as "good", the probability that $n$ random trials all miss it is $0.95^n$; to hit it with 95 % probability you need $n \ge \frac{\ln 0.05}{\ln 0.95} \approx 59$ trials, independent of the number of dimensions.
- **Bayesian optimization** fits a cheap surrogate model of "score vs. hyperparameters" and picks the next trial where improvement looks most likely.
- **Successive halving / Hyperband** give many configurations a small budget (few epochs, a data subset), keep the best half (or $1/\eta$), double their budget, and repeat. With $n$ configurations and initial budget $r$, each round costs about $n r$, for $\log_2 n + 1$ rounds, instead of $n$ full-budget runs.

## Information criteria
$\mathrm{AIC}=2k-2\ln\hat L$, $\mathrm{BIC}=k\ln N-2\ln\hat L$: penalize model complexity.

Symbols: here $k$ is the **number of parameters** (not folds), $\hat L$ the maximised likelihood, $N$ the number of observations. Lower is better. Both reward fit ($-2\ln\hat L$ falls as the model fits better) and charge for parameters. BIC's charge, $\ln N$ per parameter, exceeds AIC's 2 as soon as $N \ge 8$, so BIC prefers smaller models. AIC aims at good prediction; BIC aims at identifying the true model (consistent as $N \to \infty$). Unlike CV, both need only one fit, but they require a likelihood and are approximations.

## Worked example

**Counting fits.** Grid of $4 \times 5 = 20$ settings, 5-fold CV: $20 \times 5 = 100$ fits, plus 1 final refit on all training data = 101. Wrapping it in a 5-fold outer loop (nested CV): $5 \times 101 = 505$ fits.

**AIC and BIC disagree.** $N = 100$. Model A: $k = 3$, $\ln\hat L = -100$. Model B: $k = 6$, $\ln\hat L = -95$.
- AIC: A $= 6 + 200 = 206$, B $= 12 + 190 = 202$, so **B** wins.
- BIC: A $= 3\ln100 + 200 \approx 213.8$, B $= 6\ln 100 + 190 \approx 217.6$, so **A** wins.

The 5-unit gain in log-likelihood is worth 3 extra parameters under AIC but not under BIC's harsher penalty.

> [!danger] Data leakage
> Fit scalers, imputers, feature selectors **inside** each fold (use a pipeline). See [[Common Pitfalls]].

Why: if you standardise with the mean of all data, or select the 20 "best" features using all labels, the validation folds have influenced training. Feature selection leakage is especially severe: with thousands of random features and few samples, selecting on all data then cross-validating can report high accuracy on pure noise.

## Common confusions
- **"CV gives me a final model."** CV gives an *estimate* for a procedure. After choosing hyperparameters, refit on all training data for the final model.
- **"The best CV score is an unbiased estimate of that model's performance."** It is optimistic after selection; use nested CV or the test set.
- **"Shuffled k-fold is fine for time series."** It leaks the future into training.
- **"More folds are always better."** More cost, more correlated folds, and the variance of the estimate does not necessarily fall.
- **"AIC's $k$ and k-fold's $k$ are the same."** One counts parameters, the other folds.

## Check yourself

> [!question]- You have 500 MRI scans from 100 patients (5 each). Which splitter?
> Group k-fold with patient ID as the group, so no patient appears in both training and validation.

> [!question]- Why does random search beat grid search when only 2 of 8 hyperparameters matter?
> With the same budget, random search tests many distinct values of each important hyperparameter, while grid search repeats the same few values across the unimportant dimensions.

> [!question]- What exactly does nested CV estimate?
> The generalisation performance of the entire model-building procedure, including hyperparameter tuning.

> [!question]- With $N = 1000$, how much does BIC charge per parameter compared to AIC?
> $\ln 1000 \approx 6.9$ versus 2.

## Practice
[Cross-Validation and Model Selection - Exercises](Cross-Validation%20and%20Model%20Selection%20-%20Exercises.ipynb)

## Learn more
- [scikit-learn – cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)
- [scikit-learn – hyperparameter tuning](https://scikit-learn.org/stable/modules/grid_search.html)
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 5
- [Bergstra & Bengio (2012) – Random Search for Hyper-Parameter Optimization](https://www.jmlr.org/papers/v13/bergstra12a.html)
