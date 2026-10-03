---
tags: [ml, unsupervised, dimensionality-reduction]
status: not-started
notebook: not-started
level:
reviewed:
---
# PCA

> [!summary] In one sentence
> Principal Component Analysis rotates your coordinate system so the first axis points along the direction where the data spreads the most, the second along the most spread that is left (at right angles), and so on, so you can keep only the first few axes and lose as little information as possible.

## Intuition first

Find orthogonal directions of maximal variance.

Think of a cloud of points shaped like a flattened rugby ball floating in the air. If you had to describe each point with *one* number, the smartest choice is its position along the long axis of the ball: that number varies a lot from point to point, so it distinguishes them. Position along the short axis barely changes, so throwing it away loses little.

Or think of photographing a 3-D object: some camera angles show its shape clearly (the shadow is big and spread out), others squash it into a blob. PCA picks the camera angle whose "shadow" (projection) is as spread out as possible.

What problem does it solve?
- **Compression**: 784 pixel values → 50 numbers that keep most of the variation.
- **Visualisation**: project to 2-D or 3-D to look at the data.
- **Denoising**: noise is spread thinly over many directions; keeping the top components keeps signal and drops much of the noise.
- **Decorrelation**: the new features (principal components) are uncorrelated, which helps some models.

![A line rotating through the data until the projected variance is maximal, then points collapsing onto it](../../Attachments/ML%20Animations/PCA%20-%20projection%20onto%20PC1.gif)
*Watch the two numbers on the right: as the yellow line turns, the variance along it (yellow) and the mean squared red residual always add up to the same total, so maximising one is exactly minimising the other.*

## Algorithm
1. Center the data (and usually standardize, [[Data Preprocessing]]).
2. Covariance $S=\frac1N X^\top X$.
3. Eigen-decompose $S=Q\Lambda Q^\top$; keep top $k$ eigenvectors $W$.
4. Project $Z=XW$. Reconstruct $\hat X=ZW^\top$.

What each symbol is:
- $X$: the $N\times d$ data matrix, one centred point per row.
- $S$: the $d\times d$ covariance matrix. $S_{jj}$ is the variance of feature $j$; $S_{jl}$ is how features $j$ and $l$ vary together. ($\frac1N$ vs $\frac1{N-1}$ only rescales the eigenvalues; the directions are identical.)
- $Q$: columns are the eigenvectors $q_1,\dots,q_d$ (orthonormal, because $S$ is symmetric). These are the **principal directions** (loadings).
- $\Lambda=\operatorname{diag}(\lambda_1\ge\dots\ge\lambda_d\ge0)$: eigenvalues; $\lambda_i$ is the variance of the data along $q_i$.
- $W$: the $d\times k$ matrix of the first $k$ columns of $Q$.
- $Z=XW$: the $N\times k$ **scores**, the new coordinates of each point.
- $\hat X=ZW^\top$: the reconstruction back in the original $d$-dim space (add the mean back to undo centring).

**Why centre?** Covariance measures spread *around the mean*. Without centring the first "component" mostly points from the origin to the mean of the data, which is not a direction of variation at all.

**Why (usually) standardize?** PCA chases variance, and variance depends on units. A feature in grams has a variance $10^6$ times larger than the same feature in kilograms, so it would grab PC1 for no real reason. Standardising (each feature to variance 1) is the same as doing PCA on the **correlation** matrix. Skip it only when all features share a meaningful common unit (e.g. pixel intensities).

## The math, step by step

### Deriving PC1 (maximum variance)
Take a unit vector $w$ ($w^\top w=1$). The projection of point $x_i$ onto it is the number $z_i=w^\top x_i$. The variance of these numbers (data are centred, so their mean is 0) is
$$\frac1N\sum_i (w^\top x_i)^2=w^\top\Big(\frac1N\sum_i x_ix_i^\top\Big)w=w^\top S w .$$
Maximise $w^\top Sw$ subject to $w^\top w=1$ with a Lagrange multiplier:
$$\mathcal L=w^\top Sw-\lambda(w^\top w-1),\qquad \nabla_w\mathcal L=2Sw-2\lambda w=0\ \Rightarrow\ Sw=\lambda w .$$
So $w$ must be an **eigenvector** of $S$, and the variance it achieves is $w^\top S w=\lambda w^\top w=\lambda$. To make it as large as possible, pick the eigenvector with the **largest eigenvalue**. PC2 repeats the argument with the extra constraint $w\perp q_1$, giving the second eigenvector, and so on.

### Views
- Maximize projected variance = minimize reconstruction error.
- Probabilistic PCA: latent variable model with Gaussian noise ([[Probabilistic Graphical Models]]).

**Why the two views agree.** For a unit vector $w$, each centred point splits into a part along $w$ and a residual perpendicular to it. By Pythagoras,
$$\lVert x_i\rVert^2=\underbrace{(w^\top x_i)^2}_{\text{kept}}+\underbrace{\lVert x_i-(w^\top x_i)w\rVert^2}_{\text{lost}} .$$
Averaging over points: $\operatorname{tr}S=w^\top Sw+\text{mean squared reconstruction error}$. The left side is fixed by the data, so making the kept part as large as possible is the same as making the lost part as small as possible. More generally, keeping $k$ components,
$$\frac1N\sum_i\lVert x_i-\hat x_i\rVert^2=\sum_{i>k}\lambda_i ,$$
the reconstruction error is exactly the **sum of the discarded eigenvalues**.

**Probabilistic PCA** writes a generative model: a low-dimensional latent $z\sim\mathcal N(0,I_k)$ generates $x=Wz+\mu+\varepsilon$ with isotropic noise $\varepsilon\sim\mathcal N(0,\sigma^2 I)$. Its maximum-likelihood solution is closed-form: $\sigma^2_{\text{ML}}$ is the **average of the discarded eigenvalues** and $W_{\text{ML}}=Q_k(\Lambda_k-\sigma^2I)^{1/2}R$ for any rotation $R$. As $\sigma^2\to0$ you recover ordinary PCA. The probabilistic view gives a likelihood (for model comparison and anomaly scores), handles missing data via EM, and is the linear-Gaussian ancestor of factor analysis and VAEs.

### Equivalent via SVD
Equivalent via SVD of $X$ ([[Linear Algebra for ML]]): $X=U\Sigma V^\top$, components are columns of $V$, $\lambda_i=\sigma_i^2/N$.

Why: $S=\frac1N X^\top X=\frac1N V\Sigma U^\top U\Sigma V^\top=V\frac{\Sigma^2}{N}V^\top$, which is an eigendecomposition with $Q=V$ and $\Lambda=\Sigma^2/N$. The scores are $Z=XV_k=U_k\Sigma_k$. In practice SVD is preferred: it never forms $X^\top X$ (which squares the condition number and loses precision) and truncated/randomised SVD is fast for large data.

### Other useful facts
- **Power iteration** for PC1: start from a random $w$, repeat $w\leftarrow Sw/\lVert Sw\rVert$. Each multiplication amplifies the component along $q_1$ by $\lambda_1$ more than the others, so $w\to q_1$ at a rate set by $\lambda_2/\lambda_1$.
- **Whitening**: $Z\Lambda_k^{-1/2}$ rescales each component to variance 1, so the transformed data has identity covariance. Useful before ICA or some clustering; amplifies noise in small-eigenvalue directions.
- PCs are uncorrelated: the covariance of $Z$ is $W^\top SW=\Lambda_k$, a diagonal matrix.

## Worked example

Centred 2-D data with covariance $S=\begin{pmatrix}2&1\\1&2\end{pmatrix}$.

1. **Eigenvalues**: $\det(S-\lambda I)=(2-\lambda)^2-1=0\Rightarrow\lambda_1=3,\ \lambda_2=1$.
2. **Eigenvectors**: $q_1=\tfrac1{\sqrt2}(1,1)$ (the diagonal, where the two features move together), $q_2=\tfrac1{\sqrt2}(1,-1)$.
3. **Explained variance** of PC1: $\frac{3}{3+1}=75\%$.
4. **Project** the point $x=(2,0)$: $z=q_1^\top x=\tfrac{2}{\sqrt2}=\sqrt2\approx1.41$.
5. **Reconstruct**: $\hat x=z\,q_1=\sqrt2\cdot\tfrac1{\sqrt2}(1,1)=(1,1)$.
6. **Error**: $\lVert x-\hat x\rVert^2=\lVert(1,-1)\rVert^2=2$. This point lost its whole PC2 coordinate, $(q_2^\top x)^2=(\sqrt2)^2=2$. Averaged over all points, that loss would be $\lambda_2=1$.

## Choosing $k$
Explained variance ratio $\frac{\sum_{i\le k}\lambda_i}{\sum\lambda_i}$ (e.g. ≥ 95%), scree plot.
- The **explained variance ratio** is the fraction of total variance ($\operatorname{tr}S=\sum\lambda_i$) that the first $k$ components keep. With singular values: $\sum_{i\le k}\sigma_i^2/\sum_i\sigma_i^2$.
- A **scree plot** shows $\lambda_i$ against $i$; look for the point where the curve flattens into a "scree" of small, noise-level eigenvalues.
- If PCA feeds a model, the honest choice is to treat $k$ as a hyperparameter and pick it by cross-validation.

## Limits
Linear only, sensitive to scale, components hard to interpret. Non-linear alternatives in [[Dimensionality Reduction]].
- **Linear only**: data on a curved surface (a Swiss roll) cannot be flattened by a rotation + projection; see Kernel PCA, Isomap, UMAP.
- **Sensitive to scale**: see standardisation above. Also sensitive to **outliers**, since one extreme point can dominate the variance.
- **Hard to interpret**: each component mixes all original features with signed weights.
- **Variance ≠ usefulness**: the direction of largest variance can be useless for a classification task, while a low-variance direction separates the classes perfectly. With labels, consider LDA.

## Common confusions
- *"PCA selects the most important features."* → It builds *new* features as linear combinations of all the old ones; no original feature is dropped.
- *"I forgot to centre, but it's fine."* → Without centring, PC1 points toward the mean; scikit-learn centres for you, a hand-rolled SVD does not.
- *"Eigenvectors of $X^\top X$ and of $XX^\top$ are the same."* → Not the same matrices: $V$ (the $d$-dim directions) vs $U$ (the $N$-dim normalised scores). Their nonzero eigenvalues match.
- *"The sign of a component means something."* → $q$ and $-q$ are equally valid eigenvectors; different libraries may flip signs.
- *"95% explained variance means 95% accuracy is kept."* → It is about reconstruction of $X$, not about predicting $y$.

## Check yourself

> [!question]- Why is the variance along the unit direction $w$ equal to $w^\top Sw$?
> Projections are $z_i=w^\top x_i$ with mean 0 (centred data), so their variance is $\frac1N\sum (w^\top x_i)^2=w^\top(\frac1N\sum x_ix_i^\top)w=w^\top Sw$.

> [!question]- The singular values of a centred $X$ with $N=100$ are $10, 5, 1$. What fraction of variance does PC1 explain?
> $\lambda_i=\sigma_i^2/N$, so the ratio is $100/(100+25+1)=100/126\approx79\%$ (the $N$ cancels).

> [!question]- You keep $k$ components. What is the average squared reconstruction error?
> The sum of the discarded eigenvalues, $\sum_{i>k}\lambda_i$.

> [!question]- Your dataset has height in metres and salary in euros. What happens with unstandardised PCA?
> Salary has a vastly larger variance, so PC1 is essentially "salary" and height is ignored. Standardise first (PCA on the correlation matrix).

## Practice
[PCA - Exercises](PCA%20-%20Exercises.ipynb): eigendecomposition and projection by hand, the Lagrange derivation, PCA via covariance and via SVD, choosing $k$, whitening, power iteration and probabilistic PCA.

**Project:** [[Project - Eigenfaces]] – eigenfaces: PCA on faces and nearest-neighbour recognition

## Learn more
- [Mathematics for ML (free)](https://mml-book.github.io/) ch. 10
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 12
- [StatQuest videos](https://statquest.org/video_index.html)
- [Setosa – PCA explained visually](https://setosa.io/ev/principal-component-analysis/): drag points in 2-D/3-D and watch the components move.
- [3Blue1Brown – Essence of linear algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab): the eigenvectors and change-of-basis episodes are the geometric background.
