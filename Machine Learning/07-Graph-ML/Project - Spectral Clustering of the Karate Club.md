---
tags: [ml, project, spectral, community-detection]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Spectral Clustering of the Karate Club

> [!summary] In one sentence
> Predict how Zachary's karate club split in 1977 from the friendship graph alone, using the sign of the Fiedler vector (2nd eigenvector of the normalised Laplacian).

**Notebook:** [Project - Spectral Clustering of the Karate Club](Project%20-%20Spectral%20Clustering%20of%20the%20Karate%20Club.ipynb) · topic: [[Graph ML Overview]] · all projects: [[Projects Overview]]

## What you build
1. `normalized_laplacian`: $I-D^{-1/2}AD^{-1/2}$.
2. `fiedler_split`: sign of the second-smallest eigenvector.

## Reference results (solution, laptop CPU)
The Fiedler cut matches the real split for **94 %** of the 34 members (only members 2 and 8 are misassigned).

## Check yourself
> [!question]- Why the *second* eigenvector?
> The first eigenvector (eigenvalue 0) is constant (scaled by √degree) and carries no partition. The second minimises a relaxed normalised cut: the smoothest non-trivial signal on the graph, which changes sign where the graph is thinnest.

---
Back to [[00 - Machine Learning Index]].
