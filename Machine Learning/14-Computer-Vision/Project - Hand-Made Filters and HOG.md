---
tags: [ml, project, computer-vision, features]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Hand-Made Filters and HOG

> [!summary] In one sentence
> Implement 2-D convolution by hand, apply blur, sharpen and Sobel kernels to a photo, then build HOG features and show that they help a linear classifier on digits.

**Notebook:** [Project - Hand-Made Filters and HOG](Project%20-%20Hand-Made%20Filters%20and%20HOG.ipynb) · topic: [[Computer Vision Overview]] · all projects: [[Projects Overview]]

## What you build
1. `conv2d`: valid cross-correlation (checked against SciPy).
2. `hog`: gradient orientations → per-cell magnitude-weighted histograms.

## Reference results (solution, laptop CPU)
Linear SVM trained on only 200 digit images:

| features | test accuracy |
|---|---|
| raw pixels (64) | 0.925 |
| HOG only (36) | 0.805 |
| **pixels + HOG (100)** | **0.942** |

On tiny 8×8 digits HOG alone loses information, but it complements the pixels.

## Check yourself
> [!question]- Why is the Sobel-x response large on vertical edges?
> It measures the horizontal intensity change (right minus left), which is largest across a vertical boundary.

> [!question]- Why use unsigned orientations (0–180°) in HOG?
> A dark-to-light and a light-to-dark edge at the same angle describe the same shape, so you don't want them in different bins.

---
Back to [[00 - Machine Learning Index]].
