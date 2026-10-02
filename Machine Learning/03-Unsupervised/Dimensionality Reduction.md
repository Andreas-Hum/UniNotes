---
tags: [ml, unsupervised, dimensionality-reduction]
---
# Dimensionality Reduction

| Method | Type | Preserves |
|---|---|---|
| [[PCA]] | linear | global variance |
| LDA | linear, supervised | class separation ([[Linear Models for Classification]]) |
| Kernel PCA | non-linear | variance in feature space ([[Kernel Methods]]) |
| MDS / Isomap | non-linear | distances / geodesics |
| **t-SNE** | non-linear | local neighbourhoods; for visualization only |
| **UMAP** | non-linear | local + some global structure |
| Autoencoder | non-linear | reconstruction ([[Generative Models]]) |
| Random projection | linear | distances (Johnson–Lindenstrauss) |

> [!warning]
> Distances and cluster sizes in t-SNE / UMAP plots are not reliable. Do not over-interpret.

Motivation: curse of dimensionality, noise, compression, visualization.
