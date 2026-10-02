---
tags: [ml, masters, projects]
---
# Implement From Scratch

Implementing an algorithm yourself is the fastest way to understand it. Use NumPy (or PyTorch tensors without `nn` modules), then compare with the library version.

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
