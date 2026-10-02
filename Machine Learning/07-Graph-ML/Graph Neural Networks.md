---
tags: [ml, graph, deep-learning]
---
# Graph Neural Networks

**Message passing**: for node $v$ at layer $k$
$$h_v^{(k)}=\mathrm{UPDATE}\Big(h_v^{(k-1)},\ \mathrm{AGG}\big(\{h_u^{(k-1)}:u\in N(v)\}\big)\Big)$$

| Model | Aggregation |
|---|---|
| **GCN** | $H'=\sigma(\tilde D^{-1/2}\tilde A\tilde D^{-1/2}HW)$ |
| **GraphSAGE** | sample neighbours; mean/LSTM/pool |
| **GAT** | learned attention weights ([[Transformers]]) |
| **GIN** | sum + MLP; as expressive as 1-WL test |

- Readout for graph-level tasks: sum/mean/attention pooling.
- Issues: **over-smoothing** (deep GNNs), over-squashing, scalability (mini-batching, sampling).
- Libraries: PyTorch Geometric, DGL ([[Tools and Libraries]]).

Used for [[Link Prediction]] and node/graph classification. Overview: [[Graph ML Overview]].

## Learn more
- [Hamilton – Graph Representation Learning (free)](https://www.cs.mcgill.ca/~wlh/grl_book/) ch. 5–7
- [Stanford CS224W](https://web.stanford.edu/class/cs224w/)
- [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/)
- [GCN](https://arxiv.org/abs/1609.02907)
- [GAT](https://arxiv.org/abs/1710.10903)
