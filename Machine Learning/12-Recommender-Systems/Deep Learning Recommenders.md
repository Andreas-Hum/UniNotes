---
tags: [ml, recsys, deep-learning]
---
# Deep Learning Recommenders

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

## Two-tower training
In-batch softmax with sampled negatives:
$$L=-\log\frac{e^{s(u,i^+)/\tau}}{\sum_{j\in\text{batch}}e^{s(u,j)/\tau}}$$
Correct for popularity of in-batch negatives (logQ correction). Serve with FAISS/ScaNN/HNSW.

## Practical
- Embedding tables dominate memory; hashing tricks, mixed-dimension embeddings.
- Features: user history, context (time, device), item metadata.
- Strong baselines matter: well-tuned MF/iALS often matches fancy models (Rendle et al., "Neural Collaborative Filtering vs. Matrix Factorization Revisited", 2020).

Related: [[Transformers]], [[Graph Neural Networks]], [[Optimizers]].
