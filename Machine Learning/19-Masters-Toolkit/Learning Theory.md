---
tags: [ml, theory, masters]
---
# Learning Theory

Why do models generalise from training to test data?

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

## Learn more
- [Shalev-Shwartz & Ben-David — *Understanding Machine Learning* (free PDF)](https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning/understanding-machine-learning-theory-algorithms.pdf)
- [Stanford STATS214 / CS229M — Machine Learning Theory](https://web.stanford.edu/class/stats214/)
- [CS229 cheatsheet — learning theory section](https://stanford.edu/~shervine/teaching/cs-229/cheatsheet-supervised-learning/)
