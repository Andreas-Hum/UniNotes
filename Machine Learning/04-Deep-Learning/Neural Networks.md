---
tags: [ml, deep-learning]
---
# Neural Networks

A feed-forward network composes affine maps and non-linearities:
$$h^{(l)}=\phi\big(W^{(l)}h^{(l-1)}+b^{(l)}\big),\quad \hat y=h^{(L)}$$

- **Universal approximation**: one hidden layer with enough units approximates any continuous function on a compact set. Depth gives efficiency.
- **Output + loss**: regression → linear + MSE; binary → sigmoid + BCE; multiclass → softmax + cross-entropy ([[Logistic Regression]]).
- **Training**: [[Backpropagation]] + [[Optimizers]]; initialization (He/Xavier) matters, see [[Training Tricks]].
- Non-linearities: [[Activation Functions]].
- Architectures: [[CNN]] (images), [[RNN and LSTM]] (sequences), [[Transformers]] (everything now), [[Graph Neural Networks]].
- Regularization: weight decay, dropout, early stopping, augmentation ([[Overfitting and Regularization]]).

## Why non-linear?
Without $\phi$ the stack collapses to one linear map and cannot solve XOR ([[Linear Models for Classification]]).

## Learn more
- [MIT 6.S191 — Introduction to Deep Learning (lecture playlist)](https://www.youtube.com/playlist?list=PLtBw6njQRU-rwp5__7C0oIVt26ZgjG9NI) · [course site & labs](https://introtodeeplearning.com/)
- [3Blue1Brown – Neural Networks](https://www.3blue1brown.com/topics/neural-networks)
- [Nielsen – Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/)
- [Dive into Deep Learning](https://d2l.ai/)
