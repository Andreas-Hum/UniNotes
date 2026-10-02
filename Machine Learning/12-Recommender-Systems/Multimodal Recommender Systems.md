---
tags: [ml, recsys, multimodal]
---
# Multimodal Recommender Systems

Use **item content in several modalities** (images, text, audio, video) together with user–item interactions. Typical domains: e-commerce/fashion (product photo + title + description), micro-video (TikTok-style: visual + acoustic + text), news, music.

> [!info] Why bother?
> Pure [[Collaborative Filtering and Matrix Factorization|CF]] only knows IDs. Content features help with **cold-start items**, **sparse data**, and **visually-driven taste** (fashion, art, food).

## The general pipeline
1. **Modality encoders** (usually frozen, pre-extracted): CNN/ViT or **CLIP** for images ([[Computer Vision Overview]]), BERT/Sentence-BERT for text ([[Text Representations]]), VGGish for audio.
2. **Feature interaction / fusion**: how modalities and IDs combine.
3. **Feature enhancement**: self-supervised / contrastive objectives to align modalities ([[Self-Supervised and Contrastive Learning]]).
4. **Optimisation**: usually BPR loss on implicit feedback ([[Collaborative Filtering and Matrix Factorization]]).

This four-part split follows the taxonomy of the [Liu et al. survey](https://arxiv.org/abs/2302.03883).

## Fusion strategies
| Strategy | How | Trade-off |
|---|---|---|
| Early fusion | concatenate features before the model | simple; one modality can dominate |
| Late fusion | separate per-modality scores, then combine | flexible; misses cross-modal interactions |
| Attention fusion | learn per-user/per-item modality weights | personalised, more parameters |
| Graph-based | modality-specific or item–item graphs + GCN | current state of the art on benchmarks |

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

## Benchmarks & evaluation
- Datasets: [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/) (Baby, Sports, Clothing… with images + text), TikTok, Kwai, MovieLens + posters/trailers, MIND (news).
- Metrics: Recall@K, NDCG@K under full ranking ([[Evaluating Recommenders]]).
- Open question worth knowing for your thesis/exam: do multimodal features *actually* help, or do tuned ID-based baselines close the gap? Check ablations without each modality.

## Code
- [**MMRec toolbox**](https://github.com/enoche/MMRec) — PyTorch implementations of VBPR, MMGCN, GRCN, DualGNN, LATTICE, SLMRec, BM3, FREEDOM, MGCN, DRAGON… with a common pipeline. Best place to start experiments.
- Image/text features: CLIP via Hugging Face ([[Tools and Libraries]]).

## Connections
[[Content-Based and Hybrid Recommenders]] (content is a single-modality version) · [[Deep Learning Recommenders]] · [[Graph Neural Networks]] (LightGCN backbone) · [[Recommender Systems Overview]]

## Learn more
- [Multimodal Recommender Systems: A Survey — Liu et al. (ACM CSUR)](https://arxiv.org/abs/2302.03883)
- [MMRec toolbox](https://github.com/enoche/MMRec)
- [Lilian Weng — Contrastive Representation Learning](https://lilianweng.github.io/posts/2021-05-31-contrastive/)
- [CLIP paper](https://arxiv.org/abs/2103.00020)
