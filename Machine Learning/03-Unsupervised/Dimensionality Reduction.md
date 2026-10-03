---
tags: [ml, unsupervised, dimensionality-reduction]
status: not-started
notebook: not-started
level:
reviewed:
---
# Dimensionality Reduction

> [!summary] In one sentence
> Dimensionality reduction maps data with many features to a few new coordinates while preserving whatever structure you care about (variance, distances, neighbourhoods or class separation), and choosing a method mostly means choosing *which* structure to keep.

## Intuition first

A world map is dimensionality reduction: the Earth's surface is curved 3-D, the map is flat 2-D. Every projection distorts something. Mercator keeps angles but inflates Greenland; equal-area maps keep areas but bend shapes. No flat map keeps everything, so cartographers pick the distortion that matters least for the job. Dimensionality reduction is the same trade-off for data.

Motivation: curse of dimensionality, noise, compression, visualization.
- **Curse of dimensionality**: in high dimensions data become sparse, distances lose contrast and you need exponentially many samples to cover the space (details below). Fewer dimensions make k-NN, clustering and density estimation work again.
- **Noise**: many measured features are redundant or noisy; projecting onto the main structure removes some of the noise.
- **Compression**: store or transmit fewer numbers; speed up downstream models.
- **Visualization**: humans can only look at 2-D or 3-D.

A key idea is the **manifold hypothesis**: real high-dimensional data (images, speech) usually lie near a much lower-dimensional, possibly curved surface (a *manifold*). A $64\times64$ photo of a face lives in 4096-D space, but the faces only vary along a handful of directions (pose, lighting, expression). Linear methods find flat subspaces; non-linear methods try to follow the curved manifold.

![A spiral of points flattened two ways: PCA mixes the colours, Isomap keeps them in order](../../Attachments/ML%20Animations/Dimensionality%20Reduction%20-%20PCA%20vs%20Isomap%20unrolling.gif)
*Watch the colours on the two bottom lines: PCA squashes the spiral straight down, so points from different turns land on top of each other, while Isomap measures distance along the curve and unrolls it with the colour gradient intact.*

## The methods

| Method | Type | Preserves |
|---|---|---|
| [[PCA]] | linear | global variance |
| LDA | linear, supervised | class separation ([[Linear Models for Classification]]) |
| Kernel PCA | non-linear | variance in feature space ([[Kernel Methods]]) |
| MDS / Isomap | non-linear | distances / geodesics |
| **t-SNE** | non-linear | local neighbourhoods; for visualization only |
| **UMAP** | non-linear | local + some global structure |
| Autoencoder | non-linear | reconstruction ([[Generative Models]]) |
| Random projection | linear | distances (Johnson–Lindenstrauss) |

> [!warning]
> Distances and cluster sizes in t-SNE / UMAP plots are not reliable. Do not over-interpret.

## The math, step by step

### The curse of dimensionality, three effects
1. **Volume moves to the boundary.** The fraction of the unit cube $[0,1]^d$ that lies *within 0.05 of the boundary* is $1-0.9^d$. That is about 65% for $d=10$ and essentially 100% for $d=100$. Almost every point is "near the edge" and far from the centre.
2. **Distances concentrate.** For random points, the ratio $\frac{d_{\max}-d_{\min}}{d_{\min}}$ between a query's farthest and nearest neighbour shrinks toward 0 as $d$ grows. If all points are about equally far away, "nearest neighbour" carries little information (bad for k-NN and clustering).
3. **Sample complexity explodes.** Covering each axis with 10 bins needs $10^d$ cells; to estimate a density or search a grid you need exponentially many samples.

### PCA (linear, unsupervised)
Projects onto the top-$k$ eigenvectors of the covariance; keeps maximal variance, equivalently minimal squared reconstruction error. See [[PCA]].

### LDA (linear, supervised)
Fisher's Linear Discriminant Analysis uses the labels. With between-class scatter $S_B$ and within-class scatter $S_W$, it maximises
$$J(w)=\frac{w^\top S_B w}{w^\top S_W w},$$
"spread the class means apart, keep each class tight". For two classes the solution is $w\propto S_W^{-1}(\mu_1-\mu_2)$. In general the directions are the top eigenvectors of $S_W^{-1}S_B$, and because $S_B$ has rank at most $C-1$, LDA returns **at most $C-1$ components** for $C$ classes (PCA can return up to $d$).

### Kernel PCA (non-linear via the kernel trick)
Do PCA in a feature space $\phi(x)$ without ever computing $\phi$: build the kernel matrix $K_{ij}=k(x_i,x_j)$, centre it in feature space,
$$\tilde K=K-\mathbf 1_NK-K\mathbf 1_N+\mathbf 1_NK\mathbf 1_N,\qquad(\mathbf 1_N)_{ij}=\tfrac1N,$$
and take its top eigenvectors $\alpha_k$ (scaled so $\lambda_k\lVert\alpha_k\rVert^2=1$). The $k$-th coordinate of training point $i$ is $\lambda_k\alpha_{ik}$ (equivalently $(\tilde K\alpha_k)_i$). Needs an $N\times N$ matrix, so it scales poorly; see [[Kernel Methods]].

### MDS and Isomap (keep distances)
**Classical MDS** takes a matrix of pairwise distances $D$ and finds coordinates whose Euclidean distances match it:
1. Square the distances, $D^{(2)}_{ij}=d_{ij}^2$, and double-centre: $B=-\tfrac12 J D^{(2)} J$ with $J=I-\tfrac1N\mathbf 1\mathbf 1^\top$. $B$ is the Gram matrix $XX^\top$ of centred coordinates.
2. Eigendecompose $B=V\Lambda V^\top$ and set $Y=V_k\Lambda_k^{1/2}$.

With Euclidean input distances classical MDS gives exactly the PCA scores. **Isomap** makes it non-linear by changing the distances: build a k-nearest-neighbour graph, replace each distance by the **shortest-path (geodesic) distance** through the graph, then run classical MDS. Walking along the graph follows the manifold, which is why it can unroll a Swiss roll (the animation above). Weakness: one "short-circuit" edge across a gap ruins the geodesics.

### t-SNE (keep neighbourhoods, for pictures)
1. In high-D, turn distances into neighbour probabilities $p_{j\mid i}\propto\exp(-\lVert x_i-x_j\rVert^2/2\sigma_i^2)$, with $\sigma_i$ tuned per point so the effective number of neighbours equals the **perplexity** (typically 5–50). Symmetrise to $p_{ij}$.
2. In 2-D, use a heavy-tailed Student-t: $q_{ij}\propto(1+\lVert y_i-y_j\rVert^2)^{-1}$.
3. Move the $y_i$ by gradient descent to minimise $\mathrm{KL}(P\Vert Q)=\sum p_{ij}\log\frac{p_{ij}}{q_{ij}}$.

KL heavily punishes putting true neighbours far apart, but barely cares about non-neighbours, so **local** structure is kept and global geometry is not. The heavy tail lets moderately distant points spread out, which creates the well-separated "islands". The $\sigma_i$ adapt to local density, so dense and sparse clusters come out about the same size. Hence the warning: cluster **sizes** and **gaps between clusters** in a t-SNE plot carry little meaning, and there is no mapping for new points.

### UMAP
Builds a fuzzy k-NN graph in high-D and optimises a low-D layout whose fuzzy graph matches it (a cross-entropy objective). It keeps local structure like t-SNE, keeps **somewhat more global structure**, is faster, and can transform new points. The same warning about sizes and distances applies.

### Autoencoders
A neural network encoder $z=f(x)$ squeezes $x$ through a narrow bottleneck and a decoder $\hat x=g(z)$ reconstructs it; train to minimise $\lVert x-\hat x\rVert^2$. A linear autoencoder with squared loss learns the same subspace as PCA; non-linear layers let it follow curved manifolds. See [[Generative Models]].

### Random projection and Johnson–Lindenstrauss
Multiply by a random $k\times d$ Gaussian matrix (entries $\mathcal N(0,1/k)$). No training at all. The **Johnson–Lindenstrauss lemma** says $N$ points can be mapped to
$$k\ \ge\ \frac{4\ln N}{\varepsilon^2/2-\varepsilon^3/3}$$
dimensions while every pairwise distance is preserved within a factor $1\pm\varepsilon$ (with high probability). Remarkably $k$ depends on $N$ and $\varepsilon$ but **not on the original dimension $d$**.

## Worked example

**Hypercube shell.** Inner cube $[0.05,0.95]^d$ has side 0.9 and volume $0.9^d$.
- $d=10$: $0.9^{10}\approx0.349$, so $65\%$ of the volume is in the thin 0.05 shell.
- $d=100$: $0.9^{100}\approx2.7\times10^{-5}$, so $99.997\%$ is in the shell.

**JL target dimension** for $N=10\,000$ points and $\varepsilon=0.1$: $\ln N\approx9.21$; denominator $0.005-0.000333=0.004667$; $k\ge4\times9.21/0.004667\approx7\,900$. Useful when $d$ is in the hundreds of thousands (bag-of-words), pointless when $d=50$.

**LDA vs PCA picture.** Two long, parallel, cigar-shaped classes side by side, cigars pointing along $x$: PC1 points along the cigars ($x$), and projecting onto it mixes the classes completely. LDA's $S_W^{-1}(\mu_1-\mu_2)$ points along $y$, across the cigars, and separates them perfectly.

## Choosing a method
- Preprocessing for a model, want speed and invertibility: **PCA** (or **random projection** when $d$ is huge and you can't afford PCA).
- Have labels, want features for a classifier: **LDA**.
- 2-D picture for exploration or a paper figure: **t-SNE** or **UMAP**, then check claims against the raw data.
- Data on a smooth curved sheet: **Isomap** (or kernel PCA / UMAP).
- Lots of data and complex structure (images): **autoencoder**.
- Measure how faithful a 2-D embedding is: **trustworthiness** (do points that are neighbours in the embedding really neighbour each other in the original space? 1 = perfect).

## Common confusions
- *"Cluster A is bigger than B in the t-SNE plot, so A is more diverse."* → t-SNE equalises densities; sizes are not meaningful.
- *"A and C are far apart in t-SNE, so they are very different."* → Only local neighbourhoods are trustworthy; between-cluster distances are not.
- *"I see 7 islands, so there are 7 clusters."* → Perplexity and random seed can split or merge islands; verify with a clustering on the original data and several perplexities.
- *"Non-linear is always better than PCA."* → On linear structure PCA is optimal, fast, deterministic and invertible.
- *"LDA is a clustering / unsupervised method."* → It needs labels, and gives at most $C-1$ components.
- *"Random projection loses everything because it ignores the data."* → JL guarantees distances survive with $k=O(\log N/\varepsilon^2)$.

## Check yourself

> [!question]- Which method for a quick, training-free compression of 10 000-dimensional bag-of-words vectors for nearest-neighbour search?
> Random projection: JL preserves pairwise distances, needs no fitting and is cheap.

> [!question]- How many LDA components can you get with 3 classes and 20 features?
> At most $C-1=2$, because $S_B$ has rank at most 2.

> [!question]- Why can't PCA unroll a Swiss roll, while Isomap can?
> PCA can only rotate and drop axes (a linear projection), which stacks the layers of the roll on top of each other. Isomap uses geodesic distances along a neighbour graph, which measure distance along the sheet, and MDS then lays those distances out flat.

> [!question]- What does perplexity control in t-SNE?
> The effective number of neighbours each point considers (through its bandwidth $\sigma_i$). Small perplexity focuses on very local structure; large perplexity considers broader neighbourhoods.

## Practice
[Dimensionality Reduction - Exercises](Dimensionality%20Reduction%20-%20Exercises.ipynb): the curse of dimensionality, JL, classical MDS, Fisher LDA, kernel PCA centring, PCA vs Isomap on the Swiss roll, and trustworthiness.

## Learn more
- [scikit-learn – manifold learning](https://scikit-learn.org/stable/modules/manifold.html)
- [scikit-learn – decomposition](https://scikit-learn.org/stable/modules/decomposition.html)
- [Distill – How to Use t-SNE Effectively](https://distill.pub/2016/misread-tsne/): interactive demos of every t-SNE pitfall above.
- [UMAP documentation](https://umap-learn.readthedocs.io/)
