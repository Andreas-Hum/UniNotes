---
tags: [ml, unsupervised, clustering]
---
# Clustering

> [!summary] In one sentence
> Clustering groups unlabeled points so that points in the same group are similar and points in different groups are not, and every algorithm differs mainly in *what it means by "similar"* and *what shape it expects a group to have*.

## Intuition first

Imagine tipping a bag of mixed sweets onto a table and sorting them into piles without anyone telling you the categories. You might sort by colour, by shape, or by which ones are physically close together on the table. All of these are valid; they just answer different questions. Clustering is exactly this: **unsupervised** grouping, with no labels to check against.

What problem does it solve?
- **Discovery**: customer segments, gene-expression groups, topics in documents.
- **Compression / summarising**: replace thousands of points by a handful of prototypes (colour quantisation of images is k-means with $k$ = palette size).
- **Pre-processing**: cluster IDs as features, or one model per segment.

Three families of ideas cover almost every algorithm:
1. **Prototype-based** (k-means, k-medoids, GMM): a cluster is "the points nearest to a centre". Good for compact, blob-shaped groups.
2. **Connectivity / density-based** (hierarchical single linkage, DBSCAN, mean shift): a cluster is "a region you can walk through without crossing empty space". Handles odd shapes and noise.
3. **Graph-based** (spectral): build a similarity graph, then cut it where few edges cross. Handles non-convex shapes like two interlocking moons.

![k-means alternating between assigning points and moving centroids](../../Attachments/ML%20Animations/Clustering%20-%20k-means%20iterations.gif)
*Watch the two alternating moves: dots change colour to their nearest star, then each star jumps to the mean of its dots, and $J$ only ever goes down until nothing changes.*

## The algorithms at a glance

| Algorithm | Idea | Notes |
|---|---|---|
| **k-means** | alternate assign / recompute centroids, minimizes within-cluster SSE | needs $k$, spherical clusters, k-means++ init |
| **k-medoids** | centers are real points | robust |
| **Hierarchical (agglomerative)** | merge closest clusters; single/complete/average/Ward linkage | dendrogram, $O(N^2)$ |
| **DBSCAN** | density-connected points (ε, minPts) | arbitrary shapes, finds noise |
| **Spectral** | eigenvectors of graph Laplacian then k-means | non-convex clusters |
| **GMM** | soft assignments, see [[Gaussian Mixture Models and EM]] | probabilistic |
| **Mean shift** | climb density modes | bandwidth parameter |

## The math, step by step

### k-means objective
$$J=\sum_i\lVert x_i-\mu_{c(i)}\rVert^2$$
- $x_i$: the $i$-th data point (a vector of features).
- $c(i)\in\{1,\dots,k\}$: the cluster that point $i$ is assigned to.
- $\mu_j$: the centroid (centre) of cluster $j$.
- In words: $J$ is the **within-cluster sum of squared errors (SSE)**, the total squared distance from every point to its own centre. Small $J$ = tight clusters.

### Lloyd's algorithm (the standard k-means)
1. **Initialise** $k$ centroids (ideally with k-means++, below).
2. **Assignment step**: $c(i)=\arg\min_j\lVert x_i-\mu_j\rVert^2$, send each point to its nearest centroid.
3. **Update step**: $\mu_j=\frac{1}{|C_j|}\sum_{i\in C_j}x_i$, move each centroid to the mean of its points.
4. Repeat 2–3 until the assignments stop changing.

**Why $J$ never increases.** Each step minimises $J$ over one set of variables while holding the other fixed:
- Step 2 fixes the $\mu_j$ and picks, for each point separately, the centre with the smallest squared distance, so no other assignment could give a lower $J$.
- Step 3 fixes the assignments. For one cluster, $\sum_{i\in C_j}\lVert x_i-\mu\rVert^2$ is a convex quadratic in $\mu$; setting the gradient $-2\sum_{i\in C_j}(x_i-\mu)$ to zero gives $\mu=$ mean. So the mean is the best possible centre.
- Since $J\ge 0$ and there are only finitely many ways to partition $N$ points, the algorithm must stop. It **converges to a local minimum**, not necessarily the global one, so the result depends on the initialisation (run several restarts, `n_init` in scikit-learn).

**k-means is a hard-assignment special case of EM.** In a GMM ([[Gaussian Mixture Models and EM]]) the E-step gives each point a *soft* responsibility for every component. If all components share the covariance $\sigma^2 I$ and you let $\sigma\to 0$, the responsibilities become 0/1 (nearest centre wins) and the M-step mean update becomes the k-means update.

**Scale features first** ([[Data Preprocessing]]). k-means uses Euclidean distance, so a feature measured in thousands (income) will dominate one measured in units (age). Standardise unless the units are genuinely comparable.

### k-means++ initialisation
Pick the first centre uniformly at random from the data. Then pick each next centre at random with probability proportional to $D(x)^2$, the squared distance from $x$ to the nearest centre chosen so far. Far-away points are likely to be picked, so the initial centres spread out. This gives an expected $O(\log k)$ approximation to the optimal $J$ and in practice far fewer bad local minima.

### k-medoids
Same idea, but each centre must be an **actual data point** (the medoid), chosen to minimise the sum of distances to the other members. Because it cannot be dragged into empty space and can use any distance (including L1 or edit distance), it is **robust** to outliers.

### Hierarchical (agglomerative) clustering
Start with every point as its own cluster; repeatedly **merge the two closest clusters**. "Closest" is defined by the linkage:
- **Single**: $d(A,B)=\min_{a\in A,b\in B}d(a,b)$, the closest pair. Follows chains, so it finds elongated shapes but can "chain" two groups together through a thin bridge of points.
- **Complete**: $\max_{a,b} d(a,b)$, the farthest pair. Prefers compact, similar-diameter clusters.
- **Average**: mean of all pairwise distances. A compromise.
- **Ward**: merge the pair whose merge increases the total within-cluster SSE the least (the same quantity as $J$).

The full merge history is drawn as a **dendrogram**: the height of each join is the linkage distance at which it happened. Cut the tree at a height to get clusters. Cost: needs all pairwise distances, so at least $O(N^2)$ memory and time, which limits it to tens of thousands of points.

### DBSCAN
Two parameters: radius ε and a count minPts.
- A **core point** has at least minPts points (itself included, scikit-learn convention) within distance ε.
- A **border point** is within ε of a core point but is not core itself.
- Everything else is **noise** (label $-1$).
- Clusters are the sets of points **density-connected** through chains of core points.

You do not choose $k$; the number of clusters falls out. Clusters can have **arbitrary shapes**, and outliers are explicitly labelled as noise. Weakness: a single ε cannot fit clusters of very different densities.

### Spectral clustering
1. Build a similarity graph $W$ (e.g. $W_{ij}=\exp(-\lVert x_i-x_j\rVert^2/2\sigma^2)$ or a k-NN graph) and its degree matrix $D=\operatorname{diag}(\sum_j W_{ij})$.
2. Form the **graph Laplacian** $L=D-W$ (or a normalised version).
3. Take the eigenvectors of $L$ with the $k$ **smallest** eigenvalues as new coordinates for each point.
4. Run k-means on those rows.

Why it works: if the graph had $k$ disconnected components, $L$ would have exactly $k$ zero eigenvalues with indicator-like eigenvectors. Nearly disconnected groups give nearly such eigenvectors, so in the new coordinates the groups become well-separated blobs, even if they were **non-convex** in the original space (two moons, concentric rings).

### Mean shift
Place a kernel (window) of width = **bandwidth** around each point, move the point to the weighted mean of the data inside the window, and repeat. Points **climb to the modes** (peaks) of the estimated density; points ending at the same mode form a cluster. The bandwidth implicitly chooses the number of clusters.

## Worked example: k-means by hand

1-D data $\{1,2,4,10,11,12\}$, $k=2$, bad initial centres $\mu_1=1$, $\mu_2=4$.

| Step | Clusters | Centres | $J$ |
|---|---|---|---|
| assign | $\{1,2\}$, $\{4,10,11,12\}$ | $1,\ 4$ | $0+1+0+36+49+64=150$ |
| update | same | $1.5,\ 9.25$ | $0.5+38.75=39.25$ |
| assign | $\{1,2,4\}$, $\{10,11,12\}$ (4 is now closer to 1.5) | $1.5,\ 9.25$ | $6.75+11.19=17.94$ |
| update | same | $2.33,\ 11$ | $4.67+2=6.67$ |
| assign | no change → converged | | $6.67$ |

$J$ decreased at every half-step, exactly as the proof promises.

**Silhouette of the point $x=2$** in the final clustering: $a$ = mean distance to its own cluster mates $=\frac{1+2}{2}=1.5$; $b$ = mean distance to the nearest other cluster $=\frac{8+9+10}{3}=9$; $s=\frac{b-a}{\max(a,b)}=\frac{7.5}{9}\approx0.83$, a confidently placed point.

**Mean vs medoid**: for $\{1,2,3,4,100\}$ the mean is $22$ (a place where no point lives), while the medoid is $3$. One outlier moved the mean by 19 units and the medoid not at all.

## Choosing $k$
Elbow on SSE, silhouette score, gap statistic, BIC for GMM.
- **Elbow**: plot $J$ against $k$. $J$ always falls as $k$ grows ($k=N$ gives $J=0$), so look for the "elbow" where extra clusters stop buying much. Often ambiguous.
- **Silhouette score**: average of $s(i)=\frac{b(i)-a(i)}{\max(a(i),b(i))}\in[-1,1]$ over all points; pick the $k$ that maximises it. Near 1: well inside its cluster; near 0: on a boundary; negative: probably in the wrong cluster.
- **Gap statistic**: compare $\log J$ with what you would get on uniformly random reference data; choose the $k$ where the gap is largest (relative to its noise).
- **BIC for GMM**: likelihood penalised by number of parameters; lower is better ([[Gaussian Mixture Models and EM]]).

## Evaluation
Internal: silhouette, Davies–Bouldin. External: ARI, NMI ([[Model Evaluation and Metrics]]).
- **Internal** metrics use only the data and the clustering. Davies–Bouldin averages, over clusters, the worst ratio of (within-cluster scatter of both) / (distance between their centres); **lower is better**. Caveat: internal metrics favour the shapes their formula assumes (compact blobs), so they can rate DBSCAN's correct banana-shaped clusters poorly.
- **External** metrics compare with ground-truth labels when you have them (for benchmarking). The **Rand index** is the fraction of point *pairs* on which the two partitions agree (both "same cluster" or both "different"). **ARI** (adjusted Rand index) corrects it for chance so random labels score about 0 and a perfect match scores 1. **NMI** (normalised mutual information) measures shared information between the two labelings, in $[0,1]$. Both ignore the arbitrary names of the clusters.

## Which algorithm when?
- Compact, roughly equal-sized blobs, large $N$: **k-means** (fast, $O(Nkd)$ per iteration).
- Outliers or non-Euclidean distances: **k-medoids**.
- Want a hierarchy or a small dataset you want to explore at several granularities: **agglomerative** + dendrogram.
- Odd shapes, noise, unknown $k$: **DBSCAN** (or HDBSCAN for varying density).
- Non-convex shapes with a clear neighbourhood graph: **spectral**.
- Elliptical, overlapping clusters, or you need probabilities: **GMM**.
- Unknown $k$ and smooth density: **mean shift**.

## Common confusions
- *"k-means finds the best clustering."* → It finds a **local** minimum of $J$ that depends on initialisation; use k-means++ and several restarts.
- *"Lower SSE means a better $k$."* → SSE always falls as $k$ grows; you need a penalty or an elbow/silhouette argument.
- *"k-means works for any cluster shape."* → It implicitly assumes spherical, similar-size clusters (equal-variance Gaussians); stretched or nested clusters break it.
- *"Feature scaling does not matter for unsupervised learning."* → Distance-based methods are dominated by large-scale features; standardise first.
- *"DBSCAN has no hyperparameters because you do not set $k$."* → ε and minPts matter a lot; a k-distance plot helps pick ε.
- *"Cluster labels mean something."* → Label 0 vs 1 is arbitrary; that is why ARI/NMI are permutation-invariant.

## Check yourself

> [!question]- Why can't a Lloyd iteration increase $J$?
> The assignment step picks the closest centre for each point (best $c$ given $\mu$), and the update step sets each centre to its cluster mean, which minimises the sum of squared distances (best $\mu$ given $c$). Neither step can make $J$ larger.

> [!question]- Two long parallel strips of points: single or complete linkage?
> Single linkage: it merges along chains of near neighbours and so follows elongated shapes. Complete linkage prefers compact, round clusters and tends to cut the strips across.

> [!question]- When is a point labelled noise by DBSCAN?
> When it has fewer than minPts neighbours within ε (not core) and it is not within ε of any core point (not border).

> [!question]- A point has $a=4$ and $b=2$. What is its silhouette and what does it mean?
> $s=(2-4)/4=-0.5$. Negative: it is on average closer to another cluster than to its own, so it is probably misassigned.

> [!question]- What does k-means++ change, and what does it not change?
> It changes only the initial centres (spread out, sampled with probability $\propto D(x)^2$). The Lloyd iterations afterwards are identical.

## Practice
[Clustering - Exercises](Clustering%20-%20Exercises.ipynb): Lloyd and k-means++ from scratch, silhouette and Rand index by hand, DBSCAN and spectral clustering from scratch, and the effect of scaling and linkage.

## Learn more
- [scikit-learn – clustering](https://scikit-learn.org/stable/modules/clustering.html)
- [ISL / ISLP (free)](https://www.statlearning.com/) ch. 12
- [Naftali Harris – Visualizing k-means](https://www.naftaliharris.com/blog/visualizing-k-means-clustering/) and [Visualizing DBSCAN](https://www.naftaliharris.com/blog/visualizing-dbscan-clustering/): interactive, drag the initial centres yourself.
- [StatQuest videos](https://statquest.org/video_index.html): k-means and hierarchical clustering.
