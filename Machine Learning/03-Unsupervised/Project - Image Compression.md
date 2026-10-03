---
tags: [ml, project, clustering, pca]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Image Compression

> [!summary] In one sentence
> Compress one photo two ways, k-means on colours and low-rank SVD on structure, verify the Eckart–Young theorem numerically, and compare quality per bit.

**Notebook:** [Project - Image Compression](Project%20-%20Image%20Compression.ipynb) · topic: [[Clustering]] · all projects: [[Projects Overview]]

## What you build
1. `kmeans_step`: one Lloyd iteration (assign + update).
2. `low_rank`: best rank-k approximation via SVD.
3. `storage_bits`: what each method really costs to store.

## Reference results (solution, laptop CPU)
| method | PSNR | size vs. original |
|---|---|---|
| k-means 16 colours | 27.3 dB | 16.7 % |
| k-means 64 colours | 31.5 dB | 25.0 % |
| SVD rank 20 | 20.8 dB | 31.3 % |
| SVD rank 80 | 25.2 dB | 125 % (bigger than the photo!) |

For natural photos, colour quantisation wins clearly at equal size.

## Check yourself
> [!question]- Why does rank-80 SVD take more space than the original?
> Each rank stores h + w + 1 float32 numbers per channel: 80 × 1068 × 3 × 32 bits ≈ 8.2 Mbit, versus 427 × 640 × 24 ≈ 6.6 Mbit for the raw image. Low rank only pays off when k ≪ min(h, w).

> [!question]- What does Eckart–Young guarantee?
> Truncated SVD is the best rank-k approximation in Frobenius (and spectral) norm, with error $\sqrt{\sum_{i>k}\sigma_i^2}$.

---
Back to [[00 - Machine Learning Index]].
