---
tags: [ml, mlops]
---
# MLOps Overview

> [!summary] In one sentence
> MLOps is the engineering discipline of getting models into production and keeping them healthy: versioned data and experiments, reproducible training pipelines, safe deployment, and monitoring that notices when the world drifts away from the training data.

Deeper notes: [[Model Deployment and Serving]] · [[Experiment Tracking and Reproducibility]] · [[Data and Feature Management]].

## Intuition first
Getting models into production and keeping them healthy.

A notebook that reaches 0.92 AUC is a *prototype*, not a product. A useful analogy is the difference between cooking one great meal at home and running a restaurant. The restaurant needs reliable suppliers (data pipelines and validation), written recipes anyone can reproduce (versioned code, data, configs and seeds), a kitchen that can serve 400 plates a second at dinner rush (serving infrastructure), a way to try a new dish on a few customers before changing the menu (canary and A/B tests), and someone tasting the food every day, because ingredients change with the season (monitoring for drift).

The core reason ML needs more than ordinary DevOps: **a model's behaviour depends on data, and data changes**. Code that is not touched keeps working; a model that is not touched slowly gets worse as users, products, prices and fraudsters change. So MLOps is a **loop**, not a line: data → train → package → deploy → monitor → (drift detected) → retrain.

![Production distribution drifting away from training data while the PSI drift score climbs past its alert threshold](../../Attachments/ML%20Animations/MLOps%20Overview%20-%20data%20drift.gif)
*Watch the yellow production distribution slide away from the blue training distribution over the weeks: the model has not changed, but the PSI score goes from green (stable) to yellow (watch) to red (retrain).*

## The stages
| Stage | Practices & tools |
|---|---|
| Data | versioning (DVC, lakeFS), validation (Great Expectations), feature stores (Feast) |
| Experiments | tracking (MLflow, Weights & Biases), configs (Hydra), seeds |
| Training | pipelines (Airflow, Kubeflow, Prefect), distributed training, HPO (Optuna) |
| Packaging | Docker, ONNX, model registry |
| Serving | batch vs online; FastAPI, TorchServe, Triton, BentoML; latency budgets |
| Monitoring | data drift, concept drift, prediction distribution, performance on delayed labels |
| Testing | unit tests for data/feature code, model behavioural tests, canary/shadow deployment, A/B tests |
| Governance | model cards, lineage, reproducibility, privacy |

### What each stage is for
- **Data.** *Versioning* (DVC, lakeFS) stores a fingerprint (hash) of every dataset so "model v3" points to exactly the bytes it was trained on. *Validation* (Great Expectations) checks schemas, ranges, null rates and category sets before data reaches training or serving, catching broken upstream pipelines early. A *feature store* (Feast) computes each feature once and serves the **same** definition to training and to online serving.
- **Experiments.** Log every run's code version, config, data version, metrics and artefacts (MLflow, W&B); keep configs in files (Hydra), not in edited notebook cells; fix random seeds. Otherwise you cannot tell which change helped.
- **Training.** Pipelines (Airflow, Kubeflow, Prefect) turn "run these cells in order" into a scheduled, retryable graph of steps. Hyperparameter optimisation (Optuna) and distributed training live here.
- **Packaging.** Docker freezes the environment; ONNX exports a framework-neutral model; a **model registry** tracks versions and their stage (staging, production, archived).
- **Serving.** **Batch**: precompute predictions on a schedule (nightly churn scores, weekly recommendations); simple and cheap, but stale. **Online**: compute on request (fraud check at payment time, search ranking); fresh but needs a latency budget (e.g. p99 < 100 ms), autoscaling and fallbacks.
- **Monitoring.** Track input distributions, prediction distribution, latency and errors immediately; track true performance once (often delayed) labels arrive.
- **Testing.** Unit tests for feature code; behavioural tests for the model (see below); safe rollouts (shadow, canary, A/B).
- **Governance.** Model cards (intended use, data, metrics per subgroup, limitations), lineage (which data and code produced which model), reproducibility, privacy (PII handling, retention). See [[Explainability and Fairness]].

## The math, step by step

### Three kinds of drift
Write the joint distribution as $P(X,y)=P(y\mid X)\,P(X)$.
- **Data (covariate) drift**: $P(X)$ changes, $P(y\mid X)$ fixed. *Example:* a new marketing campaign brings younger users. The rule is the same, the inputs move.
- **Concept drift**: $P(y\mid X)$ changes. *Example:* fraudsters change tactics, so the same transaction features now mean something different. **Input monitors cannot see this**; only labelled performance can.
- **Label (prior) shift**: $P(y)$ changes with $P(X\mid y)$ fixed. *Example:* disease prevalence rises during an outbreak.

### Population Stability Index
Bin a feature (often by deciles of the training data). With expected (training) proportions $e_i$ and actual (production) proportions $a_i$:
$$\text{PSI}=\sum_i (a_i-e_i)\ln\frac{a_i}{e_i}.$$
Each term is $\ge0$ (both factors have the same sign), so PSI is 0 only when the distributions match. It is a symmetrised KL divergence. Rule of thumb: $<0.1$ stable, $0.1$–$0.25$ moderate shift, $>0.25$ major shift. Add a small $\varepsilon$ to empty bins to avoid $\ln0$.

### Kolmogorov–Smirnov statistic
For continuous features, compare the empirical CDFs of the reference and production samples:
$$D=\max_x\big|F_{\text{ref}}(x)-F_{\text{prod}}(x)\big|,$$
the largest vertical gap between the two staircase curves. Large $D$ (small p-value) → the samples probably come from different distributions. With huge samples even tiny, harmless shifts become "significant", so look at effect sizes too.

### A/B testing a new model
Control converts $\hat p_C=x_C/n_C$, treatment $\hat p_T=x_T/n_T$. Under $H_0$ (no difference) use the pooled rate $\hat p=\frac{x_C+x_T}{n_C+n_T}$:
$$z=\frac{\hat p_T-\hat p_C}{\sqrt{\hat p(1-\hat p)\big(\frac1{n_C}+\frac1{n_T}\big)}}.$$
$|z|>1.96$ → significant at $\alpha=0.05$ (two-sided). A 95 % confidence interval for the lift uses the unpooled standard error $\sqrt{\hat p_C(1-\hat p_C)/n_C+\hat p_T(1-\hat p_T)/n_T}$.

**Sample size** per group to detect an absolute lift $\delta$ from baseline $p_1$ to $p_2=p_1+\delta$ with significance $\alpha$ and power $1-\beta$ (approximately):
$$n\approx\frac{(z_{1-\alpha/2}+z_{1-\beta})^2\,\big[p_1(1-p_1)+p_2(1-p_2)\big]}{\delta^2}.$$
Small effects need *many* users: halving $\delta$ quadruples $n$. Decide $n$ in advance; stopping as soon as $p<0.05$ ("peeking") inflates false positives.

### Capacity planning: Little's law
In a stable system, average number of requests in flight $L$ = arrival rate $\lambda$ × average time in system $W$:
$$L=\lambda W.$$
It tells you how many concurrent workers (or GPU slots) you need.

## Worked example
**PSI.** Training proportions $e=(0.5,0.3,0.2)$, this week $a=(0.4,0.3,0.3)$:
$(0.4-0.5)\ln0.8=0.022$, $(0.3-0.3)\ln1=0$, $(0.3-0.2)\ln1.5=0.041$. Total PSI $\approx0.063$ → stable, no alert.

**KS.** Reference $\{1,2,3\}$, production $\{2,3,4\}$. ECDF values: at 1: $1/3$ vs $0$; at 2: $2/3$ vs $1/3$; at 3: $1$ vs $2/3$; at 4: $1$ vs $1$. Largest gap $D=1/3$.

**A/B.** Control 200/2000 = 10 %, treatment 240/2000 = 12 %. Pooled $\hat p=0.11$, SE $=\sqrt{0.11\cdot0.89\cdot(2/2000)}\approx0.0099$, $z=0.02/0.0099\approx2.02$ → $p\approx0.04$: just significant at 5 %.

**Little's law.** $\lambda=200$ requests/s, $W=50$ ms: $L=200\times0.05=10$ requests in flight on average. Provision comfortably more (say 15–20 workers) to absorb bursts and keep tail latency down.

## Deploying safely
- **Shadow deployment**: the new model receives a copy of live traffic and its predictions are logged but **not shown** to users. Answers: does it run correctly at production load, and how do its predictions differ? Zero user risk.
- **Canary release**: route a small slice (e.g. 1–5 %) of real users to the new model, watch errors and key metrics, then ramp up. Answers: is it safe? Limited blast radius.
- **A/B test**: split users randomly between models for long enough to measure a business metric with statistical power. Answers: is it *better*?

## Testing ML systems
- **Data/feature unit tests**: does the feature function handle nulls, units, time zones?
- **Behavioural tests** (CheckList, Ribeiro et al.): *invariance* (changing an irrelevant feature such as the applicant's name should not change the prediction), *directional expectation* (higher income should not lower the credit score), *minimum functionality* (simple obvious cases must be right).
- **Training–serving skew**: the model saw different features offline than online. Causes: features computed by different code paths (Python offline, Java online), **leakage** of future information into training features, different preprocessing versions, stale feature values at serving time. A feature store and logging the exact served features are the main defences. See [[Common Pitfalls]].

## Common confusions
- **"No input drift means the model is fine."** → Concept drift changes $P(y\mid X)$ with identical inputs; only labelled performance reveals it.
- **"Drift detected → retrain immediately."** → First check it matters (did performance drop? is it a data bug upstream?). Many alerts are pipeline breakages, not real-world change.
- **"Offline metrics predict online results."** → Skew, feedback loops and business metrics that differ from the training loss make online tests (canary, A/B) necessary.
- **"Reproducibility = saving the model file."** → You need code version, data version (hash), config, environment and seeds, plus lineage linking them.
- **"Online serving is always better."** → If predictions can be a day old, batch is simpler, cheaper and easier to monitor.

## Check yourself
> [!question]- Fraudsters change tactics so the same features now indicate different outcomes. Which kind of drift is this, and can a PSI monitor on inputs detect it?
> Concept drift ($P(y\mid X)$ changes). No: inputs may look identical; you need labelled performance monitoring.

> [!question]- What question does a shadow deployment answer that an A/B test does not need to, and vice versa?
> Shadow: is the new model technically sound and how do its predictions differ, at zero user risk. A/B: does it actually improve user/business outcomes, which needs users to see its outputs.

> [!question]- Compute PSI for $e=(0.5,0.5)$ and $a=(0.6,0.4)$.
> $0.1\ln1.2+(-0.1)\ln0.8=0.0182+0.0223\approx0.04$: stable.

> [!question]- A model scores 0.92 AUC offline and 0.70 in production with no input drift. Name two likely causes.
> Training–serving skew (different feature code or preprocessing online), and leakage of future information into offline training features (also stale online features, or a label definition mismatch).

> [!question]- With 400 requests/s and 25 ms per request, how many requests are in flight on average?
> $L=\lambda W=400\times0.025=10$.

## Practice
[MLOps Overview - Exercises](MLOps%20Overview%20-%20Exercises.ipynb): drift types, batch vs online serving, shadow/canary/A/B, training–serving skew, reproducibility, PSI and KS by hand and in code, A/B significance and sample size, Little's law, a data validator, data fingerprints and seeds, why concept drift is invisible to input monitors, and behavioural tests.

## Learn more
- [Made With ML — MLOps course](https://madewithml.com/)
- [Stanford CS329S — ML Systems Design (Chip Huyen)](https://stanford-cs329s.github.io/)
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/course/)
- Book: *Designing Machine Learning Systems* — Chip Huyen (O'Reilly 2022)
- [Beyond Accuracy: Behavioral Testing of NLP Models with CheckList — Ribeiro et al. 2020](https://arxiv.org/abs/2005.04118)

See [[ML Workflow]] and [[Common Pitfalls]].
