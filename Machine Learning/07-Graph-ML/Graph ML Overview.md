---
tags: [ml, graph]
---
# Graph ML Overview

> [!summary] In one sentence
> Graph machine learning makes predictions about things that are defined by their **connections** (people in a social network, atoms in a molecule, papers citing papers), using either hand-made graph features, graph kernels, learned node embeddings, or graph neural networks.

## Intuition first

Most ML assumes each data point is an independent row in a table. But a lot of data is relational: whether a user will like a product depends on what their friends like; whether a molecule is toxic depends on how its atoms are bonded; whether a paper is about ML depends on what it cites. Throwing the connections away throws away the most useful information.

A graph $G=(V,E)$ is just a set of nodes $V$ and edges $E$ between them. Two difficulties make graphs special compared with images or text:

1. **No fixed size or order.** An image is a grid with a natural "top-left"; a graph has no first node. If you renumber the nodes, it is still the same graph, so any method must give the same answer regardless of the numbering (**permutation invariance**, or for node-level outputs **permutation equivariance**: renumber the input, and the outputs are renumbered the same way).
2. **Irregular neighbourhoods.** One node has 2 neighbours, another 2,000. There is no fixed-size "window" like a convolution kernel.

Everyday analogy: you can guess a lot about a person from their friends ("show me your friends and I will tell you who you are"). Graph ML turns that proverb into algorithms: features of a node are refined using features of its neighbours, its neighbours' neighbours, and so on.

## The math, step by step

### Matrices that describe a graph

For $n$ nodes:

- **Adjacency** $A\in\{0,1\}^{n\times n}$: $A_{ij}=1$ if there is an edge between $i$ and $j$. Undirected graph → $A$ symmetric.
- **Degree** $D=\mathrm{diag}(d_1,\dots,d_n)$ with $d_i=\sum_jA_{ij}$, the number of neighbours.
- **Laplacian** $L=D-A$.

Why the Laplacian? Because of its quadratic form:
$$x^\top Lx=\sum_{\{i,j\}\in E}(x_i-x_j)^2.$$
Read $x$ as a value (a "signal") on each node. Then $x^\top Lx$ measures how much the signal *changes across edges*: small if neighbours have similar values, large if they disagree. Consequences:

- $L$ is positive semi-definite (a sum of squares is $\ge0$).
- The constant vector $\mathbf 1$ gives $x^\top Lx=0$: eigenvalue 0. The number of zero eigenvalues equals the number of **connected components**.
- The eigenvector of the second-smallest eigenvalue (the **Fiedler vector**) is the smoothest non-constant signal; splitting nodes by its sign gives a good two-way cut. This is the core of **spectral clustering**.

### Walks and powers of $A$

$(A^k)_{ij}$ counts the walks of length $k$ from $i$ to $j$. So $A^2$ tells you about friends-of-friends, and $\mathrm{trace}(A^3)/6$ counts triangles (each triangle is a closed 3-walk, counted from 3 start nodes in 2 directions).

### Random walks and PageRank

A random walker who moves to a uniformly random neighbour each step has transition matrix $D^{-1}A$. On a connected (non-bipartite) undirected graph it ends up at node $i$ with probability $d_i/2|E|$: random walks prefer high-degree nodes.

PageRank adds a "teleport": with probability $\alpha$ (typically 0.85) follow a random out-link, otherwise jump to a uniformly random node:
$$p_i=\frac{1-\alpha}{N}+\alpha\sum_{j\to i}\frac{p_j}{d^{\text{out}}_j}.$$
In words: a page is important if important pages link to it, and each page splits its importance evenly across its out-links. You solve it by **power iteration**: start uniform and apply the formula until nothing changes.

![PageRank by power iteration: node sizes settle to their importance](../../Attachments/ML%20Animations/Graph%20ML%20Overview%20-%20PageRank%20power%20iteration.gif)

*Watch the node sizes: everyone starts equal at 1/6, and after a few iterations score concentrates on nodes fed by other important nodes, not simply on those with the most in-links.*

## Tasks

- **Node** classification — predict a label per node (fraud account? topic of a paper?) → [[Graph Neural Networks]]
- **Link prediction** — will these two nodes connect? (friend suggestions, drug–target interactions) → [[Link Prediction]]
- **Graph** classification / regression (molecules) — one prediction per whole graph (is this molecule toxic? its solubility?).
- Community detection ([[Clustering]], spectral) — find groups of nodes that are densely connected inside and sparsely between.

Two settings recur:
- **Transductive:** one fixed graph, some nodes labelled, predict the others; all nodes are seen during training.
- **Inductive:** the model must work on nodes or whole graphs never seen in training (new users, new molecules). Shallow embeddings are transductive; GNNs can be inductive.

## Approaches

1. **Hand-crafted features**: degree, centrality, PageRank, common neighbours. Compute numbers per node or pair and feed them to any classifier. Examples:
   - *degree centrality* $d_i$: how many direct connections;
   - *closeness centrality*: inverse of the average shortest-path distance to all other nodes (BFS on unweighted graphs);
   - *betweenness*: how often a node lies on shortest paths between others (a bridge);
   - *clustering coefficient*: the fraction of pairs of a node's neighbours that are themselves connected, $C_i=\frac{\#\text{triangles at }i}{\binom{d_i}{2}}$.
   Interpretable and cheap, but you must guess the right features.
2. **Graph kernels**: Weisfeiler–Lehman, random walk ([[Kernel Methods]]). Define a similarity between whole graphs and use an SVM. **Weisfeiler–Lehman (WL)** colour refinement: give every node the same colour, then repeatedly recolour each node by hashing (its colour, the sorted multiset of its neighbours' colours). After $k$ rounds, a node's colour summarises its $k$-hop neighbourhood; comparing colour histograms compares graphs. Random-walk kernels count matching walks in two graphs.
3. **Shallow embeddings**: DeepWalk, node2vec, matrix factorization. Learn a vector $z_v$ per node such that nodes that co-occur on short random walks get similar vectors (the skip-gram trick from word2vec, with walks as "sentences"). DeepWalk uses uniform walks; node2vec biases the walks between BFS-like (local) and DFS-like (exploratory) behaviour. Both can be seen as implicitly factorising a matrix of walk co-occurrence statistics. Limitation: one free vector per node → transductive, and no use of node features.
4. **GNNs**: message passing. Each layer, every node aggregates its neighbours' feature vectors and updates its own; stacking $k$ layers gives each node information from its $k$-hop neighbourhood. They use node features, share weights across nodes and are inductive. Their expressive power is bounded by the 1-WL test (see [[Graph Neural Networks]]).

The lines are blurry: degree and PageRank can be input features to a GNN, and WL is the theoretical model of message passing.

## Worked example

Graph: a triangle $0\!-\!1\!-\!2$ plus a tail $2\!-\!3$.

$$A=\begin{pmatrix}0&1&1&0\\1&0&1&0\\1&1&0&1\\0&0&1&0\end{pmatrix},\quad D=\mathrm{diag}(2,2,3,1),\quad L=\begin{pmatrix}2&-1&-1&0\\-1&2&-1&0\\-1&-1&3&-1\\0&0&-1&1\end{pmatrix}.$$

- Every row of $L$ sums to 0, so $L\mathbf 1=0$: eigenvalue 0, one connected component.
- Signal $x=(1,1,0,0)$ ("nodes 0 and 1 vs 2 and 3"): only edges $0\!-\!2$ and $1\!-\!2$ connect different values, so $x^\top Lx=1+1=2$, the number of edges the split cuts.
- Walks: $(A^2)_{03}=1$ (only $0\to2\to3$); diagonal of $A^2$ = degrees; $\mathrm{trace}(A^3)=6$ → $6/6=1$ triangle.
- Clustering coefficient of node 2: neighbours $\{0,1,3\}$ form $\binom32=3$ pairs, of which one (0–1) is an edge, so $C_2=1/3$. For node 0: neighbours $\{1,2\}$ are connected → $C_0=1$.
- Random-walk stationary distribution: $d_i/2|E|=(2,2,3,1)/8$, so a long random walk spends 37.5 % of its time at node 2.

## Common confusions

- **"Node order is just a detail."** → Any model that depends on the numbering (e.g. flattening $A$ into an MLP input) learns spurious patterns. Graph methods must be permutation invariant/equivariant.
- **"High degree = important."** → Degree counts links; PageRank weighs *who* links to you. A node with few links from very central nodes can outrank one with many links from peripheral nodes.
- **"The Laplacian is just another adjacency matrix."** → $L$ measures smoothness of signals over the graph ($x^\top Lx$); its eigenvectors are the graph's "frequencies", with low eigenvalues = smooth, community-like patterns.
- **"Node embeddings like DeepWalk work for new nodes."** → They learn one vector per training node (a lookup table), so a new node has no embedding without retraining; GNNs compute embeddings from features and neighbourhoods and generalise inductively.

## Check yourself

> [!question]- What does $x^\top Lx$ equal, and what is it for $x=\mathbf 1$?
> $\sum_{\{i,j\}\in E}(x_i-x_j)^2$, the total squared disagreement across edges. For the constant vector it is 0, so $\mathbf 1$ is an eigenvector with eigenvalue 0.

> [!question]- A graph's Laplacian has eigenvalue 0 with multiplicity 3. What does that tell you?
> The graph has 3 connected components.

> [!question]- Predicting whether a molecule binds to a protein, predicting a user's age in a social network, recommending new friends: which graph task is each?
> Graph classification/regression, node classification, link prediction.

> [!question]- Why does PageRank need the teleport term $(1-\alpha)/N$?
> Without it, a walker can get stuck in dead ends or closed loops and the scores need not be unique; teleporting makes the chain irreducible so a unique stationary distribution exists, and it models a surfer who occasionally jumps to a random page.

> [!question]- How many triangles does a graph have if $\mathrm{trace}(A^3)=24$?
> $24/6=4$.

## Practice

[Graph ML Overview - Exercises](Graph%20ML%20Overview%20-%20Exercises.ipynb): adjacency, degree and Laplacian, the Laplacian quadratic form, walk and triangle counting, PageRank by hand and by power iteration, centrality and clustering coefficients, spectral community detection, Weisfeiler–Lehman refinement and DeepWalk as matrix factorisation.

Your lecture notes: [[8-semester/ML/Lecture Notes 1-12|Lectures 8–12]].

## Learn more
- [Stanford CS224W](https://web.stanford.edu/class/cs224w/)
- [Hamilton – Graph Representation Learning (free)](https://www.cs.mcgill.ca/~wlh/grl_book/)
- [Distill – A Gentle Introduction to Graph Neural Networks](https://distill.pub/2021/gnn-intro/) — interactive tour of graph data and tasks
- [DeepWalk](https://arxiv.org/abs/1403.6652) and [node2vec](https://arxiv.org/abs/1607.00653) papers
