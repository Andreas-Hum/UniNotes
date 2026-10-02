---
tags: [ml, recsys]
---
# Collaborative Filtering and Matrix Factorization

> [!summary] In one sentence
> Collaborative filtering predicts what you will like from the behaviour of people with similar taste, and matrix factorization does this by giving every user and every item a short vector of "taste factors" so that a dot product reproduces the known ratings and fills in the unknown ones.

## Intuition first

**Collaborative** filtering never looks at what an item *is*. It only looks at *who* interacted with it. If you and I both loved the same five films, and I also loved a sixth one you have not seen, it is a good bet for you. No genres, no plot summaries: the crowd's behaviour is the signal.

There are two ways to turn that into an algorithm:

1. **Neighbourhood methods** (memory-based): find similar users (or similar items) and average their ratings. Like asking your friends with similar taste.
2. **Matrix factorization** (model-based): assume taste is driven by a few hidden factors. A film might be 80% "action", 10% "romance"; a user might care a lot about action and not at all about romance. Learn these hidden numbers for everyone at once, so that *user factors · item factors ≈ rating*.

The analogy for MF: describing every song by a handful of sliders (energy, acousticness, mood…) and every listener by how much they like each slider. Nobody tells the model what the sliders mean; it discovers whatever factors best explain the ratings.

## Neighbourhood CF

- **User-based**: $\hat r_{ui}=\bar r_u+\frac{\sum_{v\in N(u)}\mathrm{sim}(u,v)(r_{vi}-\bar r_v)}{\sum|\mathrm{sim}(u,v)|}$
- **Item-based** (more stable, used by Amazon): similar items to what the user liked.
- Similarities: cosine, Pearson (mean-centred), Jaccard (implicit).

Reading the user-based formula from left to right:
- start from the user's own average $\bar r_u$ (a generous rater stays generous);
- each neighbour $v$ contributes how much they *deviated from their own average* on item $i$, $r_{vi}-\bar r_v$, weighted by how similar they are;
- divide by the total absolute similarity so the result is a weighted average of deviations.

Centring by $\bar r_v$ matters: a harsh critic's 3 stars may mean "great", a generous user's 3 stars may mean "meh". A neighbour with **negative** similarity flips the sign of their deviation: if someone with opposite taste disliked the item, that is evidence *for* you.

**Item-based** CF predicts from the items the user already rated:
$$\hat r_{ui}=\frac{\sum_{j\in N_k(i;u)}s_{ij}\,r_{uj}}{\sum_j|s_{ij}|},$$
where $N_k(i;u)$ are the $k$ items rated by $u$ that are most similar to $i$. Why is it "more stable"? A shop may have 10M users but 100k items. Item–item similarities are averaged over many users each, change slowly, and can be precomputed nightly; user–user similarities are noisier (each user has few ratings) and shift every time a user clicks.

**Similarity measures**, for vectors of ratings $x,y$ over co-rated items:
- cosine: $\frac{x^\top y}{\lVert x\rVert\lVert y\rVert}$, the angle between the two rating vectors;
- Pearson: cosine after subtracting each user's mean (removes generosity differences);
- Jaccard, for sets of clicked items $A,B$: $\frac{|A\cap B|}{|A\cup B|}$. Used for implicit data, where there are no rating values to centre.

## Matrix factorization

![The rating matrix R with question marks being filled by dot products of rows of P and columns of Q transposed](../../Attachments/ML%20Animations/Collaborative%20Filtering%20and%20Matrix%20Factorization%20-%20filling%20the%20rating%20matrix.gif)

*Watch one row of $P$ and one column of $Q^\top$ light up: their dot product is the predicted rating that replaces a "?".*

Approximate the rating matrix $R\approx PQ^\top$, user vector $p_u$, item vector $q_i\in\mathbb R^k$:
$$\min_{P,Q}\sum_{(u,i)\in\Omega}\big(r_{ui}-\mu-b_u-b_i-p_u^\top q_i\big)^2+\lambda\big(\lVert p_u\rVert^2+\lVert q_i\rVert^2+b_u^2+b_i^2\big)$$
Only observed entries $\Omega$. (Netflix Prize "Funk SVD", Koren et al.)

## The math, step by step

**Symbols.** $P\in\mathbb R^{|U|\times k}$ stacks the user vectors $p_u$ as rows; $Q\in\mathbb R^{|I|\times k}$ stacks the item vectors $q_i$. $k$ (often 16–256) is the number of latent factors. $\mu$ is the global mean rating, $b_u$ and $b_i$ are user and item biases, $\lambda$ is the regularisation strength, $\Omega$ is the set of observed pairs.

**The prediction.** $\hat r_{ui}=\mu+b_u+b_i+p_u^\top q_i$. In words: average rating, plus "this user rates high", plus "this item is generally good", plus "how well this user's taste matches this item's profile".

**Why only $\Omega$?** The unknown cells are unknown, not zero. If you fill them with 0 and take a truncated SVD, the model spends its capacity explaining fake zeros and predicts that everyone hates everything they have not rated. Summing only over observed entries fits what we actually know.

**Why the $\lambda$ term?** A user with two ratings could get an enormous $p_u$ that fits those two numbers perfectly. The penalty keeps vectors small unless the data insists ([[Overfitting and Regularization]]).

### Optimisation
- **SGD**: $e=r-\hat r$; $p_u\leftarrow p_u+\eta(e\,q_i-\lambda p_u)$, $q_i\leftarrow q_i+\eta(e\,p_u-\lambda q_i)$ — see [[Gradient Descent]].
- **ALS**: fix $Q$ → each $p_u$ is a [[Linear Regression|ridge regression]] solved in closed form; alternate. Parallel, great for implicit data.

**Deriving the SGD update.** For one observed rating, the loss is $\ell=(r_{ui}-p_u^\top q_i)^2+\lambda(\lVert p_u\rVert^2+\lVert q_i\rVert^2)$. With $e=r_{ui}-p_u^\top q_i$:
$$\frac{\partial\ell}{\partial p_u}=-2e\,q_i+2\lambda p_u,\qquad \frac{\partial\ell}{\partial q_i}=-2e\,p_u+2\lambda q_i.$$
Step against the gradient (the factor 2 is absorbed into $\eta$) and you get the update above. Intuition: if the prediction is too low ($e>0$), nudge $p_u$ toward $q_i$ and $q_i$ toward $p_u$, so their dot product grows. Biases update the same way: $b_u\mathrel{+}=\eta(e-\lambda b_u)$, $b_i\mathrel{+}=\eta(e-\lambda b_i)$.

**Deriving the ALS step.** Fix all item vectors. For one user with rated items stacked in $Q_u$ and ratings $r_u$, the loss $\sum_i(r_{ui}-p_u^\top q_i)^2+\lambda\lVert p_u\rVert^2=\lVert r_u-Q_up_u\rVert^2+\lambda\lVert p_u\rVert^2$ is exactly ridge regression. Setting the gradient $-2Q_u^\top(r_u-Q_up_u)+2\lambda p_u$ to zero gives
$$p_u=(Q_u^\top Q_u+\lambda I)^{-1}Q_u^\top r_u.$$
Every user is independent given $Q$, so all users can be solved in parallel; then fix $P$ and do the same for items. Each half-step can only lower the loss, so ALS converges monotonically.

![A user vector rotating in a two-factor latent space until its dot products match the user's ratings](../../Attachments/ML%20Animations/Collaborative%20Filtering%20and%20Matrix%20Factorization%20-%20learning%20a%20user%20vector.gif)

*Watch $p_u$ swing from the "romance" corner toward the liked action items while the predictions on the right converge to the ratings 5, 4, 1; the unrated item $i_4$ gets a low score as a by-product.*

## Worked example

**User-based prediction.** User $u$ has mean $\bar r_u=3.0$. Neighbour $v_1$ (similarity $0.8$, mean $4$) rated item $i$ a 5, a deviation of $+1$. Neighbour $v_2$ (similarity $0.5$, mean $3$) rated it 2, a deviation of $-1$.
$$\hat r_{ui}=3.0+\frac{0.8\cdot1+0.5\cdot(-1)}{0.8+0.5}=3.0+\frac{0.3}{1.3}\approx3.23.$$

**One SGD step** (no biases). $p_u=(1.0,0.5)$, $q_i=(0.8,0.2)$, observed $r=3$, $\eta=0.1$, $\lambda=0.1$.
1. Predict: $\hat r=1.0\cdot0.8+0.5\cdot0.2=0.9$, so $e=3-0.9=2.1$.
2. $p_u\leftarrow(1.0,0.5)+0.1\,\big(2.1\,(0.8,0.2)-0.1\,(1.0,0.5)\big)=(1.158,\,0.537)$.
3. $q_i\leftarrow(0.8,0.2)+0.1\,\big(2.1\,(1.0,0.5)-0.1\,(0.8,0.2)\big)=(1.002,\,0.303)$ (using the **old** $p_u$).
4. New prediction: $1.158\cdot1.002+0.537\cdot0.303\approx1.32$. Still far from 3, but moving the right way.

**One ALS step with $k=1$.** Item factors $q_1=1$, $q_2=2$, ratings $3$ and $4$, $\lambda=1$. Then $p_u=\frac{\sum q_ir_i}{\sum q_i^2+\lambda}=\frac{1\cdot3+2\cdot4}{1+4+1}=\frac{11}{6}\approx1.83$. Predictions $1.83$ and $3.67$: shrunk toward zero by $\lambda$.

## Implicit feedback
- **Weighted MF (Hu, Koren, Volinsky 2008)**: preference $p_{ui}=\mathbb 1[r_{ui}>0]$, confidence $c_{ui}=1+\alpha r_{ui}$, sum over **all** pairs.
- **BPR (Bayesian Personalized Ranking)**: pairwise loss $-\sum\ln\sigma(\hat x_{ui}-\hat x_{uj})$ for observed $i$, unobserved $j$ — optimises ranking (AUC).
- Negative sampling for scalability.

**Why can WMF sum over all pairs?** With implicit data a missing entry is a *weak* negative, not an unknown. Each pair gets a target $p_{ui}\in\{0,1\}$ and a weight $c_{ui}$: observed items count a lot (e.g. $\alpha=40$, 3 plays → $c=121$), missing ones count 1. The objective is $\sum_{u,i}c_{ui}(p_{ui}-x_u^\top y_i)^2+\lambda(\dots)$ (here $x_u,y_i$ are the user and item factors). Summing over billions of pairs sounds impossible, but the ALS update
$$x_u=(Y^\top C_uY+\lambda I)^{-1}Y^\top C_u\,\mathbf p(u),\qquad Y^\top C_uY=Y^\top Y+Y^\top(C_u-I)Y,$$
needs $Y^\top Y$ only once for all users, and $C_u-I$ is nonzero only on the user's observed items. So the cost per user depends on $|\Omega_u|$, not on the catalogue size.

**Why does BPR optimise ranking?** BPR asks only that an observed item $i$ scores higher than an unobserved item $j$ for the same user: $\hat x_{uij}=\hat x_{ui}-\hat x_{uj}>0$. The fraction of correctly ordered (positive, negative) pairs is exactly the per-user AUC, and $\ln\sigma$ is a smooth surrogate for it. For top-K lists only the order matters, so this fits better than squared error on 0/1 targets. Gradients (with $\hat x_{ui}=p_u^\top q_i$ and $\frac{d}{dx}[-\ln\sigma(x)]=-\sigma(-x)$):
$$\nabla_{p_u}\ell=-\sigma(-\hat x_{uij})(q_i-q_j),\quad \nabla_{q_i}\ell=-\sigma(-\hat x_{uij})\,p_u,\quad \nabla_{q_j}\ell=+\sigma(-\hat x_{uij})\,p_u.$$
When the pair is already well ordered ($\hat x_{uij}\gg0$), $\sigma(-\hat x_{uij})\approx0$ and nothing changes; wrongly ordered pairs get large updates. **Negative sampling** picks one random unobserved $j$ per step instead of looping over all of them.

## Extensions
SVD++ (implicit signals), timeSVD++ (temporal), factorization machines (side features, $\sum_{i<j}\langle v_i,v_j\rangle x_ix_j$), non-negative MF, probabilistic MF ([[Bayesian Inference]]).

**The factorization-machine trick.** A naive sum over all feature pairs costs $O(kn^2)$. Expanding a square gives
$$\sum_{i<j}\langle v_i,v_j\rangle x_ix_j=\frac12\sum_{f=1}^k\Big[\Big(\sum_iv_{if}x_i\Big)^2-\sum_iv_{if}^2x_i^2\Big],$$
which costs $O(kn)$ (and only the nonzero $x_i$ matter). If $x$ is one-hot(user) concatenated with one-hot(item), only one pair survives and the FM reduces to $\langle v_u,v_i\rangle=p_u^\top q_i$: plain MF. Adding more features (age, genre, time) generalises MF to side information.

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

Note the tuple assignment in the loop: both updates use the **old** `P[u]` and `Q[i]`, exactly as in the worked example.

**SGD or ALS?** SGD: cheap per step, easy to extend with any loss (BPR, biases), but needs a learning rate and is sequential. ALS: no learning rate, embarrassingly parallel, and the natural choice for implicit WMF because the all-pairs trick above only works with closed-form solves.

## Common confusions

- **"Missing ratings are zeros."** → For explicit ratings they are *unknown*; fill them with zeros and the model learns that everybody hates unseen items. Only implicit WMF treats them as low-confidence negatives, on purpose.
- **"The latent factors mean 'action' and 'romance'."** → Sometimes they roughly do, but they are only defined up to rotation. Any $PR$ and $QR$ with an orthogonal $R$ give the same predictions.
- **"Negative similarity is useless."** → In the user-based formula a negatively similar neighbour's deviation is flipped, so their dislike raises your prediction.
- **"ALS is a different model from SGD-MF."** → Same objective, different optimiser.
- **"BPR predicts ratings."** → BPR scores are only meaningful relative to each other for the same user; it optimises order (AUC), not calibrated values.

## Check yourself

> [!question]- Why is item-based CF usually preferred to user-based CF in large shops?
> There are far fewer items than users, and each item has many ratings, so item–item similarities are more reliable, change slowly, and can be precomputed. User vectors change with every click.

> [!question]- What happens in one SGD step if the prediction is too high?
> The error $e=r-\hat r$ is negative, so $p_u$ moves away from $q_i$ and $q_i$ moves away from $p_u$, shrinking their dot product (plus a small shrink toward zero from $\lambda$).

> [!question]- Why is each ALS half-step a ridge regression?
> With $Q$ fixed, the loss for one user is $\lVert r_u-Q_up_u\rVert^2+\lambda\lVert p_u\rVert^2$: a linear least-squares problem in $p_u$ with an L2 penalty, solved by $p_u=(Q_u^\top Q_u+\lambda I)^{-1}Q_u^\top r_u$.

> [!question]- In WMF, why does a zero entry have confidence 1 rather than 0?
> Because the model wants it to act as a weak negative. With confidence 0 the missing entries would be ignored and nothing would stop the model from predicting "like" for every item.

> [!question]- With one-hot user and item features, what does a factorization machine reduce to?
> Only the user–item pair is active, so the interaction term is $\langle v_u,v_i\rangle$: ordinary matrix factorization.

## Practice

[Collaborative Filtering and Matrix Factorization - Exercises](Collaborative%20Filtering%20and%20Matrix%20Factorization%20-%20Exercises.ipynb): cosine, Pearson and Jaccard by hand, a user-based prediction, one SGD step, an ALS half-step, the BPR gradient and the FM identity; then item–item kNN, biased MF with SGD, ALS, an implicit-ALS user update and BPR-MF from scratch.

## Learn more

- Koren, Bell & Volinsky, *Matrix Factorization Techniques for Recommender Systems* (IEEE Computer, 2009): the Netflix Prize write-up.
- Hu, Koren & Volinsky, *Collaborative Filtering for Implicit Feedback Datasets* (ICDM 2008): weighted MF.
- Rendle et al., [BPR: Bayesian Personalized Ranking from Implicit Feedback](https://arxiv.org/abs/1205.2618) (UAI 2009).
- [Google ML course: Matrix factorization](https://developers.google.com/machine-learning/recommendation/collaborative/matrix).
- [[Recommender Systems Overview]] · [[Recommender Systems Resources]]
