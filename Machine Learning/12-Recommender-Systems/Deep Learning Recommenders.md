---
tags: [ml, recsys, deep-learning]
---
# Deep Learning Recommenders

> [!summary] In one sentence
> Deep recommenders replace hand-built similarity and plain matrix factorization with neural networks that turn users, items, context and histories into embeddings and learn how they interact, at a scale where embedding tables, sampling tricks and fast nearest-neighbour search matter as much as the architecture.

## Intuition first

Matrix factorization gives every user and item one vector and scores with a dot product. That is already a tiny neural network: two embedding lookups and a dot product. Deep learning recommenders grow this idea in a few directions:

- **More inputs.** Not just IDs, but context (time, device), item metadata, text, and the user's recent history.
- **More flexible interaction.** An MLP or explicit cross layers can learn "this user likes action films, but only on weekends".
- **Order matters.** Your *next* video depends on the last few you watched. Sequence models (RNNs, transformers) read the history like a sentence and predict the next "word" (item).
- **Graphs.** Users and items form a bipartite graph; message passing spreads information from neighbours of neighbours.

The engineering reality shapes everything: there are billions of IDs, so **embedding tables** dominate memory, and you cannot score every item per request, so retrieval models must keep the item side precomputable. That is why the humble dot product survives in the most important retrieval model, the **two-tower** network.

| Model | Idea | Paper |
|---|---|---|
| **NCF / NeuMF** | MLP replaces dot product of embeddings | [He et al. 2017](https://arxiv.org/abs/1708.05031) |
| **Wide & Deep** | linear (memorisation) + deep (generalisation) | [Cheng et al. 2016](https://arxiv.org/abs/1606.07792) |
| DeepFM / DCN | factorization machines / explicit cross features + DNN | |
| **DLRM** | Meta's embedding + MLP + dot-product interactions | [Naumov et al. 2019](https://arxiv.org/abs/1906.00091) |
| **Two-tower** (dual encoder) | user and item encoders, dot product; ANN retrieval | YouTube DNN (Covington et al. 2016) |
| AutoRec / VAE-CF | autoencoders on the interaction matrix | |
| **SASRec** | self-attention over the user's item sequence | [Kang & McAuley 2018](https://arxiv.org/abs/1808.09781) |
| **BERT4Rec** | bidirectional masked item modeling | [Sun et al. 2019](https://arxiv.org/abs/1904.06690) |
| GRU4Rec | RNN session-based | |
| **LightGCN** | simplified GCN on user–item graph | [He et al. 2020](https://arxiv.org/abs/2002.02126) |
| LLM-based / generative retrieval | items as tokens, LLM reranking | |

## The main ideas, one by one

**NCF / NeuMF.** Instead of $s(u,i)=p_u^\top q_i$, use $s(u,i)=f([p_u;q_i])$ with an MLP $f$ (NeuMF also keeps a dot-product branch). In theory more expressive; in practice an MLP finds it surprisingly hard to learn a dot product, and the scores can no longer be served by inner-product search.

**Wide & Deep.** Two parts trained jointly:
- the **wide** part is a linear model on sparse and *crossed* features (e.g. `installed=Netflix AND shown=Disney+`). It **memorises** specific co-occurrences seen in the data;
- the **deep** part is an MLP on dense embeddings. It **generalises** to combinations never seen before, because similar items have similar embeddings.

Wide alone cannot handle unseen pairs; deep alone over-generalises and recommends loosely related items. Together: precise for frequent patterns, sensible for rare ones.

**DeepFM / DCN.** Replace hand-crafted crosses: DeepFM adds a factorization-machine layer ($\sum_{i<j}\langle v_i,v_j\rangle x_ix_j$, computable in $O(kn)$, see [[Collaborative Filtering and Matrix Factorization]]); DCN learns explicit feature crosses layer by layer.

**DLRM.** Sparse features → embedding tables; dense features → a bottom MLP; all pairwise dot products between these vectors form the interaction layer; a top MLP outputs the click probability. Built for huge industrial tables.

**AutoRec / VAE-CF / EASE.** Treat each user's row of the interaction matrix $X$ as input and reconstruct it; high reconstructed values on unseen items are recommendations. The linear extreme is **EASE** (Steck 2019): learn an item–item matrix $B$ with zero diagonal, $\min_B\lVert X-XB\rVert_F^2+\lambda\lVert B\rVert_F^2$ s.t. $\mathrm{diag}(B)=0$, solved in closed form by $P=(X^\top X+\lambda I)^{-1}$, $B_{ij}=-P_{ij}/P_{jj}$. A few lines of NumPy, and a famously strong baseline.

## Two-tower retrieval

![Two towers produce user and item embeddings that meet in a dot product; a batch score matrix whose diagonal grows during training](../../Attachments/ML%20Animations/Deep%20Learning%20Recommenders%20-%20two-tower%20in-batch%20softmax.gif)

*Watch the two towers meet only at the dot product, then watch training brighten the diagonal (true pairs) of the batch score matrix while the softmax bar of the positive grows.*

A **user tower** maps user features to $e_u\in\mathbb R^d$; an **item tower** maps item features to $e_i\in\mathbb R^d$; the score is $s(u,i)=e_u^\top e_i$ (often on normalised vectors, so it is a cosine). The towers never see each other's inputs. That restriction is the whole point: item embeddings can be computed once, put in an approximate nearest-neighbour (ANN) index, and at request time the system computes one $e_u$ and asks the index for its top few hundred items in milliseconds. What the model *cannot* capture is any interaction between a user feature and an item feature beyond the final dot product (e.g. "this user likes this brand only at this price"); those crosses are left to the ranking stage, which only sees a few hundred candidates.

### Two-tower training
In-batch softmax with sampled negatives:
$$L=-\log\frac{e^{s(u,i^+)/\tau}}{\sum_{j\in\text{batch}}e^{s(u,j)/\tau}}$$
Correct for popularity of in-batch negatives (logQ correction). Serve with FAISS/ScaNN/HNSW.

Step by step:
- A batch contains $B$ (user, positive item) pairs. Compute all $B\times B$ scores $S=UV^\top/\tau$. Row $b$ is user $b$'s scores against every item in the batch.
- The diagonal entry is the true pair; the other $B-1$ items in the row act as **negatives for free**: they are positives of other users, so no extra sampling or encoding is needed.
- The loss is a cross-entropy with the diagonal as the correct class. Its gradient has a clean form: with $P$ the row-wise softmax of $S$, $\partial L/\partial U=\frac{1}{\tau B}(P-I)V$ and $\partial L/\partial V=\frac{1}{\tau B}(P-I)^\top U$ (for the batch-averaged loss).
- **Temperature** $\tau$: a smaller $\tau$ sharpens the softmax, so the loss focuses on the hardest negatives (those scoring close to the positive).
- **logQ correction.** Items appear in batches proportionally to their popularity, so popular items are used as negatives far too often and the model learns to under-score them. Replace each logit $s_j$ by $s_j-\log q_j$, where $q_j$ is the probability that item $j$ appears in a batch. This removes the sampling bias so the learned scores approximate a full softmax.
- **Serving.** The score is an inner product, so retrieval is *maximum inner product search* (MIPS). Exact search is one matrix product plus a top-K; libraries like FAISS, ScaNN and HNSW give approximate answers orders of magnitude faster on millions of items. MIPS is not the same as cosine/L2 nearest neighbours unless vectors are normalised; indexes either support MIPS directly or add one extra dimension to reduce it to L2 search.

## Sequential recommenders

![Causal attention lets each position see only earlier items; bidirectional attention lets every position see all, with a masked item to predict](../../Attachments/ML%20Animations/Deep%20Learning%20Recommenders%20-%20causal%20vs%20bidirectional%20attention.gif)

*Watch the lower-triangular mask fill in row by row for SASRec, then flip to a full mask when BERT4Rec hides item 3 and predicts it from both sides.*

- **GRU4Rec** reads the session with a recurrent network and predicts the next item at each step ([[RNN and LSTM]]).
- **SASRec** uses a transformer decoder ([[Transformers]]): the output at position $t$ may only attend to items $1..t$ (a causal mask $M_{ts}=-\infty$ for $s>t$), and is trained to predict item $t+1$. Attention for one head: $\mathrm{softmax}\big(\frac{QK^\top}{\sqrt d}+M\big)V$.
- **BERT4Rec** uses bidirectional attention, so position $t$ sees the whole sequence. Predicting the next item would then be trivial (it is in the input), so instead random items are replaced by `[MASK]` and the model predicts them from both sides (a cloze task).

If SASRec were trained with bidirectional attention, position $t$ could look at item $t+1$, the very target it must predict, and training would be leakage, not learning.

## Graph models: LightGCN

Treat interactions as a bipartite graph ([[Graph Neural Networks]]). LightGCN strips a GCN down to pure neighbourhood averaging: no weight matrices, no non-linearities.
$$e_u^{(k+1)}=\sum_{i\in N(u)}\frac{1}{\sqrt{|N(u)|}\sqrt{|N(i)|}}\,e_i^{(k)},$$
and symmetrically for items. In matrix form $E^{(k+1)}=\tilde AE^{(k)}$ with $\tilde A=D^{-1/2}AD^{-1/2}$ and $A=\begin{pmatrix}0&X\\X^\top&0\end{pmatrix}$. The final embedding is the **mean** of layers $0..K$. After two layers a user's vector contains information from users who share items with them: collaborative filtering by message passing. The normalisation $\frac{1}{\sqrt{|N(u)|}\sqrt{|N(i)|}}$ stops very popular items and very active users from dominating.

## Worked example

**In-batch softmax.** A user's batch scores are $s=(3.0,\,1.0,\,0.0)$, the first being the positive.
- $\tau=1$: $\frac{e^3}{e^3+e^1+e^0}=\frac{20.09}{23.80}\approx0.844$, so $L=-\ln0.844\approx0.17$.
- $\tau=0.5$: logits become $(6,2,0)$, $\frac{403.4}{403.4+7.39+1}\approx0.980$, $L\approx0.02$.

Lower temperature amplifies score gaps: already-separated pairs contribute almost nothing, so learning concentrates on hard negatives.

**One LightGCN step.** User $u$ interacted with $i_1$ (which only $u$ interacted with, $|N(i_1)|=1$) and $i_2$ (4 users, $|N(i_2)|=4$); $|N(u)|=2$. With 1-d embeddings $e_{i_1}=2$, $e_{i_2}=1$:
$$e_u^{(1)}=\frac{2}{\sqrt2\sqrt1}+\frac{1}{\sqrt2\sqrt4}\approx1.414+0.354=1.77.$$
Per unit of embedding, the niche item $i_1$ gets weight $1/\sqrt2\approx0.71$ and the popular $i_2$ only $1/(2\sqrt2)\approx0.35$: twice as much influence for the niche item.

**Attention pairs.** For $T=6$ items, SASRec's causal mask allows $1+2+\dots+6=21$ (query, key) pairs; BERT4Rec allows all $6^2=36$.

## Practical
- Embedding tables dominate memory; hashing tricks, mixed-dimension embeddings.
- Features: user history, context (time, device), item metadata.
- Strong baselines matter: well-tuned MF/iALS often matches fancy models (Rendle et al., "Neural Collaborative Filtering vs. Matrix Factorization Revisited", 2020).

Why each point matters:
- **Memory.** $5\times10^7$ items × 128 dimensions × 4 bytes (float32) $=25.6$ GB for one table. 8-bit quantisation cuts it by 4×.
- **Hashing trick.** Map $n$ IDs into $m$ buckets with a hash. Memory is fixed, new IDs need no table resize, but colliding IDs share one vector. A given ID shares its bucket with at least one other with probability $1-(1-1/m)^{n-1}\approx1-e^{-n/m}$; with $n=m$ that is about 63%, which is why multiple hash functions or larger tables are used.
- **Mixed-dimension embeddings.** Popular items get large vectors, rare ones small vectors, since rare IDs have too little data to fill many dimensions anyway.
- **Baselines.** Rendle et al. (2020) showed a dot product is hard for an MLP to learn, and a properly tuned MF matches NCF. Always report MF/iALS, EASE and popularity next to a deep model.

## Common confusions

- **"An MLP scorer is strictly better than a dot product."** → It is more expressive in theory, but harder to train for this purpose and it destroys fast inner-product retrieval. Retrieval models keep the dot product on purpose.
- **"In-batch negatives are random negatives."** → They are sampled proportionally to popularity, which biases the model against popular items unless you apply the logQ correction.
- **"BERT4Rec is SASRec with more attention."** → It changes the training task: masked-item prediction instead of next-item prediction, because bidirectional attention would leak the target.
- **"Two-tower models can model any feature interaction."** → User and item features only meet in the final dot product; cross features are the ranker's job.
- **"Deeper GCNs are better."** → LightGCN typically uses 2–3 layers; more layers over-smooth all embeddings toward the same vector.

## Check yourself

> [!question]- Why do production retrieval models keep the dot product instead of an MLP scorer?
> Item embeddings can then be precomputed and indexed for (approximate) maximum inner product search, so the top items among millions are found in milliseconds. An MLP would need a forward pass for every item.

> [!question]- In a batch of 256 pairs, how many negatives does each user get with in-batch softmax?
> 255: the positives of the other users in the batch.

> [!question]- What does the logQ correction compensate for?
> The fact that in-batch negatives are sampled proportionally to popularity, so popular items are over-represented as negatives. Subtracting $\log q_j$ from each logit removes that sampling bias.

> [!question]- What is "memorisation" vs "generalisation" in Wide & Deep?
> Memorisation: the wide linear part learns weights for specific crossed features seen in the data (exact co-occurrences). Generalisation: the deep part uses embeddings to score unseen combinations by similarity.

> [!question]- What would go wrong if SASRec used bidirectional attention?
> Position $t$ could attend to item $t+1$, which is its own training target, so the model would learn to copy instead of predict.

## Practice

[Deep Learning Recommenders - Exercises](Deep%20Learning%20Recommenders%20-%20Exercises.ipynb): memorisation vs generalisation, MLP vs dot product, two-tower limits, sequential models; embedding sizing, hashing collisions, in-batch softmax and logQ by hand, a LightGCN layer, attention pairs; then in-batch softmax with gradients, a two-tower model, exact retrieval vs a NN index, the FM interaction layer, LightGCN, causal self-attention and EASE in code.

## Learn more

Related: [[Transformers]], [[Graph Neural Networks]], [[Optimizers]].
- Papers linked in the table above, plus Rendle et al., [Neural Collaborative Filtering vs. Matrix Factorization Revisited](https://arxiv.org/abs/2005.09683) (2020).
- Steck, [Embarrassingly Shallow Autoencoders for Sparse Data (EASE)](https://arxiv.org/abs/1905.03375) (2019).
- [TensorFlow Recommenders: basic retrieval tutorial](https://www.tensorflow.org/recommenders/examples/basic_retrieval) (a two-tower model end to end).
- [[Recommender Systems Overview]] · [[Recommender Systems Resources]]
