---
tags: [ml, recsys]
---
# Collaborative Filtering and Matrix Factorization

## Neighbourhood CF
- **User-based**: $\hat r_{ui}=\bar r_u+\frac{\sum_{v\in N(u)}\mathrm{sim}(u,v)(r_{vi}-\bar r_v)}{\sum|\mathrm{sim}(u,v)|}$
- **Item-based** (more stable, used by Amazon): similar items to what the user liked.
- Similarities: cosine, Pearson (mean-centred), Jaccard (implicit).

## Matrix factorization
Approximate the rating matrix $R\approx PQ^\top$, user vector $p_u$, item vector $q_i\in\mathbb R^k$:
$$\min_{P,Q}\sum_{(u,i)\in\Omega}\big(r_{ui}-\mu-b_u-b_i-p_u^\top q_i\big)^2+\lambda\big(\lVert p_u\rVert^2+\lVert q_i\rVert^2+b_u^2+b_i^2\big)$$
Only observed entries $\Omega$. (Netflix Prize "Funk SVD", Koren et al.)

### Optimisation
- **SGD**: $e=r-\hat r$; $p_u\leftarrow p_u+\eta(e\,q_i-\lambda p_u)$, $q_i\leftarrow q_i+\eta(e\,p_u-\lambda q_i)$ — see [[Gradient Descent]].
- **ALS**: fix $Q$ → each $p_u$ is a [[Linear Regression|ridge regression]] solved in closed form; alternate. Parallel, great for implicit data.

## Implicit feedback
- **Weighted MF (Hu, Koren, Volinsky 2008)**: preference $p_{ui}=\mathbb 1[r_{ui}>0]$, confidence $c_{ui}=1+\alpha r_{ui}$, sum over **all** pairs.
- **BPR (Bayesian Personalized Ranking)**: pairwise loss $-\sum\ln\sigma(\hat x_{ui}-\hat x_{uj})$ for observed $i$, unobserved $j$ — optimises ranking (AUC).
- Negative sampling for scalability.

## Extensions
SVD++ (implicit signals), timeSVD++ (temporal), factorization machines (side features, $\sum_{i<j}\langle v_i,v_j\rangle x_ix_j$), non-negative MF, probabilistic MF ([[Bayesian Inference]]).

## Relation to other topics
Truncated SVD/[[PCA]] on a filled matrix is a crude version; MF is shallow node embedding on the bipartite graph ([[Link Prediction]]).

```python
# Minimal MF with SGD (NumPy)
P = 0.1*np.random.randn(n_users, k); Q = 0.1*np.random.randn(n_items, k)
for epoch in range(20):
    for u, i, r in ratings:
        e = r - P[u] @ Q[i]
        P[u], Q[i] = P[u] + lr*(e*Q[i] - lam*P[u]), Q[i] + lr*(e*P[u] - lam*Q[i])
```
Libraries: `implicit`, `surprise`, `LightFM`, Spark MLlib ALS.
