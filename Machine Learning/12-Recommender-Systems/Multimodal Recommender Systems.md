---
tags: [ml, recsys, multimodal]
status: not-started
notebook: not-started
level:
reviewed:
---
# Multimodal Recommender Systems

> [!summary] In one sentence
> Multimodal recommenders add what an item *looks, reads and sounds like* (image, text, audio, video features from pretrained encoders) to the usual user–item interactions, so they can recommend items with little or no history and capture taste that IDs alone cannot see.

Use **item content in several modalities** (images, text, audio, video) together with user–item interactions. Typical domains: e-commerce/fashion (product photo + title + description), micro-video (TikTok-style: visual + acoustic + text), news, music.

> [!info] Why bother?
> Pure [[Collaborative Filtering and Matrix Factorization|CF]] only knows IDs. Content features help with **cold-start items**, **sparse data**, and **visually-driven taste** (fashion, art, food).

## Intuition first

To a pure CF model, a new dress is item `#48213`: a random vector that has never been clicked, so it can never be recommended. A human shop assistant would just *look* at it: "red, linen, summery: like the three dresses you bought last month." Multimodal recommenders give the model those eyes (and ears, and reading skills).

The three reasons in the box above, mechanically:
- **Cold-start items**: a new item's image/text embedding is available on day one, so it can be placed near similar items that already have interactions.
- **Sparse data**: an item with five clicks has a poorly estimated ID embedding; content features act as a strong prior that shares strength between look-alike items.
- **Visually-driven taste**: in fashion, art or food, "what it looks like" is the preference. Two dresses can have no shared buyers yet look almost identical.

Where to expect **little** gain: domains where content says little about taste (e.g. phone chargers, where a photo of one cable looks like any other) or where interaction data is already dense.

Modern encoders (CLIP for images, Sentence-BERT for text) are trained on huge generic datasets and are usually **frozen**: features are extracted once and stored. The recommender then only has to learn *how much each user cares about each modality* and how to combine content with collaborative signals.

## The general pipeline
1. **Modality encoders** (usually frozen, pre-extracted): CNN/ViT or **CLIP** for images ([[Computer Vision Overview]]), BERT/Sentence-BERT for text ([[Text Representations]]), VGGish for audio.
2. **Feature interaction / fusion**: how modalities and IDs combine.
3. **Feature enhancement**: self-supervised / contrastive objectives to align modalities ([[Self-Supervised and Contrastive Learning]]).
4. **Optimisation**: usually BPR loss on implicit feedback ([[Collaborative Filtering and Matrix Factorization]]).

This four-part split follows the taxonomy of the [Liu et al. survey](https://arxiv.org/abs/2302.03883).

**Why freeze the encoders?** (1) Cost: fine-tuning a ViT for every training step over millions of interactions is enormous; pre-extracted features are just a lookup. (2) Data: interaction labels are sparse and noisy, so fine-tuning a large encoder on them overfits. (3) Simplicity: features can be shared across models and experiments. **What you lose**: the features are not adapted to the recommendation task (CLIP knows "dress", not "dresses this user buys"). **Middle ground**: keep the encoder frozen but learn a small projection on top (VBPR's $E$, an MLP adapter), or fine-tune only the last layers / LoRA.

## Fusion strategies

![A product with image, text and ID passes through frozen encoders; per-user attention weights over modalities change from one user to another](../../Attachments/ML%20Animations/Multimodal%20Recommender%20Systems%20-%20attention%20fusion.gif)

*Same item, same modality scores: watch the attention bars swap when we switch from a user who shops by look to one who reads descriptions, and the fused score drop from 0.72 to 0.36.*

| Strategy | How | Trade-off |
|---|---|---|
| Early fusion | concatenate features before the model | simple; one modality can dominate |
| Late fusion | separate per-modality scores, then combine | flexible; misses cross-modal interactions |
| Attention fusion | learn per-user/per-item modality weights | personalised, more parameters |
| Graph-based | modality-specific or item–item graphs + GCN | current state of the art on benchmarks |

**Early fusion, done properly.** If a 768-d text vector has values around 10 and a 512-d image vector values around 0.1, concatenation is in practice "text only": distances are dominated by the larger block. Standardise each modality (z-score per feature over all items) and divide modality $m$ by $\sqrt{d_m}$, so every block has the same expected squared norm, before concatenating.

**Late fusion.** $\hat s_{ui}=\sum_m w_m\,s^{(m)}_{ui}$ with fixed weights. Easy to debug (each modality has its own score), but the model never learns that "this colour matters only for this category".

**Attention fusion.** Each user has logits $a_u\in\mathbb R^M$ over the $M$ modalities; weights $\alpha_u=\mathrm{softmax}(a_u)$ and
$$\hat s_{ui}=\sum_m\alpha_{u,m}\,s^{(m)}_{ui}.$$
The softmax keeps the weights positive and summing to 1, so they read as "how much this user trusts each modality".

## Key models (roughly chronological)
| Model | Year | Idea |
|---|---|---|
| [**VBPR**](https://arxiv.org/abs/1510.01784) | 2016 | add a pretrained CNN visual feature, projected to "visual factors", into BPR-MF: $\hat x_{ui}=\alpha+\beta_u+\beta_i+\gamma_u^\top\gamma_i+\theta_u^\top(E f_i)$ |
| **MMGCN** (Wei et al., ACM MM 2019) | 2019 | one user–item graph **per modality**, GCN on each, then combine |
| GRCN, DualGNN | 2020–21 | refine/denoise the interaction graph using content |
| [**LATTICE**](https://arxiv.org/abs/2104.09036) | 2021 | **learn item–item graphs** from modality similarity (kNN), fuse, convolve |
| SLMRec | 2022 | self-supervised learning across modalities |
| [**BM3**](https://arxiv.org/abs/2207.05969) | 2023 | bootstrapped self-supervision without negatives; reconstruct graph + align modalities |
| [**FREEDOM**](https://arxiv.org/abs/2211.06924) | 2023 | **freeze** the item–item graph from LATTICE and **denoise** the user–item graph; faster and more accurate |
| MGCN, DRAGON, LGMRec | 2023+ | multi-view / hypergraph / dual-graph variants |
| LLM/VLM-based recommenders | 2023+ | multimodal LLMs as encoders, rerankers or generative recommenders ([[LLMs Overview]]) |

## The math, step by step

### VBPR
$$\hat x_{ui}=\alpha+\beta_u+\beta_i+\gamma_u^\top\gamma_i+\theta_u^\top(E f_i)$$
- $\alpha$ global offset, $\beta_u,\beta_i$ user and item biases;
- $\gamma_u^\top\gamma_i$: the ordinary MF term on ID factors (dimension $K$);
- $f_i\in\mathbb R^F$: the frozen CNN feature of item $i$'s image (e.g. $F=4096$);
- $E\in\mathbb R^{D\times F}$: a **shared** learned projection to $D$ "visual factors" (e.g. $D=64$);
- $\theta_u\in\mathbb R^D$: how much user $u$ likes each visual factor.

Trained with BPR: $-\ln\sigma(\hat x_{ui}-\hat x_{uj})$ for observed $i$, unobserved $j$. For a **cold item**, $\beta_i$ and $\gamma_i$ were never trained (zero), but $\theta_u^\top Ef_i$ still ranks it by how well its *look* matches the user's visual taste. Plain BPR-MF would give all cold items the same score.

**Why project?** Parameters of the visual part: $DF$ (one shared $E$) $+\,|U|D$. If instead each user had a preference over raw features, it would be $|U|F$. With $|U|=10^6$, $F=512$, $D=32$: $16{,}384+3.2\times10^7\approx3.2\times10^7$ versus $5.12\times10^8$, about 16× fewer, and the shared $E$ learns from *all* users' data.

### Item–item graphs (LATTICE, FREEDOM)

![Items in image-feature space connected to their nearest neighbours; a cold item receives a representation from its neighbours](../../Attachments/ML%20Animations/Multimodal%20Recommender%20Systems%20-%20item-item%20kNN%20graph.gif)

*Watch the kNN edges appear, then the grey cold item light up with its neighbours' colour after one propagation step.*

1. Similarity per modality: $S_{ij}=\cos(f_i,f_j)$.
2. Keep each item's top-$k$ neighbours as 1s, symmetrise $A\leftarrow\max(A,A^\top)$, normalise $\tilde A=D^{-1/2}AD^{-1/2}$ (as in [[Graph Neural Networks]]).
3. Combine modalities: $\tilde A=w_{img}\tilde A_{img}+w_{txt}\tilde A_{txt}$.
4. Propagate item embeddings over it, $h_i\leftarrow\sum_j\tilde A_{ij}h_j$, and combine with a LightGCN backbone on the user–item graph.

**LATTICE** *learns* the graph: features pass through trainable projections and the kNN graph is rebuilt from the projected features during training. **FREEDOM** observes the learned graph adds little: it **freezes** the kNN graph built once from raw features and instead **denoises the user–item graph** (dropping edges with a degree-aware sampler). No graph rebuilding means much faster training, and denoising removes misleading interactions, which is why it is also more accurate.

### Contrastive alignment (InfoNCE)
To make an item's image and text embeddings agree, treat (image $k$, text $k$) as a positive pair and other texts in the batch as negatives. With L2-normalised embeddings $v_k,t_k$ and temperature $\tau$:
$$L_{v\to t}=-\frac1B\sum_k\log\frac{e^{v_k^\top t_k/\tau}}{\sum_je^{v_k^\top t_j/\tau}}.$$
CLIP's loss is the symmetric version: the average of $L_{v\to t}$ and $L_{t\to v}$. It is the same in-batch softmax used by two-tower recommenders ([[Deep Learning Recommenders]]).

## Worked example

**A VBPR score.** $\alpha=1$, $\beta_u=0.1$, $\beta_i=0.3$, $\gamma_u=(0.5,1)$, $\gamma_i=(1,0.2)$, $\theta_u=(2,0)$, $E=\begin{pmatrix}0.2&0&0.4\\0&0.5&0\end{pmatrix}$, $f_i=(1,2,0.5)$.
- $Ef_i=(0.2+0.2,\ 1.0)=(0.4,\,1.0)$, so the visual term is $\theta_u^\top Ef_i=0.8$.
- ID term $\gamma_u^\top\gamma_i=0.5+0.2=0.7$.
- $\hat x_{ui}=1+0.1+0.3+0.7+0.8=2.9$.

**Attention fusion** (the animation's numbers). Modality scores $s=(0.9,0.2,0.5)$ for (image, text, ID).
- User A, logits $(1.5,0,0.3)$: $e^{1.5}=4.48$, $e^0=1$, $e^{0.3}=1.35$, sum $6.83$, weights $\approx(0.66,0.15,0.20)$, fused $\approx0.66\cdot0.9+0.15\cdot0.2+0.20\cdot0.5\approx0.72$.
- User B, logits $(0,1.5,0.3)$: weights $\approx(0.15,0.66,0.20)$, fused $\approx0.36$.

**InfoNCE.** Two items, cosine matrix $\begin{pmatrix}0.7&0.1\\0.3&0.6\end{pmatrix}$ (rows images, columns texts), $\tau=0.5$. Row 1 logits $(1.4,0.2)$: $p=\frac{e^{1.4}}{e^{1.4}+e^{0.2}}\approx0.77$, loss $0.26$. Row 2 logits $(0.6,1.2)$: $p\approx0.65$, loss $0.44$. Mean $L_{v\to t}\approx0.35$.

## Benchmarks & evaluation
- Datasets: [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/) (Baby, Sports, Clothing… with images + text), TikTok, Kwai, MovieLens + posters/trailers, MIND (news).
- Metrics: Recall@K, NDCG@K under full ranking ([[Evaluating Recommenders]]).
- Open question worth knowing for your thesis/exam: do multimodal features *actually* help, or do tuned ID-based baselines close the gap? Check ablations without each modality.

**A fair ablation.** Train ID-only, image+ID, text+ID, image+text+ID (and content-only) variants with the *same* tuning budget each; report Recall@K/NDCG@K with full ranking on the same temporal split, with several seeds; break results down by item popularity (cold / tail / head) and user activity. Multimodal gains usually concentrate on cold and tail items; if they vanish on the head and for a well-tuned ID baseline, say so.

## Code
- [**MMRec toolbox**](https://github.com/enoche/MMRec) — PyTorch implementations of VBPR, MMGCN, GRCN, DualGNN, LATTICE, SLMRec, BM3, FREEDOM, MGCN, DRAGON… with a common pipeline. Best place to start experiments.
- Image/text features: CLIP via Hugging Face ([[Tools and Libraries]]).

## Common confusions

- **"More modalities always help."** → Only if they carry taste information the IDs do not. Well-tuned ID baselines often close the gap on warm items; ablations decide.
- **"Concatenating features is neutral."** → Without per-modality normalisation, the modality with the largest scale or dimension dominates every distance.
- **"Frozen encoders mean nothing is learned about content."** → The projection ($E$ in VBPR), attention weights and graph layers on top are learned; only the big encoder is fixed.
- **"FREEDOM is LATTICE plus more learning."** → The opposite: it *removes* graph learning (freezes the kNN graph) and spends effort on denoising the user–item graph instead.
- **"Cold items get random scores."** → In VBPR-style models their ID terms are zero but the content term still ranks them meaningfully.

## Check yourself

> [!question]- How does VBPR rank a brand-new item with no interactions?
> Its $\beta_i$ and $\gamma_i$ are zero (never trained), so the score comes from $\theta_u^\top Ef_i$: how well the item's projected visual features match the user's learned visual preferences.

> [!question]- Name the fusion strategy: "per-modality recommenders each produce a score, combined by a weighted sum".
> Late fusion. Its main risk: it misses cross-modal interactions.

> [!question]- What does LATTICE learn that FREEDOM freezes, and what does FREEDOM denoise instead?
> LATTICE learns the item–item graph from projected modality features during training; FREEDOM freezes the kNN graph built once from raw features and denoises the user–item interaction graph.

> [!question]- Why divide each modality by $\sqrt{d_m}$ before early fusion?
> After z-scoring, a $d_m$-dimensional block has expected squared norm $d_m$; dividing by $\sqrt{d_m}$ gives every modality the same expected norm, so none dominates by having more dimensions.

> [!question]- Why is the InfoNCE loss low when the diagonal of the similarity matrix is large?
> Each row's softmax then puts most probability on the matching pair, so $-\log$ of that probability is close to zero.

## Practice

[Multimodal Recommender Systems - Exercises](Multimodal%20Recommender%20Systems%20-%20Exercises.ipynb): why and when multimodal, fusion choices, frozen encoders, ablation design, LATTICE vs FREEDOM; VBPR scores and parameter counts, cold items, late vs attention fusion, a kNN graph and InfoNCE by hand; then early fusion, a LATTICE-style graph, attention fusion, the CLIP loss, VBPR for cold-start items and a modality ablation in code.

## Connections
[[Content-Based and Hybrid Recommenders]] (content is a single-modality version) · [[Deep Learning Recommenders]] · [[Graph Neural Networks]] (LightGCN backbone) · [[Recommender Systems Overview]]

## Learn more
- [Multimodal Recommender Systems: A Survey — Liu et al. (ACM CSUR)](https://arxiv.org/abs/2302.03883)
- [MMRec toolbox](https://github.com/enoche/MMRec)
- [Lilian Weng — Contrastive Representation Learning](https://lilianweng.github.io/posts/2021-05-31-contrastive/)
- [CLIP paper](https://arxiv.org/abs/2103.00020)
