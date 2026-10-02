---
tags: [ml, deep-learning, practice]
---
# Training Tricks

## Initialization
Xavier/Glorot (tanh), He/Kaiming (ReLU). Never all zeros.

## Normalization
BatchNorm (CNN), LayerNorm ([[Transformers]]), GroupNorm (small batches), RMSNorm.

## Regularization
Dropout, weight decay, label smoothing, mixup/cutmix, augmentation, early stopping ([[Overfitting and Regularization]]).

## Optimization
Warm-up + decay schedules, gradient clipping, mixed precision (bf16), gradient accumulation, gradient checkpointing ([[Optimizers]]).

## Debug checklist
1. Overfit 10 examples to ~0 loss.
2. Initial loss ≈ $\log K$ for $K$ classes.
3. Check data/labels visually and shapes.
4. Turn off augmentation/regularization first, add back later.
5. Watch gradient norms, activation statistics, learning-rate sweep.
6. Fix seeds; log with TensorBoard / Weights & Biases.

## Transfer learning
Freeze backbone → train head → unfreeze with small LR.
Pitfalls: [[Common Pitfalls]]. Code: [[PyTorch Recipes]].

## Learn more
- [Karpathy – Zero to Hero](https://karpathy.ai/zero-to-hero.html)
- [Stanford CS231n](https://cs231n.stanford.edu/) · [notes](https://cs231n.github.io/)
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/course/)
