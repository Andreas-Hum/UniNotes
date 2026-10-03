---
tags: [ml, graph, deep-learning]
status: not-started
notebook: not-started
level:
reviewed:
---
# Graph Neural Networks

> [!summary] In one sentence
> A graph neural network (GNN) gives every node a feature vector and, layer by layer, lets each node collect "messages" from its neighbours and update its vector, so that after $k$ layers each node's representation summarises its $k$-hop neighbourhood.

## Intuition first

Imagine a group chat rumour mill. Each round, everyone hears what their direct friends currently believe, mixes it with their own opinion, and forms a new opinion. After one round you know your friends' views; after two rounds, your friends' friends' views have reached you through them; after many rounds, everyone believes roughly the same thing.

That is exactly a GNN:

- the **opinion** is a node's feature vector $h_v$;
- **listening to friends** is *aggregation* over the neighbourhood $N(v)$;
- **forming a new opinion** is the *update*, a small neural network with learnable weights, shared by every node;
- **rounds** are layers.

Why not just use an MLP on each node? Because it would ignore the edges. Why not a CNN? Because graphs have no grid: nodes have different numbers of neighbours and no natural order. Message passing solves both: aggregations like sum, mean or max work for any number of neighbours and do not care about their order.

![Message passing: one node aggregates its neighbours, then all nodes update and eventually over-smooth](../../Attachments/ML%20Animations/Graph%20Neural%20Networks%20-%20message%20passing%20and%20over-smoothing.gif)

*Watch three things: the ringed node's new value is the mean of itself and its neighbours; the yellow outlines (its receptive field) grow by one hop per layer; and after many layers all colours converge to the same value, which is over-smoothing.*

## The math, step by step

**Message passing**: for node $v$ at layer $k$
$$h_v^{(k)}=\mathrm{UPDATE}\Big(h_v^{(k-1)},\ \mathrm{AGG}\big(\{h_u^{(k-1)}:u\in N(v)\}\big)\Big)$$

Symbol by symbol:
- $h_v^{(0)}=x_v$: the input features of node $v$ (atom type, user profile, bag of words, …).
- $\{h_u^{(k-1)}:u\in N(v)\}$: the *multiset* of neighbour vectors from the previous layer.
- $\mathrm{AGG}$: a **permutation-invariant** function of that multiset (sum, mean, max, attention-weighted sum). It must not depend on the order of neighbours, because there is no natural order; otherwise renumbering the nodes would change the prediction.
- $\mathrm{UPDATE}$: combines the old self-vector with the aggregated message, usually a linear map plus a non-linearity, with weights shared across all nodes. That sharing is why the number of parameters does not depend on the graph size, and why a trained GNN works on new graphs (inductive).

As a whole, a layer is **permutation equivariant**: renumber the nodes and the output vectors are renumbered the same way.

**Receptive field.** After $k$ layers, $h_v^{(k)}$ depends on all nodes within $k$ hops. In a tree where every node has degree $d$, that is $1+d+d(d-1)+\dots$ nodes, so it grows exponentially with $k$. That is the root of both over-squashing and the cost of deep GNNs on big graphs.

## The main architectures

| Model | Aggregation |
|---|---|
| **GCN** | $H'=\sigma(\tilde D^{-1/2}\tilde A\tilde D^{-1/2}HW)$ |
| **GraphSAGE** | sample neighbours; mean/LSTM/pool |
| **GAT** | learned attention weights ([[Transformers]]) |
| **GIN** | sum + MLP; as expressive as 1-WL test |

**GCN**, in detail. $H\in\mathbb R^{n\times d}$ stacks all node vectors as rows, $W\in\mathbb R^{d\times d'}$ is the learnable weight matrix.
1. $\tilde A=A+I$: add self-loops, so a node keeps its own information.
2. $\tilde D$: the degree matrix of $\tilde A$ (degrees + 1).
3. $\hat A=\tilde D^{-1/2}\tilde A\tilde D^{-1/2}$: symmetric normalisation, $\hat A_{uv}=1/\sqrt{\tilde d_u\tilde d_v}$ for neighbours (and self). Without normalisation, high-degree nodes would get huge sums and feature scales would explode with depth.
4. $\hat AH$: each node takes a weighted average of itself and its neighbours (the aggregation), $\cdot\,W$ transforms features, $\sigma$ (e.g. ReLU) adds non-linearity.

Per node: $h_v'=\sigma\big(\sum_{u\in N(v)\cup\{v\}}\frac{1}{\sqrt{\tilde d_u\tilde d_v}}W^\top h_u\big)$. Parameters per layer: $d\cdot d'$ (+ bias), regardless of the graph. **SGC** (simplified GCN) drops the non-linearities: precompute $\hat A^KX$ once, then fit logistic regression, which is surprisingly strong and very fast.

**GraphSAGE.** Samples a fixed number of neighbours per node (so the cost per node is bounded, even for hubs with millions of links) and aggregates them with mean, LSTM or max-pooling. Typically $h_v'=\sigma\big(W[h_v\,\|\,\mathrm{AGG}(h_u)]\big)$: the self-vector is concatenated rather than averaged in. Designed for inductive learning on large graphs (e.g. Pinterest-scale recommendation).

**GAT.** Not all neighbours are equally relevant, so learn the weights:
$$e_{vu}=\mathrm{LeakyReLU}\big(a^\top[Wh_v\,\|\,Wh_u]\big),\qquad \alpha_{vu}=\frac{\exp(e_{vu})}{\sum_{w\in N(v)\cup\{v\}}\exp(e_{vw})},\qquad h_v'=\sigma\Big(\sum_u\alpha_{vu}Wh_u\Big).$$
This is attention as in [[Transformers]], restricted to graph neighbours; multiple heads are concatenated or averaged.

**GIN and expressiveness.** Mean and max lose information: the neighbour multisets $\{1,1\}$ and $\{1\}$ have the same mean and max, but different sums. GIN uses a sum and an MLP, $h_v'=\mathrm{MLP}\big((1+\epsilon)h_v+\sum_{u\in N(v)}h_u\big)$, which makes the aggregation injective on multisets. Result: GIN can distinguish exactly the graphs that the 1-Weisfeiler–Lehman colour-refinement test can, and no message-passing GNN can do better. Flip side: graphs that 1-WL confuses (e.g. two triangles vs one hexagon, both 2-regular) are also indistinguishable for every message-passing GNN.

| Aggregator | Keeps | Good when |
|---|---|---|
| sum | multiset size and content | counting matters (molecules, structure) |
| mean | distribution of neighbour features | degrees vary a lot, features matter more than counts |
| max | presence of a salient feature | "is any neighbour X?" |

## Graph-level tasks, problems and tools

- Readout for graph-level tasks: sum/mean/attention pooling. After the last layer, pool all node vectors into one graph vector, $h_G=\sum_vh_v^{(K)}$ (or mean), and feed it to a classifier. Sum keeps graph size information (useful for molecules: a bigger molecule is different); mean is size-normalised.
- Issues: **over-smoothing** (deep GNNs), over-squashing, scalability (mini-batching, sampling).
  - **Over-smoothing:** each GCN-like layer is a local averaging; repeating it is a power iteration with $\hat A$, which converges to its dominant eigenvector, so after many layers all node vectors become (almost) identical and the classes are no longer separable. Hence most GNNs use only 2–4 layers. Remedies: residual/skip connections, jumping knowledge (concatenate all layers), normalisation, fewer layers.
  - **Over-squashing:** information from an exponentially growing receptive field must squeeze through a fixed-size vector, especially across bottleneck edges, so long-range dependencies get lost. Remedies: graph rewiring, adding virtual nodes, graph transformers.
  - **Scalability:** full-batch training needs the whole graph and all activations in memory. Mini-batching with neighbour sampling (GraphSAGE), cluster-based batching or precomputation (SGC) fix this.
- Libraries: PyTorch Geometric, DGL ([[Tools and Libraries]]).

Used for [[Link Prediction]] and node/graph classification. Overview: [[Graph ML Overview]].

## Worked example

**One GCN layer on a star.** Centre node 0 connected to leaves 1, 2, 3. Scalar features $h=(0,1,2,3)$, $W=1$, no activation.

1. $\tilde A=A+I$; degrees with self-loops: $\tilde d_0=4$, $\tilde d_1=\tilde d_2=\tilde d_3=2$.
2. Entries of $\hat A$: $\hat A_{00}=\frac14$, $\hat A_{0j}=\frac1{\sqrt{4\cdot2}}\approx0.354$, $\hat A_{jj}=\frac12$; leaves are not connected to each other.
3. $h'=\hat Ah$:
   - centre: $\frac14\cdot0+0.354\,(1+2+3)=2.12$;
   - leaf 1: $0.354\cdot0+\frac12\cdot1=0.5$; leaf 2: $1.0$; leaf 3: $1.5$.

The centre absorbed information from all leaves; each leaf is now half itself, half "centre-flavoured".

**GAT attention.** Node $v$ has neighbourhood $\{v,1,2\}$ with raw scores $a^\top[Wh_v\|Wh_u]=(0.5,\ 1.5,\ -2)$.
LeakyReLU (slope 0.2): $(0.5,\ 1.5,\ -0.4)$. Exponentials: $(1.65,\ 4.48,\ 0.67)$, sum $6.80$. Attention weights $\alpha\approx(0.24,\ 0.66,\ 0.10)$: neighbour 1 dominates the new representation.

**Sum vs mean.** Neighbour features $\{1,1,2,2\}$ and $\{1,2\}$: mean 1.5 for both (indistinguishable), sum 6 vs 3 (distinguished).

## Common confusions

- **"More layers = better, like in CNNs."** → Deep plain GNNs over-smooth; 2–4 layers is typical. Depth also expands the receptive field exponentially.
- **"GCN learns a separate weight per edge."** → No. The edge weights $1/\sqrt{\tilde d_u\tilde d_v}$ are fixed by the graph; only $W$ is learned and shared by all nodes. GAT is the variant that learns edge weights (attention).
- **"GNNs can tell apart any two different graphs."** → Message-passing GNNs are at most as powerful as 1-WL; some non-isomorphic graphs (e.g. regular graphs of the same degree) get identical representations.
- **"Self-loops are a detail."** → Without $+I$, a node's new vector ignores its own previous features (only neighbours count).
- **"Mean aggregation is always the safe choice."** → It discards multiset size; for counting-based tasks (how many rings, how many neighbours of type X) sum is needed.

## Check yourself

> [!question]- Why must AGG be permutation invariant?
> Neighbours have no natural order; a node numbering is arbitrary. If AGG depended on order, renumbering the same graph would change the output.

> [!question]- How many parameters does a GCN layer from 64 to 32 features have, and does it depend on the number of nodes?
> $64\cdot32=2048$ weights (+32 bias). No, it is independent of the graph size because $W$ is shared by all nodes.

> [!question]- After 3 layers, which nodes can influence node $v$'s representation?
> All nodes within 3 hops of $v$ (its 3-hop receptive field).

> [!question]- Why is GIN's aggregation a sum and not a mean?
> Sum (followed by an MLP) is injective on multisets, so different neighbourhoods map to different vectors; mean and max can collapse different multisets (e.g. $\{1\}$ and $\{1,1\}$). That makes GIN as expressive as 1-WL.

> [!question]- A 20-layer GCN gives almost the same embedding for every node. What happened, and what can you do?
> Over-smoothing: repeated normalised averaging converges to the dominant eigenvector. Use fewer layers, residual or jumping-knowledge connections, or normalisation techniques.

## Practice

[Graph Neural Networks - Exercises](Graph%20Neural%20Networks%20-%20Exercises.ipynb): the normalised adjacency and one GCN layer by hand, receptive fields and parameter counts, GAT attention, over-smoothing as power iteration, SGC, a 2-layer GCN with hand-written backprop, GraphSAGE with neighbour sampling, a GAT layer and sum vs mean readout.

## Learn more
- [Hamilton – Graph Representation Learning (free)](https://www.cs.mcgill.ca/~wlh/grl_book/) ch. 5–7
- [Stanford CS224W](https://web.stanford.edu/class/cs224w/)
- [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/)
- [GCN](https://arxiv.org/abs/1609.02907)
- [GAT](https://arxiv.org/abs/1710.10903)
- [Distill – A Gentle Introduction to Graph Neural Networks](https://distill.pub/2021/gnn-intro/) and [Understanding Convolutions on Graphs](https://distill.pub/2021/understanding-gnns/) — interactive visual explanations
- [GIN: How Powerful are Graph Neural Networks?](https://arxiv.org/abs/1810.00826)
