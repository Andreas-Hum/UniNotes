---
tags: [ml, fundamentals, workflow]
status: not-started
notebook: not-started
level:
reviewed:
---
# ML Workflow

> [!summary] In one sentence
> A machine-learning project is a loop: frame the problem, split the data before peeking, beat a simple baseline, iterate with error analysis, touch the test set **once**, then deploy and keep monitoring.

## Intuition first

Building a model is less like solving one exam question and more like running an experiment in a lab. You need a clear hypothesis (*what* are we predicting and *how* will we judge it?), a control group (a **baseline**), and a sealed envelope with the final answer that you only open at the end (the **test set**). Most real-world failures are not caused by the wrong algorithm; they come from a badly framed problem, leaked information, or a model that silently degrades after launch.

The workflow below is the checklist that prevents those failures. Steps 4–7 form an inner loop you go round many times; steps 2–9 form an outer loop that restarts when the world changes.

![The ML workflow as a pipeline with two feedback loops](../../Attachments/ML%20Animations/ML%20Workflow%20-%20pipeline%20and%20feedback%20loops.gif)
*Watch for the two loops: the yellow "iterate" loop between error analysis and modelling, and the purple loop from monitoring back to data collection. The test step is boxed in red because it is used once.*

## The nine steps

1. **Frame the problem**: task, metric, baseline, constraints.
2. **Collect & inspect data**: distributions, leakage, label quality.
3. **Split**: before looking at test data. [[Cross-Validation and Model Selection]]
4. **Preprocess & engineer features**: [[Data Preprocessing]], [[Feature Engineering]].
5. **Baseline**: dummy model, then [[Logistic Regression]] / [[Linear Regression]].
6. **Iterate models**: [[Ensemble Methods]], [[Neural Networks]].
7. **Error analysis**: where does it fail? slices, confusion matrix.
8. **Evaluate once on test**: [[Model Evaluation and Metrics]].
9. **Deploy & monitor**: drift, latency, retraining.

Checklist of mistakes: [[Common Pitfalls]]. Exam version: [[Exam Checklist]].

## Each step, with the *why*

**1. Frame.** Decide what is predicted, for whom, and what a mistake costs. "Predict churn" becomes "predict which customers cancel within 30 days, scored by recall at a fixed budget of 500 calls per week". Name constraints: latency, interpretability, fairness, data you are allowed to use. Without a metric agreed in advance you will unconsciously pick the one that flatters your model.

**2. Collect & inspect.** Plot distributions, count missing values, check label noise (have two people label 100 examples and compare). Look for **leakage**: features that would not be available at prediction time (e.g. "refund issued" when predicting fraud, or a patient ID that encodes the hospital ward).

**3. Split before peeking.** Any decision you make after looking at test data (which features to keep, which outliers to drop) leaks test information into the model. Split by *time* for temporal data and by *group* (user, patient) when rows from the same entity are correlated.

**4. Preprocess & engineer features.** Fit every transformation (scaler, imputer, encoder) on the training data only, inside a pipeline.

**5. Baseline.** A dummy model (always predict the majority class, or the training mean) tells you what "no skill" looks like. Then a simple linear model tells you how far plain features get you. If a deep net beats the dummy by 0.5 %, that is not a success.

**6. Iterate models.** Try richer models, tune hyperparameters with cross-validation on the training data.

**7. Error analysis.** Look at the confusion matrix and at performance on **slices** (by country, device, age group). Averages hide failures: 95 % overall accuracy can mean 60 % on a minority slice. Error analysis tells you whether to get more data, better features, or a different model.

**8. Test once.** The test score is only unbiased if nothing was chosen based on it. If you evaluate 20 variants on the test set and report the best, you report the maximum of 20 noisy numbers, which is optimistically biased.

**9. Deploy & monitor.** The world drifts:
- **Data (covariate) drift**: $p(x)$ changes (new user population, a sensor recalibrated), while $p(y\mid x)$ stays the same.
- **Concept drift**: $p(y\mid x)$ changes (fraudsters change tactics; what used to be safe is now fraud).

Monitor input distributions (e.g. a two-sample test such as Kolmogorov–Smirnov per feature, or the population stability index), prediction distributions, and, when labels arrive, the live metric. Retrain when they move.

## The math, step by step

**How precise is a test accuracy?** Each test example is a Bernoulli trial with success probability $p$ (the true accuracy). The observed accuracy $\hat p$ on $n$ examples has standard error
$$\mathrm{SE}(\hat p) = \sqrt{\frac{\hat p\,(1-\hat p)}{n}},$$
and an approximate 95 % confidence interval is $\hat p \pm 1.96\,\mathrm{SE}$. Small test sets give wide intervals, so small differences between models may be noise.

**Framing with costs: the decision threshold.** A classifier outputs $p = P(y = 1 \mid x)$. Predicting "negative" costs $C_{FN}$ if the truth is positive; predicting "positive" costs $C_{FP}$ if the truth is negative. Predict positive when its expected cost is lower:
$$(1-p)\,C_{FP} < p\, C_{FN} \iff p > \frac{C_{FP}}{C_{FP} + C_{FN}}.$$
With equal costs the threshold is $0.5$; if a missed fraud costs 10× a false alarm, the threshold drops to $1/11 \approx 0.09$.

**The regression baseline.** Predicting the training mean $\bar y$ for everyone gives $R^2 = 0$ on data with that mean, by definition of $R^2 = 1 - SS_{res}/SS_{tot}$. Any useful regression model must have $R^2 > 0$ on held-out data.

## Worked example

A model has **96 % accuracy** on a test set of $n = 1000$ transactions, 95 % of which are legitimate.

1. **Baseline:** always predicting "legitimate" scores 95 %. The model is only 1 percentage point better.
2. **Precision of the estimate:** $\mathrm{SE} = \sqrt{0.96 \cdot 0.04 / 1000} \approx 0.0062$, so the 95 % CI is roughly $96\% \pm 1.2\%$, i.e. $[94.8\%, 97.2\%]$, which includes the baseline's 95 %.
3. **Better framing:** look at recall on the fraud class and precision of the alerts, and set the threshold from the costs. With $C_{FP} = 1$ and $C_{FN} = 20$: threshold $= 1/21 \approx 0.048$.

## Common confusions
- **"The validation set and the test set are interchangeable."** Validation is for choosing; test is for reporting. Once you choose based on a set, it is a validation set.
- **"Fitting the scaler on all data is harmless."** It leaks test statistics (mean, variance) into training. Usually a small effect, but with target encoding or feature selection the leak can be large.
- **"Skip the baseline, the fancy model is obviously better."** Without a baseline you cannot tell skill from class imbalance.
- **"Deployment is the end."** It is the start of monitoring; models decay as data drift.
- **"Data drift and concept drift are the same."** Data drift changes $p(x)$; concept drift changes $p(y\mid x)$. The second one breaks the model even if inputs look familiar.

## Check yourself

> [!question]- Why should you split the data before exploring it in detail?
> Every choice made after looking at the test data (features, outlier rules, model family) can adapt to its quirks, so the final test score becomes optimistically biased.

> [!question]- A model scores 0.81 and another 0.82 accuracy on 500 test examples. Is the second better?
> Not convincingly: $\mathrm{SE} \approx \sqrt{0.81 \cdot 0.19 / 500} \approx 0.018$, so the difference of 0.01 is well within noise.

> [!question]- A spam filter's inputs look exactly as before, but its precision has dropped. What kind of drift is that likely to be?
> Concept drift: $p(y\mid x)$ changed (spammers changed which messages are spam-like), not $p(x)$.

> [!question]- What threshold minimises expected cost when a false negative costs 4 and a false positive costs 1?
> $C_{FP}/(C_{FP}+C_{FN}) = 1/5 = 0.2$.

## Practice
[ML Workflow - Exercises](ML%20Workflow%20-%20Exercises.ipynb)

## Learn more
- [Made With ML](https://madewithml.com/)
- [scikit-learn – choosing an estimator](https://scikit-learn.org/stable/machine_learning_map.html)
- [scikit-learn – common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html)
- [Google – Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)
