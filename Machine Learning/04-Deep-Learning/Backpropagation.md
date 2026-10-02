---
tags: [ml, deep-learning, optimization]
---
# Backpropagation

Efficient application of the chain rule on a computation graph ([[Matrix Calculus Cheatsheet]]).

## For an MLP
Forward: $z^{(l)}=W^{(l)}h^{(l-1)}+b^{(l)},\ h^{(l)}=\phi(z^{(l)})$.
Backward with $\delta^{(l)}=\partial L/\partial z^{(l)}$:
$$\delta^{(L)}=\nabla_{h}L\odot\phi'(z^{(L)}),\quad \delta^{(l)}=\big(W^{(l+1)\top}\delta^{(l+1)}\big)\odot\phi'(z^{(l)})$$
$$\frac{\partial L}{\partial W^{(l)}}=\delta^{(l)}h^{(l-1)\top},\qquad \frac{\partial L}{\partial b^{(l)}}=\delta^{(l)}$$

Softmax + cross-entropy: $\delta^{(L)}=\hat p-y$.

## Notes
- Cost ≈ 2–3× a forward pass; cache activations (memory ↔ gradient checkpointing trade-off).
- **Vanishing / exploding gradients**: products of Jacobians; mitigated by ReLU, residual connections, normalization, gradient clipping ([[Training Tricks]]).
- Automatic differentiation in PyTorch/JAX does this for you ([[PyTorch Recipes]]).
