---
tags: [ml, graph]
---
# Link Prediction

Predict missing or future edges.

## Heuristics
| Score | Formula |
|---|---|
| Common neighbours | $\lvert N(u)\cap N(v)\rvert$ |
| Jaccard | $\frac{\lvert N(u)\cap N(v)\rvert}{\lvert N(u)\cup N(v)\rvert}$ |
| Adamic–Adar | $\sum_{w}\frac1{\log d_w}$ |
| Preferential attachment | $d_ud_v$ |
| Katz / SimRank / PageRank | path-based, global |

## Learned
- **Shallow embeddings**: score $z_u^\top z_v$ (DeepWalk, node2vec, matrix factorization).
- **GNN encoders** + decoder, SEAL (subgraph-based) → [[Graph Neural Networks]].

## Evaluation
Hide a fraction of edges; sample negative non-edges; report ROC-AUC, AP, Hits@k ([[Model Evaluation and Metrics]]). Avoid leakage: remove test edges from the message-passing graph.

## Learn more
- [Stanford CS224W](https://web.stanford.edu/class/cs224w/)
- [Hamilton – Graph Representation Learning (free)](https://www.cs.mcgill.ca/~wlh/grl_book/) ch. 3
- [SEAL](https://arxiv.org/abs/1802.09691)
- [OGB link prediction benchmarks](https://ogb.stanford.edu/)
