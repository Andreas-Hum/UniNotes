---
tags: [ml, masters, checklist]
---
# Master's Self-Assessment

For each item, mark the **highest level** you can honestly reach:
**E** = explain intuitively · **D** = derive / do by hand · **I** = implement from scratch · **C** = critique (when it fails, alternatives)

A strong ML master's graduate is usually at **D** for the foundations, **I** for the core algorithms, and **C** in their specialisation. Being at **E** for topics outside your specialisation is completely normal.

## Foundations
- [ ] Linear algebra: eigendecomposition, SVD, PSD matrices → [[Linear Algebra for ML]]  `E D I C`
- [ ] Matrix calculus, chain rule → [[Matrix Calculus Cheatsheet]]  `E D I C`
- [ ] Probability: Bayes, MLE vs MAP, common distributions → [[Probability for ML]]  `E D I C`
- [ ] Optimisation: convexity, GD/SGD, Lagrangians/KKT → [[Calculus and Optimization]]  `E D I C`
- [ ] Information theory: entropy, KL, cross-entropy → [[Information Theory]]  `E D I C`
- [ ] Generalisation: bias–variance, PAC, VC dimension → [[Learning Theory]]  `E D I C`

## Classical ML
- [ ] Linear and logistic regression, regularisation → [[Linear Regression]], [[Logistic Regression]]  `E D I C`
- [ ] SVMs + kernels (primal, dual, kernel trick) → [[Support Vector Machines]]  `E D I C`
- [ ] Trees, random forests, gradient boosting → [[Ensemble Methods]]  `E D I C`
- [ ] k-means, GMM + EM, PCA → [[Gaussian Mixture Models and EM]], [[PCA]]  `E D I C`
- [ ] Evaluation, cross-validation, leakage → [[Model Evaluation and Metrics]], [[Common Pitfalls]]  `E D I C`

## Deep learning
- [ ] MLP + backprop on paper → [[Backpropagation]]  `E D I C`
- [ ] CNNs, residual connections → [[CNN]]  `E D I C`
- [ ] Attention and the Transformer block → [[Transformers]]  `E D I C`
- [ ] Optimisers, normalisation, init, debugging → [[Optimizers]], [[Training Tricks]]  `E D I C`
- [ ] VAEs, GANs, diffusion → [[Generative Models]]  `E D I C`
- [ ] Contrastive / self-supervised learning → [[Self-Supervised and Contrastive Learning]]  `E D I C`

## Probabilistic ML
- [ ] Graphical models, d-separation → [[Probabilistic Graphical Models]]  `E D I C`
- [ ] Variational inference, the ELBO → [[Variational Inference]]  `E D I C`
- [ ] MCMC → [[MCMC]]  `E D I C`
- [ ] Gaussian processes → [[Gaussian Processes]]  `E D I C`

## Specialisations (go deep in 1–2)
- [ ] Recommender systems: MF, BPR, two-tower, sequential, multimodal → [[Recommender Systems Overview]], [[Multimodal Recommender Systems]]  `E D I C`
- [ ] Graph ML: embeddings, GNNs, link prediction → [[Graph ML Overview]]  `E D I C`
- [ ] NLP / LLMs → [[NLP Overview]], [[LLMs Overview]]  `E D I C`
- [ ] Vision → [[Computer Vision Overview]]  `E D I C`
- [ ] RL → [[RL Basics and MDPs]]  `E D I C`
- [ ] Causality → [[Causal Inference]]  `E D I C`

## Research & engineering
- [ ] Read and summarise a paper in one hour → [[Paper Reading Template]]  `E D I C`
- [ ] Design a fair experiment: baselines, seeds, ablations, significance → [[Research Skills]]  `E D I C`
- [ ] Reproduce a paper's main result  `E D I C`
- [ ] Git, PyTorch training loop, experiment tracking → [[PyTorch Recipes]], [[MLOps Overview]]  `E D I C`

> [!tip]
> Redo this every semester. Watching the letters move right is the best evidence against imposter syndrome. See [[Imposter Syndrome]].
