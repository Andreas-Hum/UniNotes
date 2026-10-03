---
tags: [ml, project, gnn, semi-supervised]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - GCN from Scratch

> [!summary] In one sentence
> Implement the renormalised adjacency and a graph convolution layer, then classify all 34 karate-club members from just two labels (the instructor and the president).

**Notebook:** [Project - GCN from Scratch](Project%20-%20GCN%20from%20Scratch.ipynb) · topic: [[Graph Neural Networks]] · all projects: [[Projects Overview]]

## What you build
1. `normalize_adjacency`: $\hat D^{-1/2}(A+I)\hat D^{-1/2}$.
2. `GCNLayer.forward`: $\tilde AHW$.

## Reference results (solution, laptop CPU)
2-layer GCN (34 → 16 → 2), one-hot node IDs as features, 200 epochs: **97.1 %** of members correct, identical over 5 seeds (one member misclassified).

## Check yourself
> [!question]- Why add self-loops?
> Without them a node's new representation only averages its neighbours and forgets its own features.

> [!question]- How can two labels classify 34 nodes?
> Each layer mixes information from 1-hop neighbours, so 2 layers spread the label signal 2 hops, and the training loss on the two labelled nodes shapes embeddings that the whole community shares (homophily).

## Learn more
- [Kipf & Welling – Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)

---
Back to [[00 - Machine Learning Index]].
