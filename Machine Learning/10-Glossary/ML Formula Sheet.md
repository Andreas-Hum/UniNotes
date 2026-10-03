---
tags: [ml, formula-sheet, formelsamling, cheatsheet]
aliases: [Formelsamling, Formula Sheet]
---
# ML Formula Sheet (Formelsamling)

> [!tip] How to use
> One page of the key formulas, grouped by topic, each linked to the note that explains it. Notation: $x\in\mathbb R^d$ input, $y$ target, $N$ samples, $X\in\mathbb R^{N\times d}$ (rows = samples), $w$ weights, $\hat y$ prediction, $\sigma$ sigmoid.

## 1. Linear algebra → [[Linear Algebra for ML]]
| | |
|---|---|
| Dot product | $a^\top b=\sum_ia_ib_i=\lVert a\rVert\lVert b\rVert\cos\theta$ |
| Norms | $\lVert x\rVert_1=\sum|x_i|$, $\lVert x\rVert_2=\sqrt{\sum x_i^2}$, $\lVert x\rVert_\infty=\max|x_i|$ |
| Transpose / inverse of product | $(AB)^\top=B^\top A^\top$, $(AB)^{-1}=B^{-1}A^{-1}$ |
| Eigen | $Av=\lambda v$; symmetric $A=Q\Lambda Q^\top$ |
| SVD | $X=U\Sigma V^\top$; best rank-$k$: keep top $k$ singular values |
| Trace / det | $\mathrm{tr}(AB)=\mathrm{tr}(BA)$, $\mathrm{tr}A=\sum\lambda_i$, $\det A=\prod\lambda_i$ |
| PSD | $x^\top Ax\ge0\ \forall x$ (covariance, kernel matrices) |
| Projection onto col($X$) | $P=X(X^\top X)^{-1}X^\top$ |

## 2. Calculus and gradients → [[Matrix Calculus Cheatsheet]], [[Calculus and Optimization]]
| $f$ | $\nabla_xf$ |
|---|---|
| $a^\top x$ | $a$ |
| $x^\top Ax$ | $(A+A^\top)x$ |
| $\lVert Ax-b\rVert^2$ | $2A^\top(Ax-b)$ |
| $\sigma(z)=\frac1{1+e^{-z}}$ | $\sigma'(z)=\sigma(z)(1-\sigma(z))$ |
| $\tanh z$ | $1-\tanh^2z$ |
| softmax + cross-entropy | $\partial L/\partial z=\hat p-y$ |
- Chain rule: $\dfrac{\partial L}{\partial x}=\dfrac{\partial L}{\partial y}\dfrac{\partial y}{\partial x}$; vector form $\nabla_xz=J_h(x)^\top\nabla_yz$.
- Convex iff Hessian $H\succeq0$. Lagrangian $\mathcal L=f(x)+\sum_i\lambda_ig_i(x)$; KKT: stationarity, feasibility, $\lambda_i\ge0$, $\lambda_ig_i(x)=0$.

## 3. Probability → [[Probability for ML]]
| | |
|---|---|
| Sum / product rule | $p(x)=\sum_yp(x,y)$, $p(x,y)=p(y\mid x)p(x)$ |
| **Bayes** | $p(\theta\mid D)=\dfrac{p(D\mid\theta)p(\theta)}{p(D)}$ |
| Expectation / variance | $\mathbb E[X]=\sum xp(x)$, $\mathrm{Var}X=\mathbb E[X^2]-\mathbb E[X]^2$ |
| Covariance | $\mathrm{Cov}(X,Y)=\mathbb E[XY]-\mathbb E[X]\mathbb E[Y]$; $\mathrm{Var}(aX+b)=a^2\mathrm{Var}X$ |
| Bernoulli | $p(x)=\pi^x(1-\pi)^{1-x}$, mean $\pi$, var $\pi(1-\pi)$ |
| Binomial | $\binom nk\pi^k(1-\pi)^{n-k}$ |
| Poisson | $\frac{\lambda^ke^{-\lambda}}{k!}$, mean = var = $\lambda$ |
| Gaussian | $\mathcal N(x\mid\mu,\sigma^2)=\frac1{\sqrt{2\pi\sigma^2}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}$ |
| Multivariate Gaussian | $\frac1{(2\pi)^{d/2}|\Sigma|^{1/2}}\exp\!\big(-\tfrac12(x-\mu)^\top\Sigma^{-1}(x-\mu)\big)$ |
| Beta / Dirichlet | conjugate priors for Bernoulli / categorical |
- **MLE:** $\hat\theta=\arg\max_\theta\sum_i\log p(x_i\mid\theta)$. Gaussian → $\hat\mu=\bar x$, $\hat\sigma^2=\frac1N\sum(x_i-\bar x)^2$.
- **MAP:** $\arg\max_\theta[\log p(D\mid\theta)+\log p(\theta)]$. Gaussian prior ↔ L2, Laplace prior ↔ L1.

## 4. Information theory → [[Information Theory]]
| | |
|---|---|
| Entropy | $H(p)=-\sum p\log p$ |
| Cross-entropy | $H(p,q)=-\sum p\log q=H(p)+D_{KL}(p\Vert q)$ |
| KL divergence | $D_{KL}(p\Vert q)=\sum p\log\frac pq\ge0$ |
| Mutual information | $I(X;Y)=H(X)-H(X\mid Y)$ |
| Information gain | $H(\text{parent})-\sum_k\frac{N_k}NH(\text{child}_k)$ |
| Gini impurity | $1-\sum_kp_k^2$ |

## 5. Linear and logistic regression → [[Linear Regression]], [[Logistic Regression]]
| | |
|---|---|
| Model | $\hat y=w^\top x+b$ |
| MSE | $\frac1N\sum(y_i-\hat y_i)^2$ |
| **Normal equations** | $w=(X^\top X)^{-1}X^\top y$ |
| **Ridge** | $w=(X^\top X+\lambda I)^{-1}X^\top y$ |
| Lasso | $\min\lVert y-Xw\rVert^2+\lambda\lVert w\rVert_1$ (no closed form) |
| $R^2$ | $1-\frac{SS_{res}}{SS_{tot}}$ |
| Logistic | $p(y=1\mid x)=\sigma(w^\top x+b)$ |
| Binary cross-entropy | $-\frac1N\sum[y\log\hat p+(1-y)\log(1-\hat p)]$ |
| Gradient (logistic) | $\nabla_w=X^\top(\hat p-y)$ |
| Softmax | $p_k=\frac{e^{z_k}}{\sum_je^{z_j}}$ |
| Log-odds | $\log\frac{p}{1-p}=w^\top x+b$ |
| LDA discriminant | $\delta_k(x)=x^\top\Sigma^{-1}\mu_k-\tfrac12\mu_k^\top\Sigma^{-1}\mu_k+\log\pi_k$ |
| Perceptron update | if $y_iw^\top x_i\le0$: $w\leftarrow w+\eta y_ix_i$ |

## 6. Evaluation → [[Model Evaluation and Metrics]], [[Bias-Variance Tradeoff]]
| | |
|---|---|
| Accuracy | $\frac{TP+TN}{TP+TN+FP+FN}$ |
| Precision / Recall | $\frac{TP}{TP+FP}$ / $\frac{TP}{TP+FN}$ |
| F1 / $F_\beta$ | $\frac{2PR}{P+R}$ / $\frac{(1+\beta^2)PR}{\beta^2P+R}$ |
| Specificity / FPR | $\frac{TN}{TN+FP}$ / $\frac{FP}{FP+TN}$ |
| MCC | $\frac{TP\cdot TN-FP\cdot FN}{\sqrt{(TP+FP)(TP+FN)(TN+FP)(TN+FN)}}$ |
| ROC-AUC | $P(\text{score of random positive}>\text{score of random negative})$ |
| MAE / RMSE | $\frac1N\sum|e|$ / $\sqrt{\frac1N\sum e^2}$ |
| **Bias–variance** | $\mathbb E[(y-\hat f)^2]=\text{Bias}^2+\text{Var}+\sigma^2$ |
| AIC / BIC | $2k-2\ln\hat L$ / $k\ln N-2\ln\hat L$ |

## 7. Kernels, SVM, kNN, Naive Bayes, trees, ensembles → [[Support Vector Machines]], [[Kernel Methods]], [[Ensemble Methods]]
| | |
|---|---|
| Margin | $2/\lVert w\rVert$ |
| Hard-margin SVM | $\min\frac12\lVert w\rVert^2$ s.t. $y_i(w^\top x_i+b)\ge1$ |
| Soft-margin SVM | $\min\frac12\lVert w\rVert^2+C\sum\xi_i$ s.t. $y_i(w^\top x_i+b)\ge1-\xi_i$ |
| Hinge loss | $\max(0,1-yf(x))$ |
| SVM dual | $\max_\alpha\sum\alpha_i-\frac12\sum_{ij}\alpha_i\alpha_jy_iy_jk(x_i,x_j)$, $0\le\alpha_i\le C$, $\sum\alpha_iy_i=0$ |
| Prediction (dual) | $f(x)=\sum_i\alpha_iy_ik(x_i,x)+b$ |
| Kernels | linear $x^\top x'$; poly $(x^\top x'+c)^p$; RBF $\exp(-\gamma\lVert x-x'\rVert^2)$ |
| Naive Bayes | $p(y\mid x)\propto p(y)\prod_jp(x_j\mid y)$; Laplace: $\frac{n_{jk}+\alpha}{n_k+\alpha V}$ |
| kNN | majority vote / mean of $k$ nearest; Euclidean $\sqrt{\sum(x_i-x'_i)^2}$ |
| AdaBoost | $\epsilon_t=\sum w_i\mathbb 1[h_t(x_i)\ne y_i]$, $\alpha_t=\frac12\ln\frac{1-\epsilon_t}{\epsilon_t}$, $w_i\leftarrow w_ie^{-\alpha_ty_ih_t(x_i)}$ (normalise) |
| Gradient boosting | $F_m=F_{m-1}+\nu h_m$, $h_m$ fit to $-\partial L/\partial F_{m-1}$ (residuals for MSE) |
| Bagging variance | $\rho\sigma^2+\frac{1-\rho}{B}\sigma^2$ ($B$ models, correlation $\rho$) |

## 8. Unsupervised → [[Clustering]], [[PCA]], [[Gaussian Mixture Models and EM]]
| | |
|---|---|
| k-means objective | $J=\sum_i\lVert x_i-\mu_{c(i)}\rVert^2$ |
| PCA | maximise $w^\top Sw$ s.t. $\lVert w\rVert=1$ → eigenvectors of $S=\frac1NX_c^\top X_c$; explained variance $\lambda_k/\sum\lambda_i$ |
| GMM | $p(x)=\sum_k\pi_k\mathcal N(x\mid\mu_k,\Sigma_k)$ |
| E-step | $\gamma_{ik}=\frac{\pi_k\mathcal N(x_i\mid\mu_k,\Sigma_k)}{\sum_j\pi_j\mathcal N(x_i\mid\mu_j,\Sigma_j)}$ |
| M-step | $N_k=\sum_i\gamma_{ik}$, $\mu_k=\frac1{N_k}\sum\gamma_{ik}x_i$, $\Sigma_k=\frac1{N_k}\sum\gamma_{ik}(x_i-\mu_k)(x_i-\mu_k)^\top$, $\pi_k=N_k/N$ |
| Silhouette | $s=\frac{b-a}{\max(a,b)}$ |

## 9. Probabilistic ML → [[Bayesian Inference]], [[Variational Inference]], [[MCMC]], [[Gaussian Processes]]
| | |
|---|---|
| Predictive distribution | $p(y_*\mid x_*,D)=\int p(y_*\mid x_*,\theta)p(\theta\mid D)\,d\theta$ |
| Bayesian linear regression | prior $w\sim\mathcal N(0,\alpha^{-1}I)$ → $S_N^{-1}=\alpha I+\beta X^\top X$, $m_N=\beta S_NX^\top y$ |
| **ELBO** | $\log p(x)\ge\mathbb E_q[\log p(x\mid z)]-D_{KL}(q(z)\Vert p(z))$ |
| Metropolis–Hastings | accept with $\min\!\Big(1,\frac{\tilde p(\theta')q(\theta\mid\theta')}{\tilde p(\theta)q(\theta'\mid\theta)}\Big)$ |
| GP posterior | $\mu_*=k_*^\top(K+\sigma^2I)^{-1}y$, $\Sigma_*=k_{**}-k_*^\top(K+\sigma^2I)^{-1}k_*$ |
| Bayesian network | $p(x_1,\dots,x_n)=\prod_ip(x_i\mid\mathrm{pa}(x_i))$ |

## 10. Neural networks → [[Neural Networks]], [[Backpropagation]], [[Optimizers]], [[Activation Functions]]
| | |
|---|---|
| Layer | $h^{(l)}=\phi(W^{(l)}h^{(l-1)}+b^{(l)})$ |
| Backprop | $\delta^{(l)}=(W^{(l+1)\top}\delta^{(l+1)})\odot\phi'(z^{(l)})$; $\frac{\partial L}{\partial W^{(l)}}=\delta^{(l)}h^{(l-1)\top}$ |
| ReLU / GELU | $\max(0,z)$ / $z\Phi(z)$ |
| Xavier / He init | $\mathrm{Var}(w)=\frac2{n_{in}+n_{out}}$ / $\frac2{n_{in}}$ |
| SGD | $\theta\leftarrow\theta-\eta\nabla L$ |
| Momentum | $v\leftarrow\beta v+\nabla L$, $\theta\leftarrow\theta-\eta v$ |
| **Adam** | $m\leftarrow\beta_1m+(1-\beta_1)g$, $v\leftarrow\beta_2v+(1-\beta_2)g^2$, $\hat m=\frac{m}{1-\beta_1^t}$, $\hat v=\frac{v}{1-\beta_2^t}$, $\theta\leftarrow\theta-\eta\frac{\hat m}{\sqrt{\hat v}+\epsilon}$ |
| AdamW | Adam + decoupled decay $\theta\leftarrow\theta-\eta\lambda\theta$ |
| BatchNorm | $\hat x=\frac{x-\mu_B}{\sqrt{\sigma_B^2+\epsilon}}$, $y=\gamma\hat x+\beta$ |
| Dropout (inverted) | keep with prob. $p$, scale by $1/p$ during training |
| Initial loss check | $\approx\ln K$ for $K$ balanced classes |

## 11. CNNs and vision → [[CNN]], [[CNN Architectures]], [[Object Detection]], [[Image Segmentation]]
| | |
|---|---|
| Conv output size | $\lfloor\frac{W-F+2P}{S}\rfloor+1$ |
| Conv parameters | $(F^2C_{in}+1)C_{out}$ |
| Transposed conv output | $(W-1)S-2P+F$ |
| Residual block | $y=x+F(x)$ |
| Depthwise separable cost ratio | $\frac1{C_{out}}+\frac1{F^2}$ |
| ViT tokens | $HW/P^2$ |
| IoU / Dice | $\frac{|A\cap B|}{|A\cup B|}$ / $\frac{2|A\cap B|}{|A|+|B|}=\frac{2\,\mathrm{IoU}}{1+\mathrm{IoU}}$ |
| Focal loss | $-\alpha_t(1-p_t)^\gamma\log p_t$ |

## 12. Sequences, attention, Transformers → [[Attention Mechanism]], [[Transformers]], [[RNN and LSTM]]
| | |
|---|---|
| RNN | $h_t=\tanh(W_hh_{t-1}+W_xx_t+b)$ |
| LSTM | $f,i,o=\sigma(\cdot)$, $\tilde c=\tanh(\cdot)$, $c_t=f\odot c_{t-1}+i\odot\tilde c$, $h_t=o\odot\tanh c_t$ |
| Q, K, V | $Q=XW_Q$, $K=XW_K$, $V=XW_V$ |
| **Attention** | $\mathrm{softmax}\!\big(\frac{QK^\top}{\sqrt{d_k}}+M\big)V$ |
| Multi-head | $\mathrm{Concat}(\mathrm{head}_1..\mathrm{head}_h)W_O$, $d_k=d/h$ |
| Sinusoidal PE | $PE_{(p,2i)}=\sin(p/10000^{2i/d})$, $PE_{(p,2i+1)}=\cos(p/10000^{2i/d})$ |
| Attention cost | $O(n^2d)$ time, $O(n^2)$ memory |
| Perplexity | $\exp\!\big(-\frac1T\sum_t\log p(x_t\mid x_{<t})\big)$ |
| LoRA | $W=W_0+BA$, $B\in\mathbb R^{d\times r}$, $A\in\mathbb R^{r\times k}$, $r\ll d$ |

## 13. Generative and self-supervised → [[Generative Models]], [[Self-Supervised and Contrastive Learning]]
| | |
|---|---|
| VAE loss | $-\mathbb E_q[\log p(x\mid z)]+D_{KL}(q(z\mid x)\Vert\mathcal N(0,I))$; reparam. $z=\mu+\sigma\odot\epsilon$ |
| GAN | $\min_G\max_D\ \mathbb E[\log D(x)]+\mathbb E[\log(1-D(G(z)))]$ |
| Diffusion forward | $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$; loss $\lVert\epsilon-\epsilon_\theta(x_t,t)\rVert^2$ |
| InfoNCE | $-\log\frac{\exp(\mathrm{sim}(z_i,z_j)/\tau)}{\sum_{k\ne i}\exp(\mathrm{sim}(z_i,z_k)/\tau)}$ |
| Distillation | $(1-\alpha)\mathrm{CE}(y,p_s)+\alpha T^2\mathrm{KL}(p_t^{(T)}\Vert p_s^{(T)})$ |

## 14. Reinforcement learning → [[RL Basics and MDPs]], [[Q-Learning and Policy Gradients]]
| | |
|---|---|
| Return | $G_t=\sum_{k\ge0}\gamma^kr_{t+k+1}$ |
| Bellman expectation | $V^\pi(s)=\sum_a\pi(a\mid s)\sum_{s'}P(s'\mid s,a)[R+\gamma V^\pi(s')]$ |
| Bellman optimality | $Q^*(s,a)=\sum_{s'}P(s'\mid s,a)[R+\gamma\max_{a'}Q^*(s',a')]$ |
| TD(0) | $V(s)\leftarrow V(s)+\alpha[r+\gamma V(s')-V(s)]$ |
| SARSA | $Q(s,a)\leftarrow Q+\alpha[r+\gamma Q(s',a')-Q]$ |
| Q-learning | $Q(s,a)\leftarrow Q+\alpha[r+\gamma\max_{a'}Q(s',a')-Q]$ |
| REINFORCE | $\nabla J=\mathbb E[\nabla\log\pi_\theta(a\mid s)(G_t-b)]$ |
| PPO clip | $\mathbb E[\min(r_tA_t,\mathrm{clip}(r_t,1-\epsilon,1+\epsilon)A_t)]$, $r_t=\frac{\pi_\theta}{\pi_{old}}$ |

## 15. Graphs → [[Graph ML Overview]], [[Link Prediction]], [[Graph Neural Networks]]
| | |
|---|---|
| Laplacian | $L=D-A$; normalised $I-D^{-1/2}AD^{-1/2}$ |
| Jaccard / Adamic–Adar | $\frac{|N(u)\cap N(v)|}{|N(u)\cup N(v)|}$ / $\sum_{w\in N(u)\cap N(v)}\frac1{\log d_w}$ |
| GCN layer | $H'=\sigma(\tilde D^{-1/2}\tilde A\tilde D^{-1/2}HW)$, $\tilde A=A+I$ |
| Message passing | $h_v'=\mathrm{UPD}(h_v,\mathrm{AGG}\{h_u:u\in N(v)\})$ |

## 16. Recommender systems → [[Collaborative Filtering and Matrix Factorization]], [[Evaluating Recommenders]]
| | |
|---|---|
| MF prediction | $\hat r_{ui}=\mu+b_u+b_i+p_u^\top q_i$ |
| MF loss | $\sum_{(u,i)\in\Omega}(r_{ui}-\hat r_{ui})^2+\lambda(\lVert p_u\rVert^2+\lVert q_i\rVert^2)$ |
| BPR | $-\sum\ln\sigma(\hat x_{ui}-\hat x_{uj})$ |
| DCG / NDCG | $\sum_k\frac{2^{rel_k}-1}{\log_2(k+1)}$ / $\frac{DCG}{IDCG}$ |
| MRR | $\frac1{|U|}\sum_u\frac1{\text{rank}_u}$ |

## 17. Time series → [[Time Series Forecasting]], [[Classical Forecasting Models]], [[Time Series Validation and Features]]
| | |
|---|---|
| SES | $\ell_t=\alpha y_t+(1-\alpha)\ell_{t-1}$ |
| Holt | $\hat y_{t+h}=\ell_t+hb_t$ |
| AR(p) / MA(q) | $y_t=c+\sum\phi_iy_{t-i}+\varepsilon_t$ / $y_t=c+\varepsilon_t+\sum\theta_i\varepsilon_{t-i}$ |
| Differencing | $y'_t=y_t-y_{t-1}$, seasonal $y_t-y_{t-m}$ |
| MASE | $\frac{\text{MAE}}{\frac1{T-m}\sum|y_t-y_{t-m}|}$ |
| Pinball loss | $\max(\tau u,(\tau-1)u)$, $u=y-\hat y$ |

## 18. MLOps and monitoring → [[MLOps Overview]], [[Model Deployment and Serving]]
| | |
|---|---|
| PSI | $\sum_b(a_b-e_b)\ln\frac{a_b}{e_b}$ (< 0.1 stable, > 0.25 shift) |
| KS statistic | $\sup_x|F_1(x)-F_2(x)|$ |
| Little's law | $L=\lambda W$ |
| Two-proportion z | $z=\frac{\hat p_1-\hat p_2}{\sqrt{\hat p(1-\hat p)(1/n_1+1/n_2)}}$ |

## 19. Learning theory and causality → [[Learning Theory]], [[Causal Inference]]
| | |
|---|---|
| Finite class (realisable) | $m\ge\frac1\epsilon(\ln|\mathcal H|+\ln\frac1\delta)$ |
| Hoeffding | $P(|\bar X-\mu|\ge\epsilon)\le2e^{-2N\epsilon^2}$ (for $X\in[0,1]$) |
| VC of linear classifiers in $\mathbb R^d$ | $d+1$ |
| ATE | $\mathbb E[Y(1)-Y(0)]$ |
| IPW estimate | $\frac1N\sum\Big[\frac{T_iY_i}{e(X_i)}-\frac{(1-T_i)Y_i}{1-e(X_i)}\Big]$, $e(x)=P(T=1\mid x)$ |
| Backdoor adjustment | $p(y\mid do(x))=\sum_zp(y\mid x,z)p(z)$ |

## 20. Training tricks → [[Training Tricks]], [[Optimizers]]
| | |
|---|---|
| Cosine LR schedule | $\eta_t=\eta_{\min}+\tfrac12(\eta_{\max}-\eta_{\min})\big(1+\cos\frac{\pi t}{T}\big)$, often after linear warm-up |
| Gradient clipping (norm) | $g\leftarrow g\cdot\min\!\big(1,\frac{c}{\lVert g\rVert}\big)$ |
| Label smoothing | $y^{LS}=(1-\varepsilon)\,y_{\text{one-hot}}+\varepsilon/K$ |
| LayerNorm | $\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}\gamma+\beta$, statistics over the *features* of one example |
| Weight decay ≈ L2 (plain SGD only) | $\theta\leftarrow(1-\eta\lambda)\theta-\eta\nabla L$ |
| Linear scaling rule | batch $\times k$ ⇒ learning rate $\times k$ (with warm-up) |

## 21. LLMs and retrieval → [[LLMs Overview]], [[RAG and Agents]], [[Fine-tuning and Alignment]], [[RAG over My Notes]]
| | |
|---|---|
| Temperature | $p_i=\frac{e^{z_i/T}}{\sum_je^{z_j/T}}$ ($T\to0$ greedy, $T>1$ flatter) |
| Top-$k$ / top-$p$ | sample from the $k$ most likely / the smallest set with cumulative prob. $\ge p$ |
| Cross-entropy ↔ perplexity | $\mathrm{PPL}=e^{\mathcal L}$ ($\mathcal L$ in nats per token) |
| RoPE | rotate each pair $(x_{2i},x_{2i+1})$ at position $p$ by angle $p\,\theta_i$, $\theta_i=10000^{-2i/d}$ ⇒ $q_m^\top k_n$ depends only on $m-n$ |
| Training compute | $C\approx6ND$ FLOPs ($N$ parameters, $D$ tokens) |
| Chinchilla rule of thumb | compute-optimal $D\approx20N$ tokens |
| KV cache | $2\cdot L\cdot d\cdot T\cdot b$ bytes per sequence ($L$ layers, $T$ tokens, $b$ bytes/value) |
| Memory to train with Adam | ≈ 16 bytes/param (fp16 weights + grads, fp32 master + $m$ + $v$) |
| DPO | $-\log\sigma\!\Big(\beta\log\frac{\pi_\theta(y_w\mid x)}{\pi_{\text{ref}}(y_w\mid x)}-\beta\log\frac{\pi_\theta(y_l\mid x)}{\pi_{\text{ref}}(y_l\mid x)}\Big)$ |
| Cosine similarity | $\frac{u^\top v}{\lVert u\rVert\lVert v\rVert}$ (= dot product for normalised embeddings) |
| BM25 | $\sum_{q}\mathrm{IDF}(q)\frac{f(q,D)(k_1+1)}{f(q,D)+k_1(1-b+b\frac{|D|}{\text{avgdl}})}$, $k_1\approx1.2$, $b\approx0.75$ |
| Reciprocal rank fusion | $\mathrm{RRF}(d)=\sum_{\text{rankers}}\frac1{k+\mathrm{rank}(d)}$, rank from 1, $k=60$ |
| Recall@k / hit@k | fraction of queries with a relevant item in the top $k$ |

## 22. Classic papers in one line each → [[Paper-to-Code Months]]
| | |
|---|---|
| ResNet | $y=\mathrm{ReLU}(F(x)+\mathrm{shortcut}(x))$ |
| word2vec SGNS | $-\log\sigma(u_o^\top v_c)-\sum_{k=1}^K\log\sigma(-u_k^\top v_c)$, noise $\propto f(w)^{3/4}$, keep prob. $\sqrt{t/f(w)}$ |
| PPMI (≈ what SGNS factorises) | $\max\!\big(0,\log\frac{p(i,j)}{p(i)p(j)}\big)$ |
| LightGCN | $E^{(k+1)}=D^{-1/2}AD^{-1/2}E^{(k)}$, $E=\frac1{K+1}\sum_kE^{(k)}$ |
| DDPM reverse step | $x_{t-1}=\frac1{\sqrt{\alpha_t}}\big(x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t,t)\big)+\sigma_tz$, $\sigma_t^2=\beta_t$ |
| Fold-in a new user (ALS) | $p_u=(Q_I^\top Q_I+\lambda I)^{-1}Q_I^\top r_u$ |

## 23. Statistics for comparing models → [[Model Evaluation and Metrics]], [[Probability for ML]]
| | |
|---|---|
| Std. error of an accuracy | $\sqrt{p(1-p)/n}$ (e.g. $p=0.88$, $n=108$ ⇒ ≈ 3 points) |
| 95 % CI of a mean | $\bar x\pm1.96\,s/\sqrt n$ (use $t_{n-1}$ for small $n$) |
| Paired t-test | $t=\frac{\bar d}{s_d/\sqrt n}$ on per-fold/per-example differences $d$ |
| McNemar (two classifiers, same test set) | $\chi^2=\frac{(|b-c|-1)^2}{b+c}$, $b,c$ = examples only one model gets right |
| Bootstrap CI | resample the test set with replacement $B$ times, take the 2.5 / 97.5 percentiles |
| Bonferroni | test each of $m$ hypotheses at $\alpha/m$ |
| Cohen's $d$ | $\frac{\bar x_1-\bar x_2}{s_{\text{pooled}}}$ |

## 24. Calibration, fairness, explainability → [[Explainability and Fairness]]
| | |
|---|---|
| Brier score | $\frac1N\sum(p_i-y_i)^2$ |
| ECE | $\sum_m\frac{|B_m|}{N}\,\big|\mathrm{acc}(B_m)-\mathrm{conf}(B_m)\big|$ over confidence bins $B_m$ |
| Temperature scaling | $\mathrm{softmax}(z/T)$, fit $T$ on validation NLL |
| Demographic parity gap | $|P(\hat y=1\mid A=0)-P(\hat y=1\mid A=1)|$ |
| Equalised odds | equal TPR **and** FPR across groups |
| Shapley value | $\phi_i=\sum_{S\subseteq F\setminus\{i\}}\frac{|S|!\,(|F|-|S|-1)!}{|F|!}\big[v(S\cup\{i\})-v(S)\big]$ |

## 25. Search, games and evolution → [[Fun Projects]], [[RL Basics and MDPs]]
| | |
|---|---|
| A* priority | $f(n)=g(n)+h(n)$; optimal if $h$ is admissible ($h\le$ true cost) |
| Manhattan heuristic | $|\Delta r|+|\Delta c|$ (admissible on 4-connected unit grids) |
| Minimax | $V(s)=\max_a V(s')$ on your turn, $\min_a V(s')$ on the opponent's |
| Alpha–beta | prune when $\alpha\ge\beta$; best case $O(b^{d/2})$ nodes instead of $O(b^d)$ |
| (1+λ)-ES | sample $\theta'=\theta+\sigma\epsilon$, $\epsilon\sim\mathcal N(0,I)$; keep the best if it improves |
| Simulated annealing | accept worse moves with prob. $e^{-\Delta/T}$, lower $T$ over time |

## 26. Filtering, bandits and MCMC → [[Bayesian Inference]], [[MCMC]], [[RL Basics and MDPs]]
| | |
|---|---|
| Kalman predict | $x\leftarrow Fx$, $P\leftarrow FPF^\top+Q$ |
| Kalman update | $K=PH^\top(HPH^\top+R)^{-1}$, $x\leftarrow x+K(z-Hx)$, $P\leftarrow(I-KH)P$ |
| Gaussian fusion (1-D) | $\mu=\frac{\sigma_2^2\mu_1+\sigma_1^2\mu_2}{\sigma_1^2+\sigma_2^2}$, $\frac1{\sigma^2}=\frac1{\sigma_1^2}+\frac1{\sigma_2^2}$ |
| UCB1 | $\arg\max_a\hat\mu_a+\sqrt{2\ln t/n_a}$ |
| Thompson (Bernoulli) | sample $\theta_a\sim\mathrm{Beta}(1+s_a,1+f_a)$, play $\arg\max_a\theta_a$ |
| Regret | $R_T=T\mu^*-\sum_t\mu_{a_t}$ |
| Metropolis acceptance | $\min\big(1,\frac{p(x')}{p(x)}\big)$ for a symmetric proposal |
| Policy evaluation (closed form) | $V^\pi=(I-\gamma P_\pi)^{-1}R_\pi$ |

## 27. Graphs, features and tokens → [[Graph ML Overview]], [[Computer Vision Overview]], [[LLMs Overview]]
| | |
|---|---|
| PageRank | $r=\frac{1-d}{n}\mathbf 1+d\big(P^\top r+\frac1n\sum_{j\,\text{dangling}}r_j\mathbf 1\big)$, $d=0.85$ |
| Fiedler cut | sign of the 2nd eigenvector of $L_{sym}=I-D^{-1/2}AD^{-1/2}$ |
| Normalised cut | $\mathrm{Ncut}(A,B)=\mathrm{cut}(A,B)\big(\frac1{\mathrm{vol}A}+\frac1{\mathrm{vol}B}\big)$ |
| Sobel $x$ | $\begin{bmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{bmatrix}$ |
| Gradient orientation (HOG) | $\theta=\arctan2(g_y,g_x)\bmod180°$, histogram weighted by $\sqrt{g_x^2+g_y^2}$ |
| BPE step | merge the most frequent adjacent symbol pair; repeat for $k$ merges |
| Gini impurity / information gain | $1-\sum p_k^2$ / $H(\text{parent})-\sum_c\frac{n_c}{n}H(c)$ |
| Robust z-score | $\frac{x-\mathrm{median}}{1.4826\,\mathrm{MAD}}$ |
| Seasonal anomaly forecast | $\hat y_{t+h}=\mathrm{clim}_{t+h}+\phi^h(y_t-\mathrm{clim}_t)$ |

## 28. Building blocks you implemented → [[Projects Overview]]
| | |
|---|---|
| Encoder–decoder attention | self-attn (causal in the decoder) → cross-attn $\mathrm{softmax}(Q_{dec}K_{enc}^\top/\sqrt{d})V_{enc}$ → FFN, each with pre-LN residuals |
| Teacher forcing | decoder input = target shifted right (`BOS` + $y_{<t}$), loss on $y_t$ |
| PUCT (AlphaZero) | $a^*=\arg\max_a Q(a)+c\,P(a)\frac{\sqrt{\sum_bN(b)}}{1+N(a)}$ |
| AlphaZero loss | $-\pi^\top\log p_\theta(s)+(v_\theta(s)-z)^2$ (+ weight decay) |
| DQN target | $y=r+\gamma\max_{a'}Q_{\bar\theta}(s',a')(1-\text{done})$, Huber loss, target net $\bar\theta$ |
| Monte Carlo control | $Q(s,a)\leftarrow Q(s,a)+\frac1{N(s,a)}(G-Q(s,a))$ |
| Regret matching (CFR) | $\sigma(a)\propto\max(R(a),0)$; average strategy → Nash equilibrium |
| ELBO (reparameterised) | $\mathbb E_{\epsilon}[\log p(y,w=\mu+\sigma\epsilon)]+\sum_j\log\sigma_j$ |
| EM for GMMs | E: $r_{ik}\propto\pi_k\mathcal N(x_i\mid\mu_k,\Sigma_k)$; M: $\pi_k=\frac{N_k}{n}$, $\mu_k=\frac{\sum_ir_{ik}x_i}{N_k}$, $\Sigma_k=\frac{\sum_ir_{ik}(x_i-\mu_k)(x_i-\mu_k)^\top}{N_k}$ |
| GP posterior | $\mu_*=K_*^\top(K+\sigma_n^2I)^{-1}y$, $\Sigma_*=K_{**}-K_*^\top(K+\sigma_n^2I)^{-1}K_*$ |
| Pegasos step | $\eta_t=\frac1{\lambda t}$; $w\leftarrow(1-\eta_t\lambda)w+\eta_t y_ix_i\,[y_iw^\top x_i<1]$ |
| Ridge closed form | $\hat w=(X^\top X+\lambda I)^{-1}X^\top y$ |
| Knuth minimax (Mastermind) | choose $g$ minimising $\max_f|\{s\in S: \mathrm{fb}(g,s)=f\}|$ |
| Walk-forward split $k$ | train $=[0,\,t_k-\text{gap})$, test $=[t_k,\,t_k+h)$ |

See also: [[ML Glossary]] · [[Exam Checklist]] · [[8-semester/ML/cheetsheet|Course cheat sheet (8th semester)]]
