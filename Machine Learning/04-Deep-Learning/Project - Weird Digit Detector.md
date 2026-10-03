---
tags: [ml, project, autoencoders, anomaly-detection]
status: not-started
notebook: not-started
level: I
reviewed:
---
# Project - Weird Digit Detector

> [!summary] In one sentence
> Train an autoencoder with an 8-number bottleneck on normal handwritten digits only, and use reconstruction error to flag noisy, inverted and scribbled digits it has never seen.

**Notebook:** [Project - Weird Digit Detector](Project%20-%20Weird%20Digit%20Detector.ipynb) · topic: [[Neural Networks]] · all projects: [[Projects Overview]]

## What you build
1. `AE`: 64 → 32 → 8 → 32 → 64 with a sigmoid output.
2. `recon_error`: per-image mean squared reconstruction error = anomaly score.

## Reference results (solution, laptop CPU)
ROC AUC weird vs. normal: **1.000** overall and for each corruption type (noise, inverted, scribble), so these corruptions are easy. The stretch goals make it harder (bottleneck size, novel digit classes).

## Check yourself
> [!question]- Why must the bottleneck be small?
> With a large bottleneck the autoencoder learns something close to the identity and reconstructs anything, including anomalies. Compression forces it to model only what normal digits have in common.

> [!question]- How is this related to PCA?
> A linear autoencoder with MSE loss learns the same subspace as PCA with k components. The ReLUs let it model curved structure.

---
Back to [[00 - Machine Learning Index]].
