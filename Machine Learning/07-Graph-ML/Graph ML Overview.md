---
tags: [ml, graph]
---
# Graph ML Overview

Graph $G=(V,E)$ with adjacency $A$, degree $D$, Laplacian $L=D-A$.

## Tasks
- **Node** classification — [[Graph Neural Networks]]
- **Link prediction** — [[Link Prediction]]
- **Graph** classification / regression (molecules)
- Community detection ([[Clustering]], spectral)

## Approaches
1. Hand-crafted features: degree, centrality, PageRank, common neighbours.
2. **Graph kernels**: Weisfeiler–Lehman, random walk ([[Kernel Methods]]).
3. **Shallow embeddings**: DeepWalk, node2vec, matrix factorization.
4. **GNNs**: message passing.

Your lecture notes: [[8-semester/ML/Lecture Notes 1-12|Lectures 8–12]].

## Learn more
- [Stanford CS224W](https://web.stanford.edu/class/cs224w/)
- [Hamilton – Graph Representation Learning (free)](https://www.cs.mcgill.ca/~wlh/grl_book/)
