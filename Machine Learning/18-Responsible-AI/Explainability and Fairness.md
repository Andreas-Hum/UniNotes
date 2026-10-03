---
tags: [ml, responsible-ai]
status: not-started
notebook: not-started
level:
reviewed:
---
# Explainability and Fairness

> [!summary] In one sentence
> Explainability methods tell you *why* a model predicts what it does (globally, or for one decision), and fairness criteria tell you *for whom* its errors fall; both are needed before you can trust, debug or legally defend a model that makes decisions about people.

## Intuition first
Imagine a bank's model rejects your loan. You would ask two questions:

1. **"Why me?"**: which of my features pushed the decision to "no", and what would I have to change? That is **explainability**, here *local* (one prediction). The bank's data scientists ask the *global* version: which features matter for the model overall, and does it rely on something it should not?
2. **"Is it fair?"**: does the model make more mistakes, or harsher decisions, for some groups of people than for others? That is **fairness**.

The two are linked: explanations are often how unfairness is discovered (e.g. finding that a postcode feature acts as a proxy for ethnicity).

A helpful analogy for **SHAP**: a team wins a prize (the prediction minus the average prediction) and must split it fairly among the players (features). Shapley values, from cooperative game theory, are the unique fair split: each player gets their *average marginal contribution* over all orders in which the team could have been assembled.

![SHAP waterfall: from the base value 0.40 each feature pushes the prediction up or down to 0.35](../../Attachments/ML%20Animations/Explainability%20and%20Fairness%20-%20SHAP%20waterfall.gif)
*Watch the prediction start at the average model output $\phi_0=0.40$; red arrows (income, age) push it up and blue ones (late payments, debt ratio) push it down, and the arrows add up exactly to $f(x)=0.35$.*

## Explainability
| Method | Scope | Idea |
|---|---|---|
| Intrinsically interpretable models | global | [[Linear Regression]], [[Decision Trees]], GAMs |
| Permutation importance | global | drop in score when a feature is shuffled |
| Partial dependence / ICE | global/local | effect of a feature on predictions |
| **LIME** | local | fit a simple surrogate around one prediction |
| **SHAP** | local + global | Shapley values from game theory; TreeSHAP is fast |
| Saliency / Grad-CAM / integrated gradients | local (deep nets) | gradient-based attribution ([[CNN]]) |
| Counterfactual explanations | local | smallest change that flips the decision |

Two further axes to place any method on: **model-specific** (TreeSHAP, Grad-CAM need the model's internals) vs **model-agnostic** (permutation importance, LIME, KernelSHAP only need predictions); and **intrinsic** (the model *is* the explanation) vs **post-hoc** (explaining a black box after training).

### The math, step by step
**Intrinsically interpretable models.** A linear model $f(x)=b+\sum_j w_jx_j$ explains itself: $w_j$ is the change in prediction per unit of $x_j$, holding the others fixed (compare only after standardising features). A **GAM** $f(x)=b+\sum_j g_j(x_j)$ allows each feature its own non-linear curve but keeps contributions additive, so each $g_j$ can be plotted. Shallow [[Decision Trees]] are readable rule lists.

**Permutation importance.** With test score $s$ (e.g. $R^2$ or accuracy), shuffle column $j$ $K$ times and rescore:
$$I_j=s-\frac1K\sum_{k=1}^{K}s_{k,j}.$$
Shuffling breaks the link between feature $j$ and the target while keeping its distribution. Compute it on **held-out** data (on training data it rewards overfitting). Caveat: with two nearly identical features (height in cm and in inches) the model can use either, so shuffling one barely hurts and **both look unimportant**; shuffling also creates unrealistic rows (a 2-m person who is 50 inches tall).

**Partial dependence and ICE.** For feature(s) $S$ with the rest $C$:
$$\text{PD}_S(x_S)=\frac1n\sum_{i=1}^{n}f\big(x_S,\,x_C^{(i)}\big).$$
Each **ICE** curve is one term of the sum (one individual, varying $x_S$); the PD curve is their average. If ICE curves cross or fan out, there are interactions that the average hides.

**Shapley values.** With feature set $F$ and a value function $v(S)$ = expected prediction when only the features in $S$ are known:
$$\phi_i=\sum_{S\subseteq F\setminus\{i\}}\frac{|S|!\,(|F|-|S|-1)!}{|F|!}\Big[v(S\cup\{i\})-v(S)\Big].$$
In words: average the marginal contribution of feature $i$ over all orders of adding features. Key properties (axioms):
- **Efficiency**: $f(x)=\phi_0+\sum_i\phi_i$ with $\phi_0=v(\emptyset)=E[f(X)]$. The contributions add up exactly (the waterfall above).
- **Symmetry**: two features that contribute identically get equal value.
- **Dummy (null player)**: a feature that never changes the prediction gets 0.
- **Additivity**: for a sum of models, the Shapley values add.
Exact computation needs all $2^{|F|}$ subsets. **KernelSHAP** approximates them with a weighted linear regression on sampled coalitions (model-agnostic, slow); **TreeSHAP** computes them exactly in polynomial time for tree ensembles. For a **linear model** with independent features, $\phi_j=w_j\big(x_j-E[x_j]\big)$. Averaging $|\phi_j|$ over a dataset gives a global importance.

**LIME.** Sample perturbed points around $x$, weight them by proximity $\pi_x$, and fit a simple model $g$ (sparse linear) to the black box's outputs:
$$\xi(x)=\arg\min_{g\in G}\ \mathcal L(f,g,\pi_x)+\Omega(g),$$
where $\Omega$ penalises complexity. The coefficients of $g$ are the explanation. It is fast and intuitive, but results depend on the kernel width and the sampling, and can change between runs; SHAP's axioms give it more consistency.

**Gradient-based attributions** (deep nets, [[CNN]]). *Saliency*: $|\partial f/\partial x|$ per pixel. *Integrated gradients*: accumulate gradients along a straight path from a baseline $x'$ (e.g. a black image):
$$\text{IG}_i(x)=(x_i-x_i')\int_0^1\frac{\partial f\big(x'+\alpha(x-x')\big)}{\partial x_i}\,d\alpha,$$
which satisfies completeness (attributions sum to $f(x)-f(x')$). *Grad-CAM* weights the last convolutional feature maps by their pooled gradients to give a coarse heat-map of where the network looked.

**Counterfactual explanations.** Find the closest $x'$ with a different decision: $\min_{x'}d(x,x')$ s.t. $f(x')\neq f(x)$, ideally changing only actionable features (income, not age). For a linear classifier "approve if $w^\top x+b\ge0$", the smallest L2 change moves straight to the boundary:
$$x'=x-\frac{w^\top x+b}{\lVert w\rVert^2}\,w.$$

## Fairness
- Sources of bias: historical data, sampling, labels, proxies, feedback loops ([[Recommender Systems Overview]]).
- Criteria: demographic parity, equalised odds, equal opportunity, calibration — generally **cannot all hold at once**.
- Mitigation: pre-processing (reweighting), in-processing (constraints), post-processing (group thresholds).
- Tools: Fairlearn, AIF360, SHAP.

### Where bias comes from
- **Historical**: the data faithfully records an unfair past (past hiring favoured one group, so "good hire" labels do too).
- **Sampling / representation**: some groups are under-represented (a face dataset with few dark-skinned faces → higher error for them).
- **Label**: the target is a biased proxy for what you care about (arrests as a proxy for crime; healthcare *cost* as a proxy for health *need*).
- **Proxies**: removing the protected attribute does not help when other features (postcode, first name, shopping patterns) encode it.
- **Feedback loops**: the model's decisions shape the next training data (police sent where the model predicts crime record more crime there; recommenders show popular items, which get more clicks, which makes them more popular; see [[Recommender Systems Overview]]).

### The criteria, precisely
With prediction $\hat Y$, true label $Y$, score $S$ and group $A$:
- **Demographic parity**: $P(\hat Y=1\mid A=a)$ equal for all groups (same selection rate). The "80 % rule" (disparate impact) flags a ratio of selection rates below 0.8.
- **Equalised odds**: equal TPR **and** equal FPR across groups, i.e. $\hat Y\perp A\mid Y$.
- **Equal opportunity**: equal TPR only (qualified people are accepted at the same rate in every group).
- **Calibration** (within groups): $P(Y=1\mid S=s,A=a)=s$; a score of 0.7 means 70 % in every group. Its threshold-level cousin is *predictive parity* (equal PPV).

**Why they conflict.** For any group with base rate $p=P(Y=1)$, the confusion-matrix identity gives
$$\text{FPR}=\frac{p}{1-p}\cdot\frac{1-\text{PPV}}{\text{PPV}}\cdot\text{TPR}.$$
If two groups have **different base rates** $p$ and we insist on equal PPV and equal TPR, the right-hand sides differ, so the FPRs **must** differ. Except for a perfect classifier or equal base rates, you cannot have predictive parity and equalised odds together (Chouldechova 2017; Kleinberg et al. 2016). Choosing a criterion is therefore a value judgement about which error matters most in the application.

### Mitigation
- **Pre-processing**: change the data. *Reweighing* (Kamiran & Calders) gives each example the weight $w(g,y)=\frac{P(g)\,P(y)}{P(g,y)}$, so that in the weighted data group and label are independent.
- **In-processing**: change the training objective, e.g. minimise loss subject to a constraint on the difference in selection rates or TPRs (Fairlearn's reductions approach), or adversarial debiasing.
- **Post-processing**: change the decision rule of a trained model, e.g. **group-specific thresholds** chosen to equalise TPR (Hardt et al. 2016).

![Two groups with one shared threshold have different TPRs; lowering group B's threshold equalises TPR but raises its FPR](../../Attachments/ML%20Animations/Explainability%20and%20Fairness%20-%20group%20thresholds.gif)
*Watch group B's threshold slide left: the green shaded area (qualified people accepted) grows until $\mathrm{TPR}_B=\mathrm{TPR}_A$, but because B's scores are less informative, its false-positive rate climbs too. Equal opportunity is bought, not free.*

## Worked example
**Shapley values for two features.** $v(\emptyset)=0$, $v(\{1\})=4$, $v(\{2\})=2$, $v(\{1,2\})=8$. Two orders, each with weight $\tfrac12$:
- Feature 1: added first contributes $4-0=4$; added second contributes $8-2=6$. $\phi_1=\tfrac12(4+6)=5$.
- Feature 2: first $2-0=2$; second $8-4=4$. $\phi_2=\tfrac12(2+4)=3$.
Check efficiency: $\phi_1+\phi_2=8=v(\{1,2\})-v(\emptyset)$. The interaction bonus ($8>4+2$) was split equally.

**Fairness metrics.** 100 people per group:

| Group | TP | FP | FN | TN | selection rate | TPR | FPR |
|---|---|---|---|---|---|---|---|
| X | 30 | 10 | 10 | 50 | 0.40 | 0.75 | 0.17 |
| Y | 15 | 5 | 15 | 65 | 0.20 | 0.50 | 0.07 |

Demographic parity difference $0.20$ (ratio $0.5$, fails the 80 % rule); equal-opportunity gap $0.25$ in TPR; FPRs differ too, so equalised odds also fails.

**Counterfactual.** Approve if $2x_1+x_2-5\ge0$. Applicant $x=(1,1)$ scores $-2$. $x'=x+\frac{2}{5}(2,1)=(1.8,1.4)$, which scores exactly 0: the minimal change raises $x_1$ by 0.8 and $x_2$ by 0.4.

## Common confusions
- **"Removing the protected attribute makes the model fair."** → Proxies carry the same information ("fairness through unawareness" fails); and you need the attribute to *measure* fairness.
- **"Feature importance = causal effect."** → Importance describes the *model*, not the world. A feature can matter to the model only because it correlates with the true cause ([[Causal Inference]]).
- **"Low permutation importance means the feature is irrelevant."** → It may be redundant with a correlated feature; drop both and the score may collapse.
- **"LIME and SHAP give the truth about the model."** → They are approximations with assumptions (sampling, background data, feature independence); check stability, and sanity-check against simple baselines.
- **"There is one correct fairness metric."** → The criteria are mutually incompatible when base rates differ; the choice depends on which harms (false positives or false negatives, for whom) matter in the context.
- **"Calibrated models are fair."** → Calibration within groups can coexist with very different FPRs/FNRs across groups.

## Check yourself
> [!question]- Name the method and its scope: "Which features matter most to my gradient-boosted model across the whole test set?"
> Permutation importance or mean $|\text{SHAP}|$ (TreeSHAP): global; TreeSHAP is model-specific, permutation importance is model-agnostic.

> [!question]- What does the efficiency axiom of SHAP guarantee?
> The feature contributions sum exactly to the prediction minus the baseline: $f(x)=\phi_0+\sum_i\phi_i$.

> [!question]- What is the SHAP value of feature $j$ in a linear model with independent features?
> $\phi_j=w_j\,(x_j-E[x_j])$: the weight times how far this input is from the average.

> [!question]- Two groups have base rates 0.3 and 0.6. Can a classifier have equal PPV, equal TPR and equal FPR across them?
> Not unless it is perfect: by $\text{FPR}=\frac{p}{1-p}\frac{1-\text{PPV}}{\text{PPV}}\text{TPR}$, equal PPV and TPR with different $p$ force different FPRs.

> [!question]- Give one example each of a proxy and a feedback loop.
> Proxy: postcode standing in for ethnicity in credit scoring. Feedback loop: a recommender promoting already-popular items, whose extra clicks are fed back as evidence that they are popular.

## Practice
[Explainability and Fairness - Exercises](Explainability%20and%20Fairness%20-%20Exercises.ipynb): placing methods on the global/local map, sources of bias, permutation importance with correlated features, LIME vs SHAP, Shapley values by hand and by enumeration, SHAP for linear models, group fairness metrics, the impossibility identity, counterfactuals, PDP/ICE, a LIME-style surrogate, group thresholds for equal opportunity and reweighing.

## Learn more
- [Molnar — *Interpretable Machine Learning* (free)](https://christophm.github.io/interpretable-ml-book/)
- [Barocas, Hardt, Narayanan — *Fairness and Machine Learning* (free)](https://fairmlbook.org/)
- Papers: [SHAP — Lundberg & Lee 2017](https://arxiv.org/abs/1705.07874) · [LIME — Ribeiro et al. 2016](https://arxiv.org/abs/1602.04938) · [Equality of Opportunity — Hardt et al. 2016](https://arxiv.org/abs/1610.02413) · [Fair prediction with disparate impact — Chouldechova 2017](https://arxiv.org/abs/1703.00056)
- [Fairlearn](https://fairlearn.org/) · [SHAP library](https://github.com/shap/shap)
