---
tags: [ml, fundamentals]
---
# Learning Paradigms

| Paradigm | Data | Goal | Examples |
|---|---|---|---|
| **Supervised** | $(x, y)$ pairs | predict $y$ from $x$ | [[Linear Regression]], [[Decision Trees]], [[Neural Networks]] |
| **Unsupervised** | $x$ only | find structure | [[Clustering]], [[PCA]] |
| **Semi-supervised** | few labels + many unlabeled | use both | label propagation, pseudo-labeling |
| **Self-supervised** | labels derived from data | learn representations | masked language modeling, contrastive learning |
| **Reinforcement** | reward signal from environment | maximize return | [[Q-Learning and Policy Gradients]] |
| **Online** | stream of examples | update incrementally | perceptron, bandits |
| **Transfer / fine-tuning** | pretrained model + small data | adapt | BERT, ResNet fine-tuning |

## Discriminative vs. generative
- **Discriminative** models learn $p(y\mid x)$ directly ([[Logistic Regression]], [[Support Vector Machines]]).
- **Generative** models learn $p(x, y) = p(x\mid y)p(y)$ ([[Naive Bayes]], [[Gaussian Mixture Models and EM]], [[Generative Models]]).

## Parametric vs. non-parametric
Parametric: fixed number of parameters (linear models). Non-parametric: complexity grows with data ([[k-Nearest Neighbors]], [[Gaussian Processes]], kernel methods).
