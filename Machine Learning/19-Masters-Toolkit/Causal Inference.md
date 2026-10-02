---
tags: [ml, causality, masters]
---
# Causal Inference

> [!summary] In one sentence
> Causal inference estimates what *would* happen if we **intervened** (gave the treatment, showed the recommendation, changed the policy), which ordinary prediction from observed correlations cannot tell you when confounders, colliders or selection distort the data.

Prediction answers "what will happen?"; causal inference answers "what would happen **if we intervened**?". This matters for recommenders (what would the user have clicked without our recommendation?), A/B tests and policy decisions.

## Intuition first

Ice-cream sales and drownings rise and fall together. A predictive model happily uses ice-cream sales to forecast drownings, and it will be accurate. But banning ice cream will not save a single swimmer: both are driven by a third variable, **hot weather**. Prediction only needs the correlation; a *decision* needs the causal effect.

Every causal question is secretly a question about a world you did not observe:

- The user saw our recommendation and clicked. Would they have clicked anyway?
- The patient took drug A and recovered. Would they have recovered on drug B?

These "what if" outcomes are **counterfactuals**. We can never observe them for the same unit at the same time, so causal inference is the art of finding *comparable* units (by randomisation, by adjustment, or by a natural experiment) that stand in for the missing world.

## Two frameworks
- **Potential outcomes (Rubin)**: $Y(1),Y(0)$; average treatment effect $\mathrm{ATE}=\mathbb E[Y(1)-Y(0)]$. We never observe both outcomes for the same unit.
- **Structural causal models (Pearl)**: DAGs + do-operator $p(y\mid do(x))\neq p(y\mid x)$. This extends the [[Probabilistic Graphical Models]] you already know.

The two languages are compatible: potential outcomes are good for *estimation* (what assumptions make an estimator unbiased), DAGs are good for *reasoning* about which variables to adjust for.

![A DAG with confounder Z: observing X uses both the causal path and the backdoor path; intervening cuts the arrow into X](../../Attachments/ML%20Animations/Causal%20Inference%20-%20seeing%20vs%20doing.gif)

*Watch the arrow $Z\to X$ get cut when we switch from seeing $p(y\mid x)$ to doing $p(y\mid do(x))$: only the green causal path $X\to Y$ is left, and the backdoor formula recovers it from observational data.*

## The math, step by step

### Potential outcomes

Each unit $i$ has two potential outcomes: $Y_i(1)$ if treated, $Y_i(0)$ if not. The treatment indicator is $T_i\in\{0,1\}$. We observe only

$$Y_i=T_iY_i(1)+(1-T_i)Y_i(0).$$

In words: we see the outcome under the treatment the unit actually received; the other one is missing by construction (the **fundamental problem of causal inference**). So individual effects $Y_i(1)-Y_i(0)$ are never computable; averages can be.

- $\mathrm{ATE}=\mathbb E[Y(1)-Y(0)]$: average effect over the whole population.
- $\mathrm{ATT}=\mathbb E[Y(1)-Y(0)\mid T=1]$: average effect on those who were treated.
- **Naive difference** $\mathbb E[Y\mid T=1]-\mathbb E[Y\mid T=0]$. Adding and subtracting $\mathbb E[Y(0)\mid T=1]$ gives

$$\underbrace{\mathbb E[Y\mid T=1]-\mathbb E[Y\mid T=0]}_{\text{naive}}=\underbrace{\mathbb E[Y(1)-Y(0)\mid T=1]}_{\text{ATT}}+\underbrace{\mathbb E[Y(0)\mid T=1]-\mathbb E[Y(0)\mid T=0]}_{\text{selection bias}}.$$

In words: the naive comparison is the true effect plus a bias that measures how different the treated and untreated groups would have been *without* treatment. Randomisation makes the selection-bias term zero.

**Identification assumptions** for observational data:
- **Consistency / SUTVA**: the observed outcome equals the potential outcome of the treatment received; no interference between units and one version of the treatment.
- **Ignorability** (no unmeasured confounding): $(Y(1),Y(0))\perp T\mid X$.
- **Positivity** (overlap): $0<P(T=1\mid X)<1$ for every $X$, so every kind of unit has a chance of both treatments.

### Structural causal models and the do-operator

A DAG encodes "who listens to whom". The **do-operator** $do(X=x)$ means: set $X$ by force, deleting all arrows *into* $X$ while keeping everything else. Hence in general $p(y\mid do(x))\neq p(y\mid x)$: conditioning on $X=x$ also tells you about $X$'s causes, intervening does not.

**Backdoor criterion.** A set $Z$ is a valid adjustment set for the effect of $X$ on $Y$ if (i) no node in $Z$ is a descendant of $X$, and (ii) $Z$ blocks every path from $X$ to $Y$ that starts with an arrow **into** $X$ (a "backdoor" path). Then

$$p(y\mid do(x))=\sum_z p(y\mid x,z)\,p(z).$$

In words: compute the effect separately inside each stratum of $Z$ (where $X$ is "as good as random"), then average over the *population* distribution of $Z$, not over the distribution among the treated.

Do **not** adjust for a **mediator** ($X\to M\to Y$): it removes the indirect effect. Do **not** adjust for a **collider** ($X\to C\leftarrow Y$, or any child of $Y$): it opens a spurious path.

### Propensity scores and IPW

The **propensity score** $e(x)=P(T=1\mid X=x)$ is the probability of being treated given covariates. Under ignorability and positivity, the **inverse-propensity-weighted** estimator is

$$\widehat{\mathrm{ATE}}=\frac1n\sum_{i=1}^n\Big[\frac{T_iY_i}{e(X_i)}-\frac{(1-T_i)Y_i}{1-e(X_i)}\Big].$$

In words: a treated unit that was *unlikely* to be treated represents many similar untreated-looking units, so it gets a large weight $1/e$. Why it is unbiased (with the true $e$):
$\mathbb E\big[\frac{TY}{e(X)}\big]=\mathbb E\big[\frac{TY(1)}{e(X)}\big]=\mathbb E\big[\frac{\mathbb E[T\mid X]\,\mathbb E[Y(1)\mid X]}{e(X)}\big]=\mathbb E[Y(1)]$, using consistency, then ignorability (to factorise), then $\mathbb E[T\mid X]=e(X)$. When $e(X)$ is close to 0 or 1 the weights explode and the variance blows up, which is a positivity problem in disguise (clip or trim the weights, or use doubly-robust estimators).

### Quasi-experiments

- **Difference-in-differences**: $\mathrm{DiD}=(\bar Y^{\text{treated}}_{\text{after}}-\bar Y^{\text{treated}}_{\text{before}})-(\bar Y^{\text{control}}_{\text{after}}-\bar Y^{\text{control}}_{\text{before}})$. Subtracting the control group's change removes common trends. Key assumption: **parallel trends** without treatment.
- **Instrumental variables**: an instrument $Z$ shifts the treatment $X$, is independent of the unobserved confounder $U$ and affects $Y$ only through $X$. From $Y=\beta X+U$ with $Z\perp U$, take $\mathbb E[\cdot\mid Z=1]-\mathbb E[\cdot\mid Z=0]$ of both sides to get the **Wald estimator**
$\beta=\frac{\mathbb E[Y\mid Z=1]-\mathbb E[Y\mid Z=0]}{\mathbb E[X\mid Z=1]-\mathbb E[X\mid Z=0]}$. With continuous variables this becomes **two-stage least squares** (regress $X$ on $Z$, then $Y$ on the fitted $\hat X$). A weak instrument (denominator near 0) makes the estimate explode.
- **Regression discontinuity**: treatment is assigned by a cutoff on a score; compare units just above and just below. Assumption: units cannot precisely manipulate the score around the cutoff.

## Key tools
| Tool | Use |
|---|---|
| Randomised experiments / A/B tests | gold standard |
| Backdoor adjustment | control for confounders blocking backdoor paths |
| Propensity scores, IPW | reweight observational data; also used in **unbiased recommender evaluation** ([[Evaluating Recommenders]]) |
| Instrumental variables, diff-in-diff, regression discontinuity | quasi-experiments |
| Uplift modelling, meta-learners (T-, S-, X-learner), causal forests | heterogeneous effects with ML |

**Why randomisation is the gold standard**: random assignment makes $T$ independent of everything, observed or not, so the naive difference in means is unbiased for the ATE. For an A/B test with $n_1,n_0$ users per arm, a 95% confidence interval is $\hat\Delta\pm1.96\sqrt{s_1^2/n_1+s_0^2/n_0}$.

**Meta-learners** estimate the *conditional* effect $\tau(x)=\mathbb E[Y(1)-Y(0)\mid X=x]$ with any ML regressor:
- **S-learner**: one model $\mu(x,t)$ with $t$ as a feature; $\hat\tau(x)=\mu(x,1)-\mu(x,0)$. Simple, but regularisation can shrink the treatment effect to zero if $t$ is a weak feature.
- **T-learner**: two models $\mu_1,\mu_0$ fit on treated and control separately; $\hat\tau(x)=\mu_1(x)-\mu_0(x)$. Flexible, but noisy when one group is small.
- **X-learner**: imputes individual effects using the other group's model and combines them with propensity weights; good for unbalanced groups.
- **Causal forests** grow trees that split to maximise effect heterogeneity rather than prediction accuracy.

## Worked example

**Naive difference vs. ATE.** An oracle shows both potential outcomes for four users (minutes watched):

| unit | $Y(1)$ | $Y(0)$ | $T$ | observed $Y$ |
|---|---|---|---|---|
| 1 | 9 | 7 | 1 | 9 |
| 2 | 8 | 6 | 1 | 8 |
| 3 | 3 | 2 | 0 | 2 |
| 4 | 4 | 3 | 0 | 3 |

- True ATE: effects $2,2,1,1$, mean $1.5$.
- Naive: $\frac{9+8}{2}-\frac{2+3}{2}=8.5-2.5=6$.
- ATT $=2$; selection bias $=\mathbb E[Y(0)\mid T=1]-\mathbb E[Y(0)\mid T=0]=6.5-2.5=4$; check: $2+4=6$. Heavy users got treated, so the naive number quadruples the effect.

**Backdoor adjustment (Simpson's paradox).** Suppose a confounder $Z$ (e.g. severity) drives both the treatment and the outcome. In the animation below, the pooled regression of $Y$ on $X$ has a **negative** slope, yet within each value of $Z$ the slope is **positive**. The pooled comparison mixes "who gets more $X$" with "what $X$ does".

![Pooled data show a negative trend; splitting by the confounder Z reveals a positive trend inside each group](../../Attachments/ML%20Animations/Causal%20Inference%20-%20Simpsons%20paradox.gif)

*Watch the red pooled line point downwards, then the blue and yellow within-group lines point upwards once the points are coloured by $Z$.*

With counts: if treatment A succeeds more often than B in **every** stratum but A was given mostly to hard cases, the raw success rates can favour B. The adjusted comparison $P(\text{succ}\mid do(A))=\sum_z P(\text{succ}\mid A,z)P(z)$ weights each stratum by its population share and reverses the conclusion back to A.

**Difference-in-differences.** A treated region goes from 20 to 26 sessions, a control region from 18 to 21. DiD $=(26-20)-(21-18)=3$; the naive before/after number $6$ would wrongly credit the common trend ($+3$) to the feature.

## Classic pitfalls

Classic pitfalls: confounding, collider bias (the "explaining away" effect from d-separation), Simpson's paradox, selection bias.

- **Confounding**: a common cause $Z\to X$, $Z\to Y$ creates correlation without causation. Fix: adjust for $Z$ (backdoor), randomise, or use a quasi-experiment if $Z$ is unmeasured. In a linear model $Y=2X+3Z+\varepsilon$ with $X=Z+\text{noise}$, omitting $Z$ gives slope $2+3\,\mathrm{Cov}(X,Z)/\mathrm{Var}(X)$, i.e. omitted-variable bias.
- **Collider bias**: in $A\to C\leftarrow B$, $A$ and $B$ are independent, but **conditioning** on $C$ makes them dependent ("explaining away", as in [[Probabilistic Graphical Models]]). Among Hollywood actors, talent and looks look negatively correlated because being cast depends on both. In ML: training only on items that were *shown* or *clicked* conditions on a collider.
- **Simpson's paradox**: a trend in pooled data reverses inside every subgroup, because group membership confounds the comparison.
- **Selection bias**: the units in your data were selected by a process related to the outcome (survivorship, logged feedback from an existing recommender). IPW with the logging policy's propensities is the standard correction ([[Evaluating Recommenders]]).

## Common confusions

- *"A strong feature importance means the feature causes the outcome."* → Importance measures predictive usefulness. A confounder can make a feature predictive with zero causal effect.
- *"Adjust for as many variables as possible."* → Adjusting for mediators removes part of the effect, and adjusting for colliders creates bias. Choose the set with the backdoor criterion.
- *"$p(y\mid do(x))$ is just $p(y\mid x)$ with better data."* → They are different quantities. Even infinite observational data give $p(y\mid x)$; you need assumptions (a DAG, ignorability) or an experiment to get the interventional one.
- *"IPW fixes everything."* → Only under ignorability and positivity. Unmeasured confounders stay biased, and tiny propensities give huge variance.
- *"Diff-in-diff needs similar levels."* → It needs parallel **trends**; the levels may differ.

## Check yourself

> [!question]- Why can we never compute an individual treatment effect from data?
> Each unit is either treated or not, so only one of $Y_i(1)$, $Y_i(0)$ is observed; the other is a counterfactual that is missing by construction.

> [!question]- In the DAG $C\to X$, $C\to Y$, $X\to M\to Y$, $X\to Y$, $Y\to S$, is $\{C,S\}$ a valid backdoor set for the effect of $X$ on $Y$?
> No. $S$ is a descendant of $X$ (through $Y$), so condition (i) fails; conditioning on a child of $Y$ also biases the estimate. $\{C\}$ alone is valid.

> [!question]- With 6 users, $e(1)=2/3$, $e(0)=1/3$: what weight does a treated unit with $X=0$ get in IPW?
> $1/e(0)=3$: it was unlikely to be treated, so it stands in for three similar units.

> [!question]- An encouragement raises treatment uptake from 0.2 to 0.7 and mean outcome from 1.0 to 2.0. What is the IV estimate?
> Wald: $(2.0-1.0)/(0.7-0.2)=2$. The intent-to-treat effect $1$ is scaled up by the compliance difference $0.5$.

> [!question]- Why does conditioning on "was cast" make talent and looks negatively correlated among actors?
> Casting is a collider (talent → cast ← looks). Conditioning on it opens the path: among those cast, a less talented actor must have been better-looking to make it.

## Practice

[Causal Inference - Exercises](Causal%20Inference%20-%20Exercises.ipynb): seeing vs. doing, collider bias, choosing adjustment sets, ATE vs. naive difference, Simpson's paradox on the kidney-stone data, IPW by hand and its unbiasedness proof, DiD, the Wald estimator and 2SLS, an A/B test, and T- vs. S-learners on simulations where the truth is known.

## Learn more
- [Hernán & Robins — *Causal Inference: What If* (free)](https://miguelhernan.org/whatifbook)
- [Brady Neal — Introduction to Causal Inference (course + book)](https://www.bradyneal.com/causal-inference-course)
- Libraries: DoWhy, EconML, CausalML
- [Scott Cunningham — *Causal Inference: The Mixtape* (free online)](https://mixtape.scunning.com/)
- [Matheus Facure — *Causal Inference for the Brave and True* (free, Python)](https://matheusfacure.github.io/python-causality-handbook/)
