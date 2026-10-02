---
tags: [ml, probabilistic, graphical-models]
---
# Probabilistic Graphical Models

Graph structure encodes conditional independence.

## Bayesian networks (directed)
$p(x_1..x_n)=\prod_i p(x_i\mid\mathrm{pa}(x_i))$. **d-separation** tells which independences hold (chain, fork, collider/explaining away).

## Markov random fields (undirected)
$p(x)=\frac1Z\prod_c\psi_c(x_c)$ over cliques; $Z$ intractable in general.

## Inference
- Exact: variable elimination, belief propagation / junction tree (exponential in treewidth).
- Approximate: [[Variational Inference]], [[MCMC]], loopy BP.

## Learning
Parameters: MLE counts (fully observed) or [[Gaussian Mixture Models and EM|EM]] (latent). Structure: score-based or constraint-based.

## Examples
[[Naive Bayes]], HMM, Kalman filter, LDA topic model, PPCA, mixture models. See your AI notes in [[5-semester/Machine intelligence/Noter små|Noter små]].

## Learn more
- [Bishop – PRML (free PDF)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) ch. 8
- [Murphy – Probabilistic ML (free)](https://probml.github.io/pml-book/)
