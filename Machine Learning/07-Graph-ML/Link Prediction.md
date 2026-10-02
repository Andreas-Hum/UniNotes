---
tags: [ml, graph]
---
# Link Prediction

> [!summary] In one sentence
> Link prediction scores pairs of nodes that are not (yet) connected and ranks them by how likely an edge is, using simple neighbourhood heuristics, path counts, learned node embeddings or GNNs, and is evaluated by hiding real edges and checking whether they come out on top.

## Intuition first

Predict missing or future edges. "People you may know", "customers who bought this also bought", "this protein probably interacts with that drug", "this paper should cite that one": all are link prediction. You see a graph today and want to guess which edges are missing (incomplete data) or will appear (the graph grows).

Why is this possible at all? Because real networks are not random:

- **Triadic closure:** if two people have many friends in common, they are likely to meet and become friends ("a friend of a friend is a friend").
- **Homophily:** similar nodes connect (same interests, same field, similar chemistry).
- **Rich get richer:** popular nodes attract even more links (new web pages link to Google, not to your blog).

Each heuristic below is one of these ideas turned into a formula. Learned methods (embeddings, GNNs) learn which patterns matter from the data instead.

![Scoring two candidate pairs by their common neighbours](../../Attachments/ML%20Animations/Link%20Prediction%20-%20common%20neighbours.gif)

*Watch the highlighted neighbourhoods: $u$ and $v$ share three neighbours, so the pair scores high and becomes a predicted link, while $u$ and $w$ share none and score zero.*

## The math, step by step

Notation: $N(u)$ is the set of neighbours of $u$, $d_u=|N(u)|$ its degree, $A$ the adjacency matrix, $m$ the number of edges.

### Heuristics

| Score | Formula |
|---|---|
| Common neighbours | $\lvert N(u)\cap N(v)\rvert$ |
| Jaccard | $\frac{\lvert N(u)\cap N(v)\rvert}{\lvert N(u)\cup N(v)\rvert}$ |
| Adamic–Adar | $\sum_{w}\frac1{\log d_w}$ |
| Preferential attachment | $d_ud_v$ |
| Katz / SimRank / PageRank | path-based, global |

What each one means:

- **Common neighbours (CN):** the count of shared friends. Pure triadic closure. Equals $(A^2)_{uv}$, the number of length-2 paths.
- **Jaccard:** CN divided by the total number of distinct neighbours. Corrects for the fact that two hubs share many neighbours just because they have so many: "what fraction of their friends are shared?"
- **Adamic–Adar (AA):** the sum runs over the common neighbours $w\in N(u)\cap N(v)$. Each shared neighbour counts $1/\log d_w$, so a shared neighbour with few connections counts more than a shared celebrity. Sharing a niche hobby club says more than both following the same pop star.
- **Preferential attachment (PA):** $d_ud_v$, rich-get-richer. It does not even look at shared neighbours. Why the product? In a random graph that keeps only the degrees (the configuration model, $2m$ edge "stubs" paired at random), the expected number of edges between $u$ and $v$ is about $d_ud_v/2m$.
- **Katz:** counts *all* paths between $u$ and $v$, discounting long ones:
  $$S_{uv}=\sum_{\ell\ge1}\beta^\ell(A^\ell)_{uv},\qquad S=(I-\beta A)^{-1}-I,$$
  which converges when $\beta<1/\lambda_{\max}(A)$. It sees beyond 2 hops, so it can score pairs with no common neighbours.
- **SimRank:** "two nodes are similar if their neighbours are similar" (recursive). **Personalised PageRank:** the probability that a random walk restarting at $u$ is at $v$.

Local heuristics (CN, Jaccard, AA, PA) are cheap and surprisingly strong baselines; global ones (Katz, SimRank, PageRank) capture longer-range structure at higher cost.

## Learned

- **Shallow embeddings**: score $z_u^\top z_v$ (DeepWalk, node2vec, matrix factorization). Each node gets a free vector $z_u\in\mathbb R^k$, trained so that connected (or walk-co-occurring) pairs have a large dot product. Typically $p(u\sim v)=\sigma(z_u^\top z_v)$ with binary cross-entropy on positive edges and sampled negative pairs. For a positive pair the loss is $-\log\sigma(z_u^\top z_v)$, whose gradient w.r.t. $z_u$ is $-(1-\sigma(z_u^\top z_v))\,z_v$: gradient descent pulls $z_u$ towards $z_v$, and harder when the model is still unsure. Matrix factorisation is the same idea written as $A\approx ZZ^\top$.
- **GNN encoders** + decoder, SEAL (subgraph-based) → [[Graph Neural Networks]]. A GNN computes $z_u$ from node features and the neighbourhood (works for new nodes), then a decoder scores the pair (dot product, MLP on $[z_u\,\|\,z_v]$, …). **SEAL** instead extracts the small subgraph around $u$ and $v$, labels nodes by their distance to the pair, and classifies the subgraph with a GNN; it can learn heuristics like CN or AA automatically.
- **Combining heuristics:** compute several heuristic scores per pair and train a logistic regression or gradient-boosted model on them; a strong, cheap baseline.

## Evaluation

Hide a fraction of edges; sample negative non-edges; report ROC-AUC, AP, Hits@k ([[Model Evaluation and Metrics]]). Avoid leakage: remove test edges from the message-passing graph.

Step by step:

1. **Split edges:** randomly hide e.g. 10 % of edges as test positives (and some as validation).
2. **Sample negatives:** pairs that are not edges in the *full* graph (never accidentally a hidden positive).
3. **Score using only the training graph.** Every heuristic, embedding and GNN must be computed on the graph *without* the test edges.
4. **Rank and measure:**
   - **ROC-AUC** = probability that a random positive scores higher than a random negative.
   - **AP** (average precision): averages the precision at the rank of each positive; sensitive to the top of the ranking.
   - **Hits@k**: fraction of positives ranked above the $k$-th highest-scoring negative (the OGB convention), or in the top $k$ of a candidate list. Matches the use case "show $k$ suggestions".

**Why leakage is so dangerous here.** If a test edge $(u,v)$ stays in the graph, then $A_{uv}=1$ is directly visible: Katz's $\ell=1$ term, a GNN's message passing and the degrees all "see the answer", and scores look excellent but are meaningless.

**Why negatives matter.** Real graphs are sparse, so random non-edges are usually trivially far apart, and AUC on random negatives can look great even for weak models. Harder negatives (e.g. pairs 2 hops apart) or ranking metrics such as Hits@k give a more honest picture.

## Worked example

Use the graph from the animation: $N(u)=\{a,b,c,d\}$, $N(v)=\{a,b,c,e\}$, and degrees $d_a=3$, $d_b=d_c=2$, $d_u=d_v=4$.

- CN $=|\{a,b,c\}|=3$.
- Jaccard $=3/|\{a,b,c,d,e\}|=3/5=0.6$.
- Adamic–Adar $=\frac1{\ln3}+\frac1{\ln2}+\frac1{\ln2}=0.91+1.44+1.44=3.80$.
- PA $=4\cdot4=16$.
- For $(u,w)$ with $N(w)=\{e,g\}$: CN $=0$, Jaccard $=0$, AA $=0$, but PA $=4\cdot2=8$. PA still gives a non-zero score because it ignores shared neighbours.

**Metrics.** Scores for 2 hidden positives: $\{0.9,0.6\}$; for 3 negatives: $\{0.7,0.2,0.1\}$.
- AUC: of the $2\times3=6$ positive–negative pairs, the positive wins in 5 (0.9 beats all three; 0.6 beats 0.2 and 0.1) → $5/6\approx0.83$.
- Ranking: 0.9 (+), 0.7 (−), 0.6 (+), 0.2, 0.1. Precision at the positives' ranks: $1/1$ and $2/3$ → AP $=(1+0.667)/2\approx0.83$.
- Hits@1: the highest negative is 0.7; one of two positives beats it → 0.5.

## Common confusions

- **"Common neighbours and preferential attachment measure the same thing."** → CN measures shared neighbourhood (local closure); PA only multiplies degrees, so two unrelated hubs get a huge PA score.
- **"High ROC-AUC means the model is useful."** → With easy random negatives in a sparse graph almost anything gets high AUC. Check Hits@k / AP and harder negatives.
- **"I removed the test edges from the labels, so there is no leakage."** → They must also be removed from the *input graph* used for features, embeddings and message passing.
- **"Shallow embeddings can score any pair."** → Only pairs of nodes seen in training; new nodes have no vector. GNN encoders handle new nodes if they have features.
- **"Katz with any $\beta$ works."** → The series only converges for $\beta<1/\lambda_{\max}(A)$.

## Check yourself

> [!question]- Why does Adamic–Adar divide by $\log d_w$?
> A common neighbour with few connections is stronger evidence than a hub that is connected to everyone; the $1/\log d_w$ weight down-weights hubs.

> [!question]- What is $(A^2)_{uv}$, and which heuristic is it?
> The number of length-2 walks from $u$ to $v$, i.e. the number of common neighbours.

> [!question]- You computed node2vec embeddings on the full graph, then evaluated on hidden edges. What went wrong?
> Leakage: the test edges influenced the random walks and hence the embeddings. Embeddings must be trained on the graph with test edges removed.

> [!question]- What does ROC-AUC = 0.5 mean for a link predictor?
> Its scores rank positives above negatives no better than chance.

## Practice

[Link Prediction - Exercises](Link%20Prediction%20-%20Exercises.ipynb): the four heuristic scores by hand and vectorised, the Katz index, ROC-AUC / AP / Hits@k from scratch, a leak-free edge split, matrix-factorisation embeddings, learning to combine heuristics, and measuring how much leakage inflates scores.

## Learn more
- [Stanford CS224W](https://web.stanford.edu/class/cs224w/)
- [Hamilton – Graph Representation Learning (free)](https://www.cs.mcgill.ca/~wlh/grl_book/) ch. 3
- [SEAL](https://arxiv.org/abs/1802.09691)
- [OGB link prediction benchmarks](https://ogb.stanford.edu/)
- [node2vec](https://arxiv.org/abs/1607.00653) — biased random walks for node embeddings
