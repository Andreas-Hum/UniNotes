---
tags: [ml, deep-learning, representation-learning]
---
# Self-Supervised and Contrastive Learning

Learn representations from unlabeled data by inventing a **pretext task**; then fine-tune or use a linear probe.

## Families
| Family | Pretext task | Examples |
|---|---|---|
| **Contrastive** | pull augmented views of the same sample together, push others apart | SimCLR, MoCo, CLIP (image–text) |
| Non-contrastive | match views without negatives (stop-gradient, momentum encoder) | BYOL, SimSiam, DINO, BM3 ([[Multimodal Recommender Systems]]) |
| Masked modeling | reconstruct masked parts | BERT ([[Transformers]]), MAE |
| Autoregressive | predict the next token | GPT ([[LLMs Overview]]) |

## InfoNCE / NT-Xent loss
For anchor $z_i$, positive $z_j$, temperature $\tau$:
$$\ell_{i}=-\log\frac{\exp(\mathrm{sim}(z_i,z_j)/\tau)}{\sum_{k\neq i}\exp(\mathrm{sim}(z_i,z_k)/\tau)}$$
Same form as the in-batch softmax of two-tower recommenders ([[Deep Learning Recommenders]]).

## Practical lessons (SimCLR)
Strong augmentation composition (crop + colour), a projection head, large batches / many negatives, temperature matters. Collapse (all embeddings equal) is the failure mode to watch for.

## Learn more
- [SimCLR — Chen et al. 2020](https://arxiv.org/abs/2002.05709)
- [CLIP — Radford et al. 2021](https://arxiv.org/abs/2103.00020)
- [Lilian Weng — Contrastive Representation Learning](https://lilianweng.github.io/posts/2021-05-31-contrastive/)
