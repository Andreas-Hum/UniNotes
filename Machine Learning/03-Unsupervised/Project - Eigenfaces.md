---
tags: [ml, project, pca, faces]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Eigenfaces

> [!summary] In one sentence
> Run PCA via SVD on 400 face images (the Olivetti/AT&T dataset), look at the eigenfaces, reconstruct faces from a few components, and recognise people with nearest neighbours in eigenface space.

**Notebook:** [Project - Eigenfaces](Project%20-%20Eigenfaces.ipynb) · topic: [[PCA]] · all projects: [[Projects Overview]]

## What you build
1. `pca`: mean, top-k right singular vectors and explained variances.
2. `reconstruct`: project and map back.

## Reference results (solution, laptop CPU)
61 of 4,096 dimensions explain 90 % of the variance.

| features | 1-NN accuracy (40 people) |
|---|---|
| 5 eigenfaces | 75 % |
| 20 eigenfaces | 91 % |
| **50 eigenfaces** | **93 %** |
| 4,096 raw pixels | 93 % |

## Check yourself
> [!question]- Why compute PCA with SVD instead of the covariance matrix?
> The covariance is 4,096 × 4,096; the SVD of the centred 300 × 4,096 data matrix is cheaper and numerically more accurate (no squaring of the condition number).

> [!question]- What do the first eigenfaces capture?
> Mostly lighting direction and overall face shape, not identity, which is why dropping the first few can improve recognition.

---
Back to [[00 - Machine Learning Index]].
