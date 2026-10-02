---
tags: [ml, theory, masters]
---
# Learning Theory

> [!summary] In one sentence
> Learning theory explains **why** a model that does well on its training data should also do well on unseen data, and tells you how much data you need, by bounding the gap between empirical risk and true risk in terms of the size or *capacity* of the hypothesis class.

Why do models generalise from training to test data?

## Intuition first

Imagine a student preparing for an exam with a stack of 50 past questions. If they genuinely learn the method, they will do well on *new* questions too. If they simply memorise the 50 answers, they will ace the practice set and fail the exam. Learning theory is the mathematics of telling these two situations apart *before* you see the exam.

Two forces fight each other:

- **Luck shrinks with data.** A score measured on $N$ random examples is a noisy estimate of the "real" score. The more examples, the less noise (this is what concentration inequalities such as Hoeffding make precise).
- **Choice creates optimism.** A learner does not evaluate *one* hypothesis; it searches a whole class $\mathcal H$ and picks the one that looks best on the training data. The more hypotheses it can choose from, the more likely one of them looks good *by luck*. So the bound must pay a price for the "size" of $\mathcal H$: $\ln|\mathcal H|$ for finite classes, the **VC dimension** or the **Rademacher complexity** for infinite ones.

Every result in this note has the same shape:

$$
\underbrace{R(h)}_{\text{true error}} \;\le\; \underbrace{\hat R(h)}_{\text{training error}} \;+\; \underbrace{\text{(capacity of }\mathcal H\text{)}\big/\text{(amount of data)}}_{\text{generalisation gap}}
$$

and the whole subject is about making that last term small and honest.

![A single fixed classifier evaluated on 60 test sets: as N grows, the test errors squeeze into the band R ± epsilon](../../Attachments/ML%20Animations/Learning%20Theory%20-%20Hoeffding%20concentration.gif)

*Watch the red dots (test sets whose error lands more than $\epsilon$ from the truth) disappear as $N$ grows, while the Hoeffding bound $2e^{-2N\epsilon^2}$ falls towards zero.*

## Core concepts

- **Empirical vs. true risk**: $\hat R(h)=\frac1N\sum\ell(h(x_i),y_i)$ vs. $R(h)=\mathbb E[\ell(h(x),y)]$. ERM minimises $\hat R$.
- **PAC learning**: with probability $\ge1-\delta$, error $\le\epsilon$ after $m(\epsilon,\delta)$ samples.
- **Finite hypothesis class**: $m\ge\frac{1}{\epsilon}\big(\ln|\mathcal H|+\ln\frac1\delta\big)$ in the realisable case.
- **VC dimension**: the largest set the class can shatter. Linear classifiers in $\mathbb R^d$ have VC $=d+1$. Generalisation gap $\approx O\big(\sqrt{\frac{\mathrm{VC}\,\log N}{N}}\big)$.
- **Rademacher complexity**: data-dependent capacity measure; gives tighter bounds.
- **No Free Lunch**: averaged over all problems, no learner is best, so inductive bias is necessary.
- **Bias–complexity trade-off**: approximation error vs. estimation error ([[Bias-Variance Tradeoff]]).
- **Margins**: generalisation bounds that depend on the margin, not the dimension, explain why SVMs work ([[Support Vector Machines]]).
- **Concentration inequalities**: Hoeffding, McDiarmid, union bound.
- **Modern puzzles**: over-parameterised networks still generalise; double descent; implicit regularisation of SGD; the neural tangent kernel.

The sections below unpack each bullet.

## The math, step by step

### 1. Empirical risk vs. true risk

$$\hat R(h)=\frac1N\sum_{i=1}^N\ell(h(x_i),y_i)\qquad\text{vs.}\qquad R(h)=\mathbb E_{(x,y)\sim\mathcal D}\big[\ell(h(x),y)\big]$$

- $h$ is a hypothesis (a trained model), $\ell$ a loss (e.g. 0–1 loss: 1 if wrong, 0 if right), $(x_i,y_i)$ are $N$ i.i.d. samples from the unknown distribution $\mathcal D$.
- $\hat R$ is what you *can* compute (the training or test error); $R$ is what you *care about* (the error on the whole population).
- **ERM** (empirical risk minimisation) returns $\hat h=\arg\min_{h\in\mathcal H}\hat R(h)$.

In words: for a hypothesis fixed **before** looking at the data, $\hat R(h)$ is an unbiased estimate of $R(h)$, because $\mathbb E[\hat R(h)]=\frac1N\sum_i\mathbb E[\ell(h(x_i),y_i)]=R(h)$. For the ERM output $\hat h$ it is **biased downwards**: $\hat h$ was chosen *because* its training error is low, partly by fitting noise. That bias is the generalisation gap $R(\hat h)-\hat R(\hat h)$.

### 2. Concentration: Hoeffding and the union bound

**Hoeffding's inequality.** For a fixed $h$ and a loss in $[0,1]$,

$$P\big(|\hat R(h)-R(h)|>\epsilon\big)\le 2e^{-2N\epsilon^2}.$$

In words: the probability that an average of $N$ bounded i.i.d. terms is more than $\epsilon$ away from its mean decays *exponentially* in $N\epsilon^2$. Setting the right-hand side to $\delta$ and solving gives the test-set size you need:
$N\ge\frac{\ln(2/\delta)}{2\epsilon^2}$.

**Union bound.** For any events, $P(A_1\cup\dots\cup A_k)\le\sum_j P(A_j)$. Apply it to the events "hypothesis $h_j$ is misleading" and you get a statement about *all* hypotheses at once (a **uniform** bound):

$$P\big(\exists h\in\mathcal H: |\hat R(h)-R(h)|>\epsilon\big)\le 2|\mathcal H|e^{-2N\epsilon^2}
\;\;\Longrightarrow\;\; N\ge\frac{\ln|\mathcal H|+\ln(2/\delta)}{2\epsilon^2}.$$

This is the **agnostic** finite-class bound (no assumption that a perfect $h$ exists). Because it holds for every $h$ simultaneously, it also holds for whichever $\hat h$ ERM picks.

**McDiarmid's inequality** generalises Hoeffding from averages to any function $f(x_1,\dots,x_N)$ whose value changes by at most $c_i$ when you change the $i$-th input: $P\big(f-\mathbb E f\ge t\big)\le\exp\!\big(-2t^2/\sum_i c_i^2\big)$. It is the tool behind Rademacher bounds.

### 3. PAC learning and the finite-class bound

**PAC** ("probably approximately correct"): an algorithm PAC-learns $\mathcal H$ if, for every $\epsilon,\delta$, after $m(\epsilon,\delta)$ samples it outputs $h$ with $R(h)\le\epsilon$ (*approximately correct*) with probability $\ge1-\delta$ (*probably*).

**Derivation of the realisable bound** (some $h\in\mathcal H$ has $R(h)=0$; ERM returns any hypothesis consistent with the data). Call $h$ *bad* if $R(h)>\epsilon$.

1. A single bad $h$ is correct on one random sample with probability $<1-\epsilon$.
2. Samples are independent, so it is consistent with all $m$ of them with probability $<(1-\epsilon)^m\le e^{-\epsilon m}$ (using $1-x\le e^{-x}$).
3. Union bound over at most $|\mathcal H|$ bad hypotheses: $P(\text{some bad }h\text{ is consistent})\le|\mathcal H|e^{-\epsilon m}$.
4. Require $|\mathcal H|e^{-\epsilon m}\le\delta$ and take logs:

$$m\ge\frac{1}{\epsilon}\Big(\ln|\mathcal H|+\ln\frac1\delta\Big).$$

In words: the data needed grows only **logarithmically** in the number of hypotheses and in $1/\delta$, but linearly in $1/\epsilon$. In the agnostic case (section 2) the dependence worsens to $1/\epsilon^2$.

### 4. VC dimension and shattering

For infinite classes (all lines, all thresholds) $\ln|\mathcal H|=\infty$, so we need a better notion of size. What matters is not how many hypotheses exist but how many **different labellings** they can produce on $N$ points.

- $\mathcal H$ **shatters** a set of points if it can realise *all* $2^n$ labellings of them.
- The **VC dimension** is the size of the largest set that $\mathcal H$ can shatter.

![Straight lines realise all 8 labellings of 3 points, but no line separates the 4-point XOR labelling](../../Attachments/ML%20Animations/Learning%20Theory%20-%20VC%20shattering.gif)

*Watch the counter reach 8/8 for three points; then a rotating line fails to split the XOR pattern, which is why lines in the plane have VC dimension 3.*

Examples (to show VC $=k$ you need *one* set of size $k$ that is shattered and an argument that *no* set of size $k+1$ is):
- Thresholds $\mathbb 1[x\ge t]$ on $\mathbb R$: VC $=1$ (for $x_1<x_2$ the labelling $(1,0)$ is impossible).
- Intervals $\mathbb 1[a\le x\le b]$: VC $=2$ (for three points, $(1,0,1)$ is impossible).
- Linear classifiers $\mathrm{sign}(w^\top x+b)$ in $\mathbb R^d$: VC $=d+1$, so $3$ in the plane.

The VC bound says that, with probability $\ge1-\delta$, for all $h\in\mathcal H$ the gap is roughly
$O\big(\sqrt{\frac{\mathrm{VC}\,\log N}{N}}\big)$ (plus a $\sqrt{\ln(1/\delta)/N}$ term). In words: you need a number of samples proportional to the VC dimension, i.e. to the number of "effective parameters". The key step (Sauer's lemma) is that a class of VC dimension $d_{VC}$ produces at most $O(N^{d_{VC}})$ labellings of $N$ points, polynomial instead of $2^N$, so the union bound pays $\ln N^{d_{VC}}=d_{VC}\ln N$.

### 5. Rademacher complexity

$$\hat{\mathfrak R}_n(\mathcal H)=\mathbb E_\sigma\Big[\sup_{h\in\mathcal H}\frac1n\sum_{i=1}^n\sigma_i h(x_i)\Big],\qquad\sigma_i\in\{\pm1\}\text{ uniform}.$$

In words: draw random $\pm1$ labels $\sigma_i$ ("pure noise") and ask how well the best $h$ in the class can correlate with them *on your actual sample*. A class that can fit noise well is a high-capacity class. It is **data-dependent**: it uses the real $x_i$, so it is usually tighter than VC. A typical bound (loss in $[0,1]$, with probability $\ge1-\delta$, for all $h$):
$R(h)\le\hat R(h)+2\,\mathfrak R_n+\sqrt{\frac{\ln(1/\delta)}{2n}}$, where $\mathfrak R_n$ is the Rademacher complexity of the loss class. **Massart's lemma** links it to counting: if the class produces at most $L$ labellings of the sample, $\hat{\mathfrak R}_n\le\sqrt{2\ln L/n}$ (for thresholds $L=n+1$). Values shrink roughly like $1/\sqrt n$.

### 6. Approximation vs. estimation error

Let $h^\star$ be the Bayes-optimal predictor and $h_{\mathcal H}=\arg\min_{h\in\mathcal H}R(h)$ the best member of the class. Add and subtract $R(h_{\mathcal H})$:

$$R(\hat h)-R(h^\star)=\underbrace{R(h_{\mathcal H})-R(h^\star)}_{\text{approximation error}}+\underbrace{R(\hat h)-R(h_{\mathcal H})}_{\text{estimation error}}.$$

- A **bigger** $\mathcal H$ lowers (or keeps) the approximation error but raises the estimation error (more ways to overfit).
- **More data** leaves the approximation error unchanged and lowers the estimation error.

This is the bias–complexity trade-off, the theory version of [[Bias-Variance Tradeoff]].

## Worked example

**Finite class, realisable.** $|\mathcal H|=100$ hypotheses, target $\epsilon=0.1$, $\delta=0.05$.
$\ln 100\approx4.605$, $\ln 20\approx2.996$, sum $7.601$, divide by $0.1$: $m\ge76.01$, so **77 samples**.

**How big a test set?** One fixed model, want $|\hat R-R|\le0.1$ with 95% confidence:
$N\ge\frac{\ln(2/0.05)}{2\cdot0.1^2}=\frac{3.689}{0.02}=184.4$, so **185 test samples**. Halving $\epsilon$ to $0.05$ multiplies this by 4.

**Shattering by hand.** Three non-collinear points $A,B,C$ and lines: the labelling "all $+$" uses a line far away; "only $A$ is $+$" uses a line cutting $A$ off; "$A,B$ are $+$" is the same line with the sides swapped. By symmetry all $2^3=8$ labellings work. Four points in a square with diagonal labels ($+,-,+,-$) cannot be separated by any line, and every 4-point configuration has some such bad labelling, so VC $=3=d+1$.

## No Free Lunch and inductive bias

Averaged over *all* possible labelling functions, every learner has the same expected error on points it has not seen. This does **not** make ML pointless: the uniform average is dominated by structureless noise functions we never meet. Real problems have structure, and a learner wins when its **inductive bias** matches that structure: $k$-NN assumes nearby points share labels, linear regression assumes an (approximately) linear relationship, a [[CNN]] assumes locality and translation invariance.

## Margins: why SVMs escape the dimension

The VC dimension of linear classifiers grows with $d$, yet SVMs with huge (even infinite, via kernels) feature spaces generalise. The reason is the **margin** $\gamma$. The perceptron mistake bound shows the flavour: if $\lVert x_i\rVert\le R$ and some unit vector separates the data with margin $y_iw^{\star\top}x_i\ge\gamma$, the perceptron makes at most $(R/\gamma)^2$ mistakes. Proof sketch: after $k$ mistakes $k\gamma\le w_k^\top w^\star\le\lVert w_k\rVert\le\sqrt kR$, so $k\le R^2/\gamma^2$. No dimension appears. Similarly, the effective capacity of large-margin linear classifiers scales like $R^2/\gamma^2$, which is why maximising the margin ([[Support Vector Machines]]) is a capacity control.

## Modern puzzles

A ResNet with 25 M parameters can reach zero training error on 50 000 images and still generalise, although its VC dimension makes classical bounds vacuous. Partial explanations:

- **Implicit regularisation of SGD**: among the many interpolating solutions, (S)GD from small initialisation tends to find low-norm, "flat" ones, so the effective capacity is far below the parameter count.
- **Data- and norm-dependent bounds** (Rademacher, margin, PAC-Bayes) can be small even when the VC dimension is huge.
- **Neural tangent kernel**: very wide networks trained by gradient descent behave like kernel regression with a fixed kernel ([[Kernel Methods]]), whose generalisation is governed by norms rather than parameter count.
- **Double descent**: test error first follows the classic U-shape as capacity grows, peaks at the **interpolation threshold** (parameters $\approx$ samples, where the model can just barely fit the noise and needs enormous weights), and then *descends again* as more parameters let the minimum-norm interpolant become smoother.

## Common confusions

- *"Low training error means a good model."* → Only if the capacity term is small relative to $N$. ERM's training error is optimistically biased.
- *"VC dimension = number of parameters."* → Often close for linear models ($d+1$), but not in general: $\sin(\omega x)$ has one parameter and infinite VC dimension.
- *"To show VC $=k$ I must shatter every set of size $k$."* → No: **one** shattered set of size $k$ suffices, but **no** set of size $k+1$ may be shattered.
- *"Hoeffding applies to my best-of-20 test score."* → It applies only to a hypothesis fixed before seeing the test data. Selecting on the test set needs a union bound ([[Common Pitfalls]]).
- *"No Free Lunch says all algorithms are equally good."* → Only averaged over all possible problems, most of which are noise. On structured real problems, matching inductive bias wins.
- *"Bounds are useless because they are loose."* → They are often loose by constants, but they predict the right **scalings** ($\sqrt{1/N}$, $\ln|\mathcal H|$, $R^2/\gamma^2$), which guide design.

## Check yourself

> [!question]- Why is $\hat R(\hat h)$ of the ERM solution typically smaller than $R(\hat h)$, even though $\hat R(h)$ is unbiased for any fixed $h$?
> Because $\hat h$ depends on the data: it was selected for having low training error, which partly reflects the noise in this particular sample. Picking the minimum of many noisy estimates is biased downwards.

> [!question]- How does the required sample size change if you square the size of a finite hypothesis class?
> $\ln|\mathcal H|^2=2\ln|\mathcal H|$, so the $\ln|\mathcal H|$ term doubles. The dependence is logarithmic, which is why even huge finite classes are learnable.

> [!question]- What is the VC dimension of intervals $\mathbb 1[a\le x\le b]$ on the real line, and why?
> 2. Two points can get all four labellings, but for $x_1<x_2<x_3$ the labelling $(1,0,1)$ needs a gap inside the interval, which is impossible.

> [!question]- Which error term does collecting more data reduce: approximation or estimation?
> Estimation error. Approximation error depends only on how good the best member of $\mathcal H$ is, not on the data.

> [!question]- Why can an SVM in an infinite-dimensional feature space still generalise?
> Its capacity is controlled by the margin: margin-based bounds scale like $R^2/\gamma^2$ and do not depend on the dimension.

## Practice

[Learning Theory - Exercises](Learning%20Theory%20-%20Exercises.ipynb): finite-class and Hoeffding sample sizes by hand, deriving the bounds, VC dimension of simple classes, brute-force shattering with an LP, Rademacher complexity of thresholds, the ERM generalisation gap and double descent with random features.

## Learn more
- [Shalev-Shwartz & Ben-David — *Understanding Machine Learning* (free PDF)](https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning/understanding-machine-learning-theory-algorithms.pdf)
- [Stanford STATS214 / CS229M — Machine Learning Theory](https://web.stanford.edu/class/stats214/)
- [CS229 cheatsheet — learning theory section](https://stanford.edu/~shervine/teaching/cs-229/cheatsheet-supervised-learning/)
- [Caltech *Learning From Data* (Abu-Mostafa) — free lecture videos on VC theory](https://work.caltech.edu/telecourse.html)
