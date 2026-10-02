---
tags: [ml, masters, projects]
---
# Implement From Scratch

> [!summary] In one sentence
> Re-implementing each core algorithm in plain NumPy and checking it number-for-number against a trusted library is the fastest way to turn "I have read about it" into "I understand every line of it".

Implementing an algorithm yourself is the fastest way to understand it. Use NumPy (or PyTorch tensors without `nn` modules), then compare with the library version.

## Intuition first

Reading a derivation feels like understanding; writing the code exposes every gap. You discover that "compute the gradient" hides a transpose, that "assign to the nearest centroid" needs a broadcasted distance matrix, that the softmax overflows unless you subtract the maximum, and that sklearn silently adds L2 regularisation. It is like learning to cook: watching a recipe video is not the same as getting the sauce to thicken yourself.

The trick that makes this efficient is having a **referee**. A library implementation (sklearn, PyTorch, SciPy) gives you the right answer on the same data, so you get instant, objective feedback: either `np.allclose(mine, lib)` is `True`, or you have found exactly the thing you did not understand yet.

![The from-scratch loop: read the math, write NumPy, run the library on the same data, compare; if they differ, fix and repeat](../../Attachments/ML%20Animations/Implement%20From%20Scratch%20-%20test%20loop.gif)

*Watch the comparison turn red first (a shape bug, a default hyperparameter or a sign flip), send you back to the code, and only then turn green.*

## The list

| # | Implement | Check against | Note |
|---|---|---|---|
| 1 | Linear regression (closed form + GD) | `sklearn.linear_model.LinearRegression` | [[Linear Regression]] |
| 2 | Logistic regression with softmax | `LogisticRegression` | [[Logistic Regression]] |
| 3 | k-NN + k-means | `KNeighborsClassifier`, `KMeans` | [[k-Nearest Neighbors]], [[Clustering]] |
| 4 | Decision tree (Gini) | `DecisionTreeClassifier` | [[Decision Trees]] |
| 5 | PCA via SVD | `PCA` | [[PCA]] |
| 6 | GMM with EM | `GaussianMixture` | [[Gaussian Mixture Models and EM]] |
| 7 | Naive Bayes | `MultinomialNB` | [[Naive Bayes]] |
| 8 | Autograd engine (micrograd) | [Karpathy's video](https://karpathy.ai/zero-to-hero.html) | [[Backpropagation]] |
| 9 | MLP on MNIST in NumPy | PyTorch version | [[Neural Networks]] |
| 10 | Adam optimiser | `torch.optim.Adam` | [[Optimizers]] |
| 11 | Conv layer forward/backward | `nn.Conv2d` | [[CNN]] |
| 12 | Self-attention + a tiny GPT | [nanoGPT / "Let's build GPT"](https://karpathy.ai/zero-to-hero.html) | [[Transformers]] |
| 13 | Matrix factorization + BPR | `implicit` library | [[Collaborative Filtering and Matrix Factorization]] |
| 14 | GCN layer | PyTorch Geometric `GCNConv` | [[Graph Neural Networks]] |
| 15 | VAE on MNIST | — | [[Generative Models]] |
| 16 | Q-learning on FrozenLake, then DQN on CartPole | Stable-Baselines3 | [[Q-Learning and Policy Gradients]] |
| 17 | Metropolis–Hastings sampler | PyMC | [[MCMC]] |
| 18 | VBPR (MF + image features) | [MMRec](https://github.com/enoche/MMRec) | [[Multimodal Recommender Systems]] |

Snippets to start from: [[NumPy Snippets]], [[PyTorch Recipes]].

**Suggested order**: rows 1–7 build NumPy fluency (vectorisation, broadcasting, log-space); rows 8–12 are the deep-learning core (backprop is the common thread); rows 13–18 connect to recommender systems, graphs, generative models, RL and sampling.

## How do you know your implementation is right?

Four independent tests, from cheapest to strongest:

1. **Library reference** on the same data and hyperparameters (sklearn, SciPy, PyTorch). Best for closed-form estimators (rows 1, 5, 7).
2. **Numerical gradient check** against your analytic gradient. Essential for any hand-written backward pass (rows 8–12, 14, 15).
3. **Known exact answers** on tiny inputs you can solve by hand: a 2-point regression, a 3×3 convolution, a 3-node graph.
4. **Invariants and convergence**: the loss decreases monotonically (GD on a convex loss, k-means inertia, the EM log-likelihood, ALS); probabilities sum to 1; for stochastic algorithms (Q-learning, MCMC) compare against an exact solution (value iteration, analytic moments) rather than demanding identical numbers.

## The math, step by step: gradient checking

For a scalar loss $f(\theta)$, the **central difference**

$$g_{\text{num}}=\frac{f(\theta+h)-f(\theta-h)}{2h}$$

approximates $f'(\theta)$ with error $O(h^2)$ (the one-sided $\frac{f(\theta+h)-f(\theta)}{h}$ has error $O(h)$, so prefer the central one). Compare with your analytic gradient $g$ using the **relative error**

$$\text{rel}=\frac{|g-g_{\text{num}}|}{\max(|g|,|g_{\text{num}}|)}.$$

In words: tilt a secant line through two nearby points; as $h$ shrinks it becomes the tangent, whose slope your backward pass claims to compute. With float64 and $h\approx10^{-5}$, a correct gradient gives relative error around $10^{-6}$ or smaller; $10^{-2}$ means a bug. Too small an $h$ makes floating-point cancellation dominate, so do not go below about $10^{-7}$. For a vector $\theta$, perturb one coordinate at a time.

![A secant through f(theta - h) and f(theta + h) converges to the tangent of the analytic gradient as h shrinks](../../Attachments/ML%20Animations/Implement%20From%20Scratch%20-%20gradient%20check.gif)

*Watch the yellow secant rotate onto the green tangent as $h$ shrinks, and the relative error fall from $10^{-1}$ to about $10^{-5}$.*

## Worked example

**Gradient check by hand.** $f(\theta)=\theta^3$ at $\theta=2$, analytic $f'(2)=3\cdot2^2=12$. With $h=0.01$:
$f(2.01)=8.120601$, $f(1.99)=7.880599$, so $g_{\text{num}}=\frac{0.240002}{0.02}=12.0001$.
Relative error $\frac{0.0001}{12.0001}\approx8.3\cdot10^{-6}$, matching the predicted error $h^2f'''/6=10^{-4}$. Pass.

**Gini by hand (row 4).** A node with 5 A and 5 B has $G=1-\sum_kp_k^2=1-0.25-0.25=0.5$. Split into (4 A, 1 B) and (1 A, 4 B): each child has $1-0.64-0.04=0.32$, weighted $0.5\cdot0.32+0.5\cdot0.32=0.32$, so the impurity decrease is $0.18$. The tree tries every candidate threshold (midpoints between consecutive distinct sorted values) and keeps the largest decrease.

## Key equations per row

- **Linear regression**: add a bias column $X_b=[\mathbf 1,X]$; closed form solves $X_b^\top X_bw=X_b^\top y$ (use `np.linalg.solve`, never `inv`); GD uses $\nabla=\frac2NX_b^\top(X_bw-y)$.
- **Softmax regression**: $p_i=\mathrm{softmax}(W^\top[1,x_i])$, gradient $\frac1NX_b^\top(P-Y)$ with one-hot $Y$ (same form as linear regression). Subtract the row max before `exp`.
- **k-NN / k-means**: pairwise squared distances via broadcasting `((A[:, None] - B[None]) ** 2).sum(-1)`. k-means alternates *assign* and *update*; each step lowers the inertia $\sum_i\lVert x_i-\mu_{c_i}\rVert^2$, so it converges, but only to a local optimum.
- **PCA via SVD**: centre, $X_c=U\Sigma V^\top$, components are the rows of $V^\top$, variances $\sigma_j^2/(N-1)$, scores $Z=X_cV_k$. SVD avoids forming $X_c^\top X_c$, which squares the condition number.
- **GMM with EM**: E-step responsibilities $\gamma_{ik}\propto\pi_k\mathcal N(x_i\mid\mu_k,\sigma_k^2)$ (normalise with log-sum-exp); M-step weighted means, variances, weights. The log-likelihood must never decrease.
- **Multinomial NB**: $\theta_{kj}=\frac{N_{kj}+\alpha}{N_k+\alpha d}$ (Laplace smoothing), predictions in log-space.
- **Autograd**: each op stores its parents and a local backward closure; `backward()` topologically sorts and applies the chain rule in reverse, **accumulating** with `+=` because a value can feed several nodes.
- **MLP backprop**: `dZ2 = (P - Y)/B`, `dW2 = H.T @ dZ2`, `dH = dZ2 @ W2.T`, `dZ1 = dH * (Z1 > 0)`, `dW1 = X.T @ dZ1`.
- **Adam**: $m\leftarrow\beta_1m+(1-\beta_1)g$, $v\leftarrow\beta_2v+(1-\beta_2)g^2$, bias-correct $\hat m=m/(1-\beta_1^t)$, $\hat v=v/(1-\beta_2^t)$, step $w\leftarrow w-\text{lr}\,\hat m/(\sqrt{\hat v}+\epsilon)$. The first step is $\approx-\text{lr}\cdot\mathrm{sign}(g)$ whatever $|g|$.
- **Conv layer**: forward is a cross-correlation $O_{ij}=\sum_{a,b}X_{i+a,j+b}K_{ab}$; backward $dK=X\star dO$ (valid correlation) and $dX$ is the full convolution of $dO$ with $K$. The backward pass of a conv is itself a conv.
- **Self-attention**: $A=\mathrm{softmax}\big(\frac{QK^\top}{\sqrt{d_k}}+M\big)$, output $AV$, with causal mask $M_{ts}=-\infty$ for $s>t$. Dividing by $\sqrt{d_k}$ keeps logits at unit variance.
- **Matrix factorisation**: $R\approx PQ^\top$; ALS solves a ridge problem per user $p_u=(Q_u^\top Q_u+\lambda I)^{-1}Q_u^\top r_u$, then per item. **BPR** maximises $\ln\sigma(\hat r_{ui}-\hat r_{uj})$ for a consumed item $i$ over a non-consumed $j$.
- **GCN**: $H'=\hat AHW$ with $\hat A=\tilde D^{-1/2}\tilde A\tilde D^{-1/2}$, $\tilde A=A+I$.
- **VAE**: $\mathrm{KL}\big(\mathcal N(\mu,\sigma^2)\,\|\,\mathcal N(0,1)\big)=\frac12(\mu^2+\sigma^2-1-\ln\sigma^2)$; sample $z=\mu+\sigma\epsilon$ (reparameterisation) so gradients flow through $\mu,\sigma$.
- **Q-learning**: $Q(s,a)\leftarrow Q(s,a)+\alpha\big(r+\gamma\max_{a'}Q(s',a')(1-\text{done})-Q(s,a)\big)$; off-policy because of the $\max$.
- **Metropolis–Hastings** (random walk): accept $x'$ with probability $\min\big(1,\tilde p(x')/\tilde p(x)\big)$; on rejection **repeat** the old $x$. The normalising constant cancels.

## Why does my result differ from the library?

Most mismatches are not bugs in your maths but differences in **defaults**:

- **Logistic regression** weights larger than sklearn's: `LogisticRegression` applies L2 regularisation by default (`C=1.0`). Dividing its objective by $CN$ shows it equals your mean loss plus $\frac{\lambda}{2}\lVert W\rVert^2$ with $\lambda=\frac1{CN}$ (bias unpenalised).
- **PCA** components multiplied by $-1$: singular vectors are defined only up to sign; compare absolute values.
- **k-means** centres differ: local optima depend on initialisation (`n_init`, `random_state`); pass the same initial centres.
- **Decision tree** splits differ: ties in impurity decrease are broken differently.
- **GMM** variances differ slightly: sklearn adds `reg_covar` to the diagonal.
- **Softmax weights** differ but probabilities agree: softmax is over-parameterised (adding a constant to all columns changes nothing), so compare probabilities.

## Common confusions

- *"If the loss goes down, my gradient is right."* → A wrong gradient can still point roughly downhill. Run a numerical gradient check.
- *"Close to sklearn is good enough."* → Aim for `np.allclose` on a deterministic algorithm. A 2% difference is usually a default you have not matched (regularisation, smoothing, convergence tolerance).
- *"Use `np.linalg.inv` for the normal equations."* → `solve` (or `lstsq`) is faster and numerically more stable.
- *"Exact equality is the test for stochastic algorithms."* → For Q-learning, MCMC or SGD, test against the known solution or analytic moments, with a tolerance.
- *"Loops are fine, I'll vectorise later."* → Vectorising is part of the understanding (broadcasting, shapes); write `assert` on shapes as you go ([[NumPy Snippets]]).

## Check yourself

> [!question]- Why is the central difference preferred over the one-sided difference for gradient checks?
> Its error is $O(h^2)$ instead of $O(h)$, because the second-order Taylor terms cancel. You get a more accurate check for the same $h$.

> [!question]- Your PCA components equal sklearn's times $-1$. Bug?
> No. Singular vectors are only defined up to sign (sklearn flips them deterministically). Compare absolute values or align signs.

> [!question]- In a micrograd-style engine, why must `_backward` use `+=` rather than `=`?
> A value can be used by several downstream nodes; its gradient is the sum of the contributions from each path (multivariate chain rule). `=` would overwrite all but the last.

> [!question]- What does Adam's first step look like starting from $m=v=0$?
> After bias correction $\hat m_1=g$, $\hat v_1=g^2$, so $\Delta w=-\text{lr}\,g/(|g|+\epsilon)\approx-\text{lr}\cdot\mathrm{sign}(g)$: scale-invariant per coordinate.

> [!question]- Which test would you use for a Metropolis–Hastings sampler?
> Compare sample moments with the analytic ones (e.g. mixture mean $\sum_k\pi_k\mu_k$) with a tolerance, and check the acceptance rate; identical numbers to PyMC are not expected.

## Practice

[Implement From Scratch - Exercises](Implement%20From%20Scratch%20-%20Exercises.ipynb): testing strategies and library mismatches, then rows 1–17 as coding challenges (linear and softmax regression, k-NN and k-means, a Gini tree, PCA, EM, Naive Bayes, a micrograd engine, an MLP, Adam, conv backward, causal self-attention, GCN normalisation, ALS, the VAE KL term, Q-learning and Metropolis–Hastings).

## Learn more
- [Andrej Karpathy — Neural Networks: Zero to Hero (micrograd, makemore, nanoGPT)](https://karpathy.ai/zero-to-hero.html)
- [MMRec — multimodal recommendation toolbox](https://github.com/enoche/MMRec)
- [CS231n notes — gradient checks and sanity checks](https://cs231n.github.io/neural-networks-3/)
