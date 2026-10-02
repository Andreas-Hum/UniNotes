---
tags: [ml, unsupervised, clustering]
---
# Clustering

| Algorithm | Idea | Notes |
|---|---|---|
| **k-means** | alternate assign / recompute centroids, minimizes within-cluster SSE | needs $k$, spherical clusters, k-means++ init |
| **k-medoids** | centers are real points | robust |
| **Hierarchical (agglomerative)** | merge closest clusters; single/complete/average/Ward linkage | dendrogram, $O(N^2)$ |
| **DBSCAN** | density-connected points (ε, minPts) | arbitrary shapes, finds noise |
| **Spectral** | eigenvectors of graph Laplacian then k-means | non-convex clusters |
| **GMM** | soft assignments, see [[Gaussian Mixture Models and EM]] | probabilistic |
| **Mean shift** | climb density modes | bandwidth parameter |

## Choosing $k$
Elbow on SSE, silhouette score, gap statistic, BIC for GMM.

## Evaluation
Internal: silhouette, Davies–Bouldin. External: ARI, NMI ([[Model Evaluation and Metrics]]).

## k-means objective
$$J=\sum_i\lVert x_i-\mu_{c(i)}\rVert^2$$
Converges to a local minimum, a hard-assignment special case of EM. Scale features first ([[Data Preprocessing]]).
