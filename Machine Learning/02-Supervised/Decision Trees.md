---
tags: [ml, supervised, trees]
---
# Decision Trees

> [!summary] In one sentence
> A decision tree predicts by asking a sequence of yes/no questions about the features ("is $x_1\le 4$?"), and it is grown by recursive partitioning: at every node, pick the split that best reduces impurity, then repeat inside each half.

## Intuition first

Think of the game *20 Questions*, or a doctor's triage flowchart: "Fever? → yes → Rash? → no → …". Each question cuts the set of possibilities in two, and a good question is one that leaves each half as *pure* as possible (ideally all patients in a branch have the same diagnosis). A decision tree is exactly that flowchart, learned from data.

Growing one is a **greedy, top-down** procedure:
1. Start with all training points in one node.
2. Try every feature and every threshold; measure how mixed ("impure") the two resulting children are.
3. Keep the split that reduces impurity the most, and recurse into each child.
4. Stop when a node is pure, too small, or too deep; the leaf predicts the majority class (classification) or the mean (regression).

**What problem does it solve?** It gives a model you can *read*: every prediction is a short chain of human-checkable rules. It needs almost no preprocessing (no scaling, mixed feature types are fine) and captures interactions automatically ("if income is high *and* age is low …"). Its weakness, high variance, is precisely what [[Ensemble Methods]] (Random Forest, Gradient Boosting) fix, which is why trees are the building block of the strongest models for tabular data.

![A depth-2 tree growing: each split draws a line in feature space and a node in the tree](../../Attachments/ML%20Animations/Decision%20Trees%20-%20recursive%20splits.gif)
*Watch how each node of the tree on the right is one axis-aligned cut on the left: the root cut $x_1\le4$ drops the Gini impurity from 0.50 to 0.33, then each half is split again on $x_2$ until every rectangle is pure.*

## The math, step by step

### Impurity of a node
Let $p_k$ be the fraction of points in the node that belong to class $k$ (out of $K$ classes).

| Criterion | Formula |
|---|---|
| Entropy | $-\sum p_k\log_2p_k$ |
| Gini | $1-\sum p_k^2$ |
| Variance (regression) | $\frac1n\sum(y-\bar y)^2$ |

What they mean in words:
- **Entropy** ([[Information Theory]]) is the average number of bits needed to encode the class of a random point from the node. Pure node: 0 bits. 50/50 with two classes: 1 bit. With $K$ classes it is at most $\log_2K$, reached by the uniform distribution.
- **Gini** is the probability that two points drawn at random (with replacement) from the node have *different* labels: $\sum_k p_k(1-p_k)=1-\sum_kp_k^2$. Pure: 0; maximum $1-1/K$ at uniform.
- **Variance** is the regression analogue: the mean squared error you make if the leaf predicts the node mean $\bar y$.
- **Misclassification error** $1-\max_kp_k$ also measures impurity, but it is *not* used for growing trees: it is piecewise linear, so many different splits give the same score (it is not strictly concave). Entropy and Gini are strictly concave and reward splits that create a very pure child even when the error count does not change. It is, however, a sensible criterion for pruning.

### Information gain
Split a parent node $S$ into children $S_1,\dots,S_V$. The quality of the split is

$$\text{Gain}=I(S)-\sum_{v}\frac{|S_v|}{|S|}\,I(S_v),$$

**Information gain** = parent impurity − weighted child impurity ([[Information Theory]]). The weights $|S_v|/|S|$ matter: a tiny pure child should not count as much as a big one. With entropy as $I$ this is literally the mutual information between the split and the label.

### Gain ratio (C4.5)
Plain information gain loves attributes with many values: a "customer ID" column splits the data into $N$ pure singletons, so its gain is maximal, yet it is useless for new customers. C4.5 divides by the information in the split itself:

$$\text{GainRatio}=\frac{\text{Gain}}{\text{SplitInfo}},\qquad \text{SplitInfo}=-\sum_v\frac{|S_v|}{|S|}\log_2\frac{|S_v|}{|S|}.$$

A split into many tiny branches has a large SplitInfo, which cancels its inflated gain.

### The three classic algorithms
ID3 uses gain, C4.5 uses gain ratio, CART uses Gini and binary splits. CART (what scikit-learn implements) only ever asks "is $x_j\le t$?", trying every midpoint between consecutive sorted values of every feature; regression trees use the variance criterion.

### Why greedy?
Finding the *smallest* or *most accurate* tree is NP-hard, so trees are grown greedily and a split is never revisited. Greedy can be myopic: on XOR data ($y=x_1\oplus x_2$) every single split on $x_1$ or $x_2$ at the root has gain 0, even though a depth-2 tree is perfect.

## Worked example

**Classification.** 8 emails, 4 spam (+) and 4 not (−). Two candidate splits:
- "contains *free*": yes $(3+,1-)$, no $(1+,3-)$
- "has attachment": yes $(2+,2-)$, no $(2+,2-)$

Parent: entropy $=-\tfrac12\log_2\tfrac12-\tfrac12\log_2\tfrac12=1$ bit; Gini $=1-(\tfrac14+\tfrac14)=0.5$.

Split on *free*: each child has $p=(\tfrac34,\tfrac14)$, entropy $=-\tfrac34\log_2\tfrac34-\tfrac14\log_2\tfrac14=0.311+0.5=0.811$, Gini $=1-(\tfrac9{16}+\tfrac1{16})=0.375$. Both children have 4 of the 8 points, so the weighted impurity equals the child impurity. Gain $=1-0.811=0.189$ bits; Gini decrease $=0.5-0.375=0.125$.

Split on *attachment*: both children are still 50/50, gain $=0$. CART picks *free*.

**Regression.** $x=(1,2,3,4)$, $y=(2,4,10,12)$. Parent mean 7, variance $\tfrac14(25+9+9+25)=17$. Threshold $2.5$: left $\{2,4\}$ (mean 3, variance 1), right $\{10,12\}$ (mean 11, variance 1), weighted variance $\tfrac24\cdot1+\tfrac24\cdot1=1$. Threshold $1.5$: left $\{2\}$ (variance 0), right $\{4,10,12\}$ (mean 8.67, variance 11.56), weighted $\tfrac34\cdot11.56=8.67$. So $t=2.5$ wins, and the two leaves predict 3 and 11.

## Controlling overfitting
Max depth, min samples per leaf, **cost-complexity pruning**, validation pruning.

A fully grown tree keeps splitting until every leaf is pure, so it reaches 100% training accuracy by memorising noise. Two families of fixes:

- **Pre-pruning (early stopping)**: `max_depth`, `min_samples_leaf`, `min_samples_split`, `min_impurity_decrease`. Cheap, but may stop too early (remember XOR: a useless-looking split can enable great splits below it).
- **Post-pruning**: grow the full tree, then cut back.
  - *Cost-complexity (weakest-link) pruning* (CART): minimise $R_\alpha(T)=R(T)+\alpha|T|$, where $R(T)$ is the training error and $|T|$ the number of leaves. For each internal node $t$ with subtree $T_t$, collapsing it to a leaf costs $R(t)-R(T_t)$ more error but saves $|T_t|-1$ leaves, so it becomes worthwhile once $\alpha\ge\alpha_{\text{eff}}(t)=\frac{R(t)-R(T_t)}{|T_t|-1}$. Repeatedly pruning the node with the smallest $\alpha_{\text{eff}}$ gives a nested sequence of trees; choose $\alpha$ (`ccp_alpha` in scikit-learn) by [[Cross-Validation and Model Selection|cross-validation]].
  - *Validation (reduced-error) pruning*: replace a subtree by a leaf whenever that does not hurt accuracy on a held-out set.

## Pros / cons
+ interpretable, handles mixed types and missing values, no scaling needed
− unstable (high variance), axis-aligned boundaries

Why each one holds:
- **Interpretable**: a shallow tree is a readable rule list; you can trace any prediction.
- **No scaling needed**: a split $x_j\le t$ depends only on the *order* of values, so any monotone rescaling of a feature gives the same tree.
- **Mixed types**: numeric features use thresholds, categorical ones use subsets of categories; nothing needs to share a unit.
- **Missing values**: CART can use *surrogate splits* (another feature that mimics the chosen split) and newer implementations learn which side missing values go to.
- **Unstable / high variance**: a small change in the data can change the root split, and everything below it changes too. Train trees on bootstrap resamples and you will see different root features and many disagreeing predictions ([[Bias-Variance Tradeoff]]).
- **Axis-aligned boundaries**: every cut is perpendicular to an axis, so a diagonal boundary like $x_1>x_2$ becomes a staircase that needs many leaves; one engineered feature $x_1-x_2$ would need a single split ([[Feature Engineering]]).

Fix variance with [[Ensemble Methods]] (Random Forest, Gradient Boosting).

## Common confusions
- *"Trees find the best tree."* → They find a greedy one; each split is locally optimal and never revisited.
- *"Higher information gain always means a better attribute."* → Not for many-valued attributes like IDs; that is why C4.5 uses the gain ratio.
- *"Training accuracy of 100% is good news."* → For a fully grown tree it is the default and signals overfitting; look at validation accuracy and prune.
- *"Gini and entropy give very different trees."* → In practice they almost always pick the same splits; Gini is slightly cheaper (no logarithm).
- *"Feature scaling helps trees."* → It does nothing; only the ordering of values matters. (It matters a lot for [[k-Nearest Neighbors]] or [[Support Vector Machines]].)

## Check yourself

> [!question]- A node has 3 classes in proportions $(\tfrac13,\tfrac13,\tfrac13)$. What are its entropy and Gini?
> Entropy $=\log_23\approx1.585$ bits, Gini $=1-3\cdot\tfrac19=\tfrac23$; both are the maxima for $K=3$.

> [!question]- Why is weighted *child* impurity used, not the plain average?
> A child holding 2 points should not matter as much as one holding 200; weighting by $|S_v|/|S|$ measures the expected impurity of a random point after the split.

> [!question]- In cost-complexity pruning, what happens as $\alpha$ grows from 0 to $\infty$?
> $\alpha=0$ keeps the full tree; larger $\alpha$ penalises leaves more, so subtrees are collapsed in order of their $\alpha_{\text{eff}}$, until only the root (a single leaf) remains.

> [!question]- Why do trees struggle with the boundary $x_1=x_2$?
> Each split is axis-aligned, so a diagonal is approximated by a staircase that needs many leaves (and data) to be accurate.

> [!question]- Why does ID3 love a "customer ID" attribute, and how does C4.5 fix it?
> Splitting on ID gives one pure leaf per customer, so the gain equals the parent entropy (maximal). C4.5 divides by SplitInfo, which is $\log_2N$ for $N$ equal branches, so the ratio becomes small.

## Practice
[Decision Trees - Exercises](Decision%20Trees%20-%20Exercises.ipynb): greedy vs optimal, why not misclassification error, gain ratio; by hand: entropy and Gini of a node, information gain, gain ratio, a regression split, weakest-link pruning, impurity bounds; in code: impurity functions, exhaustive split search, a recursive CART, depth vs overfitting, cost-complexity pruning, instability and axis-aligned staircases.

## Learn more
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 8
- [scikit-learn – decision trees](https://scikit-learn.org/stable/modules/tree.html)
- [StatQuest videos](https://statquest.org/video_index.html)
- [R2D3 – A visual introduction to machine learning](http://www.r2d3.us/visual-intro-to-machine-learning-part-1/): a scrolling animation of a tree splitting houses in San Francisco vs New York
